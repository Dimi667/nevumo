import hashlib
import logging
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

import bcrypt as _bcrypt
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from config import settings
from models import AuthRateLimit, PendingLeadClaim, Lead

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
