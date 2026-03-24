from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config import settings
from dependencies import get_db
from models import PasswordResetToken, User
from schemas import (
    AuthTokenResponse,
    CheckEmailRequest,
    CheckEmailResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
    ResetPasswordResponse,
    ValidateResetTokenRequest,
    ValidateResetTokenResponse,
)
from services.auth_service import (
    check_rate_limit,
    create_jwt,
    generate_reset_token,
    get_dummy_hash,
    hash_password,
    hash_token,
    record_rate_limit,
    send_reset_email,
    verify_password,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/check-email", response_model=CheckEmailResponse)
async def check_email(
    body: CheckEmailRequest,
    db: Session = Depends(get_db),
) -> CheckEmailResponse:
    user = db.query(User).filter(User.email == body.email).first()
    return CheckEmailResponse(data={"exists": user is not None})


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
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    record_rate_limit(db, ip, "register")

    token = create_jwt(user.id, user.email, user.role)
    return AuthTokenResponse(data={
        "token": token,
        "user": {"id": str(user.id), "email": user.email, "role": user.role},
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

    token = create_jwt(user.id, user.email, user.role)
    return AuthTokenResponse(data={
        "token": token,
        "user": {"id": str(user.id), "email": user.email, "role": user.role},
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
        send_reset_email(user.email, reset_url)

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
