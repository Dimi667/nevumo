import hashlib
import json
import secrets
import urllib.parse
from datetime import datetime, timedelta
from secrets import token_hex
from typing import Optional, Any

import httpx
from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from apps.api.config import settings
from apps.api.dependencies import get_db, get_current_user
from apps.api.models import Location, MagicLinkToken, PasswordResetToken, Provider, User
from apps.api.schemas import (
    AuthTokenResponse,
    ChangePasswordRequest,
    ChangePasswordResponse,
    CheckEmailRequest,
    CheckEmailResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    GoogleOAuthCompleteRequest,
    LoginRequest,
    MagicLinkRequest,
    RegisterRequest,
    RequestMagicLinkBody,
    ResetPasswordRequest,
    ResetPasswordResponse,
    SlugCheckResponse,
    SwitchRoleRequest,
    ValidateResetTokenRequest,
    ValidateResetTokenResponse,
)
from apps.api.services.auth_service import (
    check_rate_limit,
    create_jwt,
    delete_user_account,
    generate_reset_token,
    get_dummy_hash,
    get_or_create_oauth_user,
    hash_password,
    hash_token,
    link_pending_claims,
    record_rate_limit,
    send_reset_email,
    verify_password,
)
from apps.api.services.email_service import email_service

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/check-email", response_model=CheckEmailResponse)
async def check_email(
    body: CheckEmailRequest,
    db: Session = Depends(get_db),
) -> CheckEmailResponse:
    user = db.query(User).filter(User.email == body.email).first()
    return CheckEmailResponse(data={"exists": user is not None})


@router.get("/register/slug/check", response_model=SlugCheckResponse)
async def check_registration_slug(
    slug: str = Query(..., min_length=2, max_length=50),
    city_slug: Optional[str] = Query(None),
    category_slug: Optional[str] = Query(None),
    db: Session = Depends(get_db),
) -> SlugCheckResponse:
    """Check slug availability during registration (no auth required)."""
    from apps.api.services.provider_service import validate_slug, generate_slug_suggestions
    
    is_valid, error = validate_slug(slug)
    if not is_valid:
        return SlugCheckResponse(
            success=True,
            data={"available": False, "valid": False, "error": error}
        )
    
    existing = db.query(Provider).filter(Provider.slug == slug).first()
    if existing:
        suggestions = generate_slug_suggestions(slug, city_slug, category_slug, db)
        return SlugCheckResponse(
            success=True,
            data={"available": False, "valid": True, "suggestions": suggestions}
        )
    
    return SlugCheckResponse(
        success=True,
        data={"available": True, "valid": True}
    )


@router.post("/register", response_model=AuthTokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> AuthTokenResponse:
    ip = request.client.host if request.client else "unknown"

    if not check_rate_limit(db, ip, "register"):
        return JSONResponse(status_code=429, content={"success": False, "error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests. Please try again later."}})

    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        record_rate_limit(db, ip, "register")
        return JSONResponse(status_code=409, content={"success": False, "error": {"code": "EMAIL_ALREADY_EXISTS", "message": "Email is already registered"}})

    user = User(
        email=body.email,
        password_hash=hash_password(body.password),
        role=body.role,
        city_id=body.city_id,
        is_active=True,
    )
    db.add(user)
    db.flush()  # assign user.id before creating Provider

    if body.role == "provider":
        # Create provider with draft slug (not based on email) and email as placeholder business_name
        # The actual slug and business name will be set during onboarding step 1
        draft_slug = f"draft{token_hex(6)}"  # e.g., drafta3f7b2d8e1c5
        provider = Provider(
            user_id=user.id,
            business_name=body.email,  # Placeholder to indicate onboarding needed
            slug=draft_slug,
            rating=0,
            verified=False,
            availability_status="active",
        )
        db.add(provider)
    
    db.refresh(user)

    record_rate_limit(db, ip, "register")

    # Link any pending claims after successful registration
    try:
        link_pending_claims(user.id, user.email, user.phone, db)
    except Exception:
        # Auth must NEVER fail due to claim linking errors
        pass
    email_service.send_welcome_email(user.email, user.role)

    token = create_jwt(user.id, user.email, user.role)
    return AuthTokenResponse(data={
        "token": token,
        "user": {"id": str(user.id), "email": user.email, "role": user.role, "locale": user.locale},
    })


@router.post("/login", response_model=AuthTokenResponse)
async def login(
    body: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> AuthTokenResponse:
    ip = request.client.host if request.client else "unknown"

    if not check_rate_limit(db, ip, "login"):
        return JSONResponse(status_code=429, content={"success": False, "error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests. Please try again later."}})

    user = db.query(User).filter(User.email == body.email).first()

    city_slug = None
    if user.city_id:
        location = db.query(Location).filter(Location.id == user.city_id).first()
        city_slug = location.slug if location else None

    # Always run bcrypt verify to prevent timing-based email enumeration.
    candidate_hash = (user.password_hash if (user and user.password_hash) else get_dummy_hash())
    valid = verify_password(body.password, candidate_hash)

    if not user or not valid:
        record_rate_limit(db, ip, "login")
        return JSONResponse(status_code=401, content={"success": False, "error": {"code": "INVALID_CREDENTIALS", "message": "Invalid email or password"}})

    if not user.is_active:
        record_rate_limit(db, ip, "login")
        return JSONResponse(status_code=403, content={"success": False, "error": {"code": "ACCOUNT_DISABLED", "message": "This account has been disabled"}})

    record_rate_limit(db, ip, "login")

    # Link any pending claims after successful login
    try:
        link_pending_claims(user.id, user.email, user.phone, db)
    except Exception:
        # Auth must NEVER fail due to claim linking errors
        pass

    token = create_jwt(user.id, user.email, user.role)
    return AuthTokenResponse(data={
        "token": token,
        "user": {"id": str(user.id), "email": user.email, "role": user.role, "city_slug": city_slug},
    })


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(
    body: ForgotPasswordRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> ForgotPasswordResponse:
    ip = request.client.host if request.client else "unknown"

    if not check_rate_limit(db, ip, "forgot"):
        return JSONResponse(status_code=429, content={"success": False, "error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests. Please try again later."}})

    record_rate_limit(db, ip, "forgot")

    user = db.query(User).filter(User.email == body.email, User.is_active == True).first()  # noqa: E712

    if user:
        raw_token, token_hash = generate_reset_token()
        expires_at = datetime.utcnow() + timedelta(minutes=settings.RESET_TOKEN_EXPIRY_MINUTES)

        reset_record = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        db.add(reset_record)
        db.commit()

        locale = user.locale or "en"
        reset_url = f"{settings.APP_URL}/{locale}/auth/reset-password?token={raw_token}"
        email_service.send_password_reset_email(user.email, reset_url)

    # Always return the same response — no email enumeration.
    return ForgotPasswordResponse(data={
        "message": "If an account with this email exists, a reset link has been sent.",
    })


@router.post("/validate-reset-token", response_model=ValidateResetTokenResponse)
async def validate_reset_token(
    body: ValidateResetTokenRequest,
    db: Session = Depends(get_db),
) -> ValidateResetTokenResponse:
    token_hash = hash_token(body.token)
    record = (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.token_hash == token_hash)
        .first()
    )

    if not record:
        return ValidateResetTokenResponse(data={"valid": False, "error": "expired"})

    if record.used_at is not None:
        return ValidateResetTokenResponse(data={"valid": False, "error": "used"})

    if record.expires_at < datetime.utcnow():
        return ValidateResetTokenResponse(data={"valid": False, "error": "expired"})

    return ValidateResetTokenResponse(data={"valid": True})


@router.post("/reset-password", response_model=ResetPasswordResponse)
async def reset_password(
    body: ResetPasswordRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> ResetPasswordResponse:
    ip = request.client.host if request.client else "unknown"

    if not check_rate_limit(db, ip, "reset"):
        return JSONResponse(status_code=429, content={"success": False, "error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests. Please try again later."}})

    token_hash = hash_token(body.token)
    record = (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.token_hash == token_hash)
        .first()
    )

    if not record:
        record_rate_limit(db, ip, "reset")
        return JSONResponse(status_code=400, content={"success": False, "error": {"code": "TOKEN_INVALID", "message": "Reset token is invalid"}})

    if record.used_at is not None:
        record_rate_limit(db, ip, "reset")
        return JSONResponse(status_code=400, content={"success": False, "error": {"code": "TOKEN_USED", "message": "Reset token has already been used"}})

    if record.expires_at < datetime.utcnow():
        record_rate_limit(db, ip, "reset")
        return JSONResponse(status_code=400, content={"success": False, "error": {"code": "TOKEN_EXPIRED", "message": "Reset token has expired"}})

    user = db.query(User).filter(User.id == record.user_id, User.is_active == True).first()  # noqa: E712
    if not user:
        record_rate_limit(db, ip, "reset")
        return JSONResponse(status_code=400, content={"success": False, "error": {"code": "TOKEN_INVALID", "message": "Reset token is invalid"}})

    user.password_hash = hash_password(body.password)
    record.used_at = datetime.utcnow()
    db.commit()

    record_rate_limit(db, ip, "reset")

    token = create_jwt(user.id, user.email, user.role)
    return ResetPasswordResponse(data={
        "token": token,
        "user": {"id": str(user.id), "email": user.email, "role": user.role},
    })


@router.post("/password", response_model=ChangePasswordResponse)
async def change_password(
    body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ChangePasswordResponse:
    """Change or set password for authenticated user.
    
    - If user is passwordless (password_hash is None): set new password (current_password ignored)
    - If user has password: verify current_password, then set new password
    """
    # Rate limit: 5 attempts per 15 minutes per user
    if not check_rate_limit(db, str(current_user.id), "change_password"):
        return JSONResponse(
            status_code=429,
            content={"success": False, "error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Too many attempts. Please try again later."}}
        )

    # Reload user from DB to get fresh password_hash
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        return JSONResponse(
            status_code=404,
            content={"success": False, "error": {"code": "USER_NOT_FOUND", "message": "User not found"}}
        )

    # Passwordless user: set password directly
    if user.password_hash is None:
        user.password_hash = hash_password(body.new_password)
        db.commit()
        record_rate_limit(db, str(current_user.id), "change_password")
        return ChangePasswordResponse(data={"message": "password_set"})

    # User has password: verify current password
    if body.current_password is None:
        record_rate_limit(db, str(current_user.id), "change_password")
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": {"code": "CURRENT_PASSWORD_REQUIRED", "message": "Current password is required"}}
        )

    if not verify_password(body.current_password, user.password_hash):
        record_rate_limit(db, str(current_user.id), "change_password")
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": {"code": "INVALID_CURRENT_PASSWORD", "message": "Current password is invalid"}}
        )

    # Set new password
    user.password_hash = hash_password(body.new_password)
    db.commit()
    record_rate_limit(db, str(current_user.id), "change_password")
    return ChangePasswordResponse(data={"message": "password_changed"})


@router.post("/switch-role", response_model=AuthTokenResponse)
async def switch_role(
    body: SwitchRoleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AuthTokenResponse:
    if current_user.role == body.role:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": {"code": "ALREADY_IN_ROLE", "message": "Already in this role"}},
        )

    if body.role == "provider":
        from apps.api.services.provider_service import get_or_create_provider
        from secrets import token_hex
        
        # Check if provider already exists
        from apps.api.models import Provider
        existing_provider = db.query(Provider).filter(Provider.user_id == current_user.id).first()
        
        if existing_provider:
            # Provider already exists, no need to create
            pass
        elif body.business_name and body.preferred_slug:
            # User provided business_name and slug, create provider with those values
            get_or_create_provider(
                current_user,
                db,
                preferred_slug=body.preferred_slug,
                business_name=body.business_name,
            )
        else:
            # No provider exists and no business_name/slug provided - create draft provider
            # This matches the registration flow for provider role
            draft_slug = f"draft{token_hex(6)}"
            provider = Provider(
                user_id=current_user.id,
                business_name=current_user.email,  # Placeholder to indicate onboarding needed
                slug=draft_slug,
                rating=0,
                verified=False,
                availability_status="active",
            )
            db.add(provider)

    current_user.role = body.role
    db.commit()

    token = create_jwt(current_user.id, current_user.email, body.role)
    return AuthTokenResponse(data={
        "token": token,
        "user": {
            "id": str(current_user.id),
            "email": current_user.email,
            "role": body.role,
            "locale": current_user.locale,
        },
    })


@router.post("/magic-link", response_model=AuthTokenResponse)
async def magic_link_auth(
    body: MagicLinkRequest,
    db: Session = Depends(get_db),
) -> AuthTokenResponse:
    import hashlib
    
    # Hash token
    token_hash = hashlib.sha256(body.token.encode()).hexdigest()
    
    # Look up token
    token_record = db.query(MagicLinkToken).filter(MagicLinkToken.token_hash == token_hash).first()
    
    if not token_record:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": {"code": "TOKEN_INVALID", "message": "Invalid magic link token"}}
        )
    
    if token_record.expires_at < datetime.utcnow():
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": {"code": "TOKEN_EXPIRED", "message": "Magic link has expired"}}
        )
    
    if token_record.used_at is not None:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": {"code": "TOKEN_USED", "message": "Magic link has already been used"}}
        )
    
    # Get or create user
    user = db.query(User).filter(User.email == token_record.email).first()
    if not user:
        user = User(
            email=token_record.email,
            role='client',
            locale='en',
            is_active=True,
            password_hash=None  # passwordless account
        )
        db.add(user)
        db.flush()
    
    # Mark token as used
    token_record.used_at = datetime.utcnow()
    
    # Link pending claims
    try:
        link_pending_claims(user.id, user.email, user.phone, db)
    except Exception:
        # Auth must NEVER fail due to claim linking errors
        pass
    
    db.commit()
    
    # Create JWT
    token = create_jwt(user.id, user.email, user.role)
    return AuthTokenResponse(data={
        "token": token,
        "user": {"id": str(user.id), "email": user.email, "role": user.role},
    })


@router.post("/request-magic-link", status_code=200)
async def request_magic_link(
    body: RequestMagicLinkBody,
    db: Session = Depends(get_db),
) -> dict:
    email = body.email.strip().lower()

    # Rate limit check: allow only 1 request per minute per email
    cutoff = datetime.utcnow() - timedelta(seconds=60)
    recent = db.query(MagicLinkToken).filter(
        MagicLinkToken.email == email,
        MagicLinkToken.created_at >= cutoff,
    ).first()
    if recent:
        return JSONResponse(status_code=429, content={
            "success": False,
            "error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Please wait before requesting another link"}
        })

    # Delete existing unused tokens for this email (cleanup)
    db.query(MagicLinkToken).filter(
        MagicLinkToken.email == email,
        MagicLinkToken.used_at.is_(None),
    ).delete()

    # Generate token
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    # Create DB record
    magic_token = MagicLinkToken(
        email=email,
        token_hash=token_hash,
        expires_at=datetime.utcnow() + timedelta(hours=24),
        lead_id=None,
    )
    db.add(magic_token)
    db.commit()

    # Build magic link URL
    magic_link_url = f"{settings.APP_URL}/{body.lang}/auth/magic?token={raw_token}"

    # Send email
    email_service.send_login_magic_link_email(email, magic_link_url, body.lang)

    # Always return 200 (never reveal if email exists)
    return {"success": True, "message": "If this email is registered, you will receive a login link shortly"}


@router.delete("/account")
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    result = delete_user_account(db, current_user)
    if result["success"]:
        return JSONResponse(status_code=200, content=result)
    return JSONResponse(status_code=500, content=result)


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    return {
        "success": True,
        "data": {
            "id": str(current_user.id),
            "email": current_user.email,
            "role": current_user.role,
            "has_password": current_user.password_hash is not None,
            "locale": current_user.locale,
        }
    }


@router.get("/google")
async def google_oauth(
    lang: str = Query(default="en"),
    intent: str = Query(default="client"),
    category: str = Query(default=""),
    city: str = Query(default=""),
) -> RedirectResponse:
    """Redirect to Google OAuth consent page."""
    redirect_uri = f"{settings.OAUTH_REDIRECT_BASE}/api/v1/auth/google/callback"
    oauth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope=openid email profile&"
        f"access_type=offline&"
        f"prompt=consent&"
        f"state={lang}|{intent}|{category}|{city}"
    )
    return RedirectResponse(url=oauth_url)


@router.get("/google/callback")
async def google_oauth_callback(
    code: str = Query(...),
    state: str = Query(default="en"),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    """Handle Google OAuth callback."""
    # Parse state
    parts = state.split("|")
    lang = parts[0] if len(parts) > 0 else "en"
    intent = parts[1] if len(parts) > 1 else "client"
    category = parts[2] if len(parts) > 2 else ""
    city = parts[3] if len(parts) > 3 else ""

    try:
        # Exchange code for access token
        redirect_uri = f"{settings.OAUTH_REDIRECT_BASE}/api/v1/auth/google/callback"
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        async with httpx.AsyncClient() as client:
            token_response = await client.post(token_url, data=token_data)
            token_response.raise_for_status()
            token_json = token_response.json()
            access_token = token_json["access_token"]

            # Get user info
            user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
            user_info_response = await client.get(
                user_info_url,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            user_info_response.raise_for_status()
            user_info = user_info_response.json()

        email = user_info["email"]
        name = user_info.get("name", "")
        oauth_id = user_info["sub"]

        # Check if user exists
        existing_user = db.query(User).filter(
            (User.oauth_provider == "google") & (User.oauth_id == oauth_id) |
            (User.email == email)
        ).first()

        # If user does NOT exist → redirect to terms page
        if not existing_user:
            params = urllib.parse.urlencode({
                "email": email,
                "name": name,
                "oauth_id": oauth_id,
                "lang": lang,
                "intent": intent,
                "category": category,
                "city": city
            })
            return RedirectResponse(url=f"{settings.OAUTH_REDIRECT_BASE}/{lang}/auth/oauth-terms?{params}")

        # Get or create user
        user, jwt_token = get_or_create_oauth_user(
            email=email,
            name=name,
            oauth_provider="google",
            oauth_id=oauth_id,
            db=db,
        )

        # Redirect to frontend with token
        user_data = json.dumps({
            "id": str(user.id),
            "email": user.email,
            "role": user.role,
            "locale": user.locale,
        })

        # Determine redirect based on role
        if user.role == "provider":
            redirect = f"/{lang}/provider/dashboard"
        else:  # client
            redirect = f"/{lang}/client/dashboard"

        redirect_url = f"{settings.OAUTH_REDIRECT_BASE}/{lang}/auth/oauth-callback?token={jwt_token}&user={user_data}&redirect={redirect}"
        return RedirectResponse(url=redirect_url)

    except Exception as e:
        # On any error, redirect to auth page with error
        logger = __import__("logging").getLogger(__name__)
        logger.error(f"Google OAuth error: {e}")
        error_redirect = f"{settings.OAUTH_REDIRECT_BASE}/en/auth?error=oauth_failed"
        return RedirectResponse(url=error_redirect)


@router.post("/google/complete", response_model=AuthTokenResponse)
async def google_oauth_complete(
    body: GoogleOAuthCompleteRequest,
    db: Session = Depends(get_db),
) -> AuthTokenResponse:
    """Complete Google OAuth after terms acceptance."""
    # Check if user exists (protection against duplicate calls)
    existing_user = db.query(User).filter(
        (User.oauth_provider == "google") & (User.oauth_id == body.oauth_id) |
        (User.email == body.email)
    ).first()

    # If user exists → return JWT token directly
    if existing_user:
        if body.intent == "provider":
            from apps.api.models import Provider
            existing_provider = db.query(Provider).filter(Provider.user_id == existing_user.id).first()
            if not existing_provider:
                from secrets import token_hex
                draft_slug = f"draft{token_hex(6)}"
                provider = Provider(
                    user_id=existing_user.id,
                    business_name=existing_user.email,
                    slug=draft_slug,
                    rating=0,
                    verified=False,
                    availability_status="active",
                )
                db.add(provider)
                db.commit()
        token = create_jwt(existing_user.id, existing_user.email, existing_user.role)
        return AuthTokenResponse(data={
            "token": token,
            "user": {"id": str(existing_user.id), "email": existing_user.email, "role": existing_user.role},
            "is_new_user": False,
        })

    # If not exists → create user
    user = User(
        email=body.email,
        name=body.name,
        oauth_provider="google",
        oauth_id=body.oauth_id,
        role="provider" if body.intent == "provider" else "client",
        password_hash=None,
        is_active=True,
        locale=body.lang,
    )
    db.add(user)
    db.flush()
    link_pending_claims(user.id, user.email, user.phone, db)
    db.commit()

    if body.intent == "provider":
        from secrets import token_hex
        from apps.api.models import Provider
        draft_slug = f"draft{token_hex(6)}"
        provider = Provider(
            user_id=user.id,
            business_name=user.email,
            slug=draft_slug,
            rating=0,
            verified=False,
            availability_status="active",
        )
        db.add(provider)
        db.commit()

    # Return JWT token
    token = create_jwt(user.id, user.email, user.role)
    return AuthTokenResponse(data={
        "token": token,
        "user": {"id": str(user.id), "email": user.email, "role": user.role},
        "is_new_user": True,
    })
