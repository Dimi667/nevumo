import hashlib
import logging
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

import bcrypt as _bcrypt
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from apps.api.config import settings
from apps.api.models import AuthRateLimit, Lead, LeadMatch, Message, PendingLeadClaim, Provider, ProviderCity, Review, Service, ServiceCity, User

logger = logging.getLogger(__name__)

# Pre-computed bcrypt hash used as timing dummy when user not found during login.
# This prevents timing-based email enumeration by always running bcrypt verify.
_DUMMY_HASH = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"


def hash_password(password: str) -> str:
    return _bcrypt.hashpw(password.encode("utf-8"), _bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return _bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def create_jwt(user_id: UUID, email: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRY_HOURS)
    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_jwt(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None


def generate_reset_token() -> tuple[str, str]:
    """Generate a reset token. Returns (raw_token, sha256_hash)."""
    raw = secrets.token_urlsafe(32)
    hashed = hashlib.sha256(raw.encode()).hexdigest()
    return raw, hashed


def generate_magic_link_token(email: str, db: Session, hours: int = 24, invalidate_existing: bool = True) -> str:
    """Generate and persist a magic link token for the given email. Returns raw_token. Caller must commit."""
    import secrets
    import hashlib
    from datetime import datetime, timedelta
    from apps.api.models import MagicLinkToken
    if invalidate_existing:
        db.query(MagicLinkToken).filter(
            MagicLinkToken.email == email,
            MagicLinkToken.used_at.is_(None),
        ).delete()
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    magic_token = MagicLinkToken(
        email=email,
        token_hash=token_hash,
        expires_at=datetime.utcnow() + timedelta(hours=hours),
        lead_id=None,
    )
    db.add(magic_token)
    return raw_token


def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


def send_reset_email(email: str, reset_url: str) -> None:
    """Phase 1: log to console. Replace with real email provider later."""
    logger.info("=== PASSWORD RESET EMAIL ===")
    logger.info("To: %s", email)
    logger.info("Reset URL: %s", reset_url)
    logger.info("============================")


def get_dummy_hash() -> str:
    return _DUMMY_HASH


def check_rate_limit(db: Session, ip: str, action: str) -> bool:
    """Returns True if the request is allowed, False if rate limited."""
    window_start = datetime.utcnow() - timedelta(minutes=settings.AUTH_RATE_LIMIT_WINDOW_MINUTES)
    count = (
        db.query(AuthRateLimit)
        .filter(
            AuthRateLimit.ip == ip,
            AuthRateLimit.action == action,
            AuthRateLimit.created_at >= window_start,
        )
        .count()
    )
    return count < settings.AUTH_RATE_LIMIT_MAX


def record_rate_limit(db: Session, ip: str, action: str) -> None:
    db.add(AuthRateLimit(ip=ip, action=action))
    db.commit()


def link_pending_claims(user_id: UUID, email: str, phone: Optional[str], db: Session) -> int:
    """
    Called after successful register or login.
    Links any pending_lead_claims matching email OR phone to the user.
    Returns count of linked leads.
    """
    try:
        # Find all pending_lead_claims where:
        # - (email = user.email OR phone = user.phone)
        # - claimed = False
        # - expires_at > NOW()
        query = db.query(PendingLeadClaim).filter(
            PendingLeadClaim.claimed == False,
            PendingLeadClaim.expires_at > datetime.utcnow()
        )
        
        if email:
            query = query.filter(PendingLeadClaim.email == email)
        elif phone:
            query = query.filter(PendingLeadClaim.phone == phone)
        else:
            return 0
        
        pending_claims = query.all()
        linked_count = 0
        
        for claim in pending_claims:
            # UPDATE leads SET client_id = user_id WHERE id = claim.lead_id AND client_id IS NULL
            updated = db.query(Lead).filter(
                Lead.id == claim.lead_id,
                Lead.client_id.is_(None)
            ).update({"client_id": user_id})
            
            if updated:
                # UPDATE pending_lead_claims SET claimed = True, claimed_at = NOW()
                claim.claimed = True
                claim.claimed_at = datetime.utcnow()
                linked_count += 1
        
        if linked_count > 0:
            db.commit()
        
        return linked_count
    except Exception as e:
        logger.error(f"Error linking pending claims for user {user_id}: {e}")
        db.rollback()
        return 0


def delete_user_account(db: Session, user: User) -> dict:
    """
    GDPR-compliant account deletion.
    Runs all steps in a single DB transaction; rolls back on any failure.
    """
    try:
        db.query(Lead).filter(Lead.client_id == user.id).update({"client_id": None, "phone": "deleted"})

        provider = db.query(Provider).filter(Provider.user_id == user.id).first()
        if provider:
            db.query(Lead).filter(Lead.provider_id == provider.id).update({"provider_id": None})
            db.query(Service).filter(Service.provider_id == provider.id).delete()
            db.query(ProviderCity).filter(ProviderCity.provider_id == provider.id).delete()
            db.query(LeadMatch).filter(LeadMatch.provider_id == provider.id).delete()
            db.delete(provider)

        # Delete reviews written by this user as a client (NO ACTION FK — must be explicit)
        db.query(Review).filter(Review.client_id == user.id).delete()
        # Delete messages sent by this user (NO ACTION FK — preventive)
        db.query(Message).filter(Message.sender_id == user.id).delete()

        db.delete(user)

        db.commit()
        return {"success": True, "data": {"message": "account_deleted"}}
    except Exception as e:
        db.rollback()
        logger.error(f"Account deletion failed for user {user.id}: {e}")
        return {"success": False, "error": {"code": "DELETE_FAILED", "message": str(e)}}


def get_or_create_oauth_user(email: str, name: str, oauth_provider: str, oauth_id: str, db: Session) -> tuple[User, str]:
    """
    Get or create a user from OAuth credentials.
    Returns (user, jwt_token).
    """
    # Try to find user by oauth_provider + oauth_id
    user = db.query(User).filter(
        User.oauth_provider == oauth_provider,
        User.oauth_id == oauth_id
    ).first()

    if user:
        # Link pending claims for existing OAuth user
        try:
            link_pending_claims(user.id, user.email, user.phone, db)
        except Exception:
            pass
        token = create_jwt(user.id, user.email, user.role)
        return user, token

    # Try to find user by email
    user = db.query(User).filter(User.email == email).first()

    if user:
        # Update existing user with OAuth info
        user.oauth_provider = oauth_provider
        user.oauth_id = oauth_id
        db.commit()
        # Link pending claims
        try:
            link_pending_claims(user.id, user.email, user.phone, db)
        except Exception:
            pass
        token = create_jwt(user.id, user.email, user.role)
        return user, token

    # Create new user
    user = User(
        email=email,
        name=name,
        oauth_provider=oauth_provider,
        oauth_id=oauth_id,
        role="client",
        password_hash=None,
        is_active=True,
        locale="en",
    )
    db.add(user)
    db.flush()

    # Link pending claims
    try:
        link_pending_claims(user.id, user.email, user.phone, db)
    except Exception:
        pass

    db.commit()
    token = create_jwt(user.id, user.email, user.role)
    return user, token


def get_or_create_claim_user(
    email: str,
    lang: str,
    db: Session,
    scraped_phone: Optional[str] = None,
) -> tuple["User", str]:
    """
    Find or create a user for the magic-link claim flow.
    The claim token from the outreach email is proof of identity —
    no password or OAuth required.

    - If user exists with role='provider': issue new JWT, return as-is.
    - If user exists with role='client': update role to 'provider',
      issue new JWT, return updated user.
    - If user does not exist: create new User with role='provider',
      password_hash=None (passwordless), issue JWT, return new user.

    Returns: (user, jwt_token)
    """
    from apps.api.models import User  # local import to avoid circular

    email = email.strip().lower()

    # Find existing user by email
    user = db.query(User).filter(User.email == email).first()

    if user:
        # Ensure user has provider role for claim flow
        if user.role != "provider":
            user.role = "provider"
            db.commit()
            db.refresh(user)
        
        # Pre-fill phone from scraped data if user has no phone
        if scraped_phone and not user.phone:
            user.phone = scraped_phone
            db.commit()
            db.refresh(user)
    else:
        # Create new passwordless provider account
        user = User(
            email=email,
            role="provider",
            password_hash=None,
            is_active=True,
            locale=lang,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Pre-fill phone from scraped data if user has no phone
        if scraped_phone and not user.phone:
            user.phone = scraped_phone
            db.commit()
            db.refresh(user)

    jwt_token = create_jwt(
        user_id=user.id,
        email=user.email,
        role=user.role,
    )

    return user, jwt_token


def determine_post_auth_redirect(
    user: "User",
    db: "Session",
    lang: Optional[str] = None,
    claim_token: Optional[str] = None,
    intent: Optional[str] = None,
) -> str:
    """
    Determine the appropriate redirect URL after successful authentication.
    
    Priority order:
    1. claim_token: redirect to claim flow
    2. effective_role (intent or user.role): client or provider
    3. For providers: check onboarding completeness and redirect accordingly
    
    This function is READ-ONLY — it does not mutate the database.
    """
    # Priority 1: claim_token
    if claim_token:
        effective_lang = lang or user.locale or "en"
        return f"/{effective_lang}/claim/{claim_token}"
    
    # Priority 2: determine effective role
    effective_role = intent if intent in ("client", "provider") else user.role
    effective_lang = lang or user.locale or "en"
    
    # Priority 3: client role
    if effective_role == "client":
        return f"/{effective_lang}/client/dashboard"
    
    # Priority 4: provider role with onboarding check
    if effective_role == "provider":
        # Find provider profile linked to user
        provider = db.query(Provider).filter(Provider.user_id == user.id).first()
        
        if not provider:
            # New provider — send to wizard step 1
            return f"/{effective_lang}/provider/dashboard/profile"
        
        # Use existing check_onboarding_complete function if available
        try:
            from apps.api.services.provider_service import check_onboarding_complete
            is_complete, missing_fields = check_onboarding_complete(db, provider.id)
            
            if not is_complete:
                # Redirect based on what's missing
                if "business_name" in missing_fields:
                    return f"/{effective_lang}/provider/dashboard/profile"
                if "service" in missing_fields or "city" in missing_fields:
                    # /provider/dashboard/services exists
                    return f"/{effective_lang}/provider/dashboard/services"
            
            # All complete — dashboard
            return f"/{effective_lang}/provider/dashboard"
        except ImportError:
            # Fallback: check fields directly if check_onboarding_complete not available
            has_description = bool(provider.description and len(provider.description) > 10)
            has_photo = bool(getattr(provider, "profile_image_url", None))
            
            # Check if provider has at least 1 service with a city
            has_services = (
                db.query(ServiceCity)
                .join(Service, Service.id == ServiceCity.service_id)
                .filter(Service.provider_id == provider.id)
                .first()
            ) is not None
            
            if not has_description or not has_photo:
                # Step 1 — profile (description + photo)
                return f"/{effective_lang}/provider/dashboard/profile"
            
            if not has_services:
                # Step 2 — services
                return f"/{effective_lang}/provider/dashboard/services"
            
            # All complete — dashboard
            return f"/{effective_lang}/provider/dashboard"
    
    # Fallback
    return f"/{effective_lang}/client/dashboard"
