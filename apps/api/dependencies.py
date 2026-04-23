import os
from typing import Optional

import redis as redis_lib
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from apps.api.database import SessionLocal
from apps.api.services.auth_service import decode_jwt


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


_redis_client: Optional[redis_lib.Redis] = None

try:
    _redis_client = redis_lib.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 0)),
        decode_responses=True,
    )
    _redis_client.ping()
except Exception:
    _redis_client = None


def get_redis() -> Optional[redis_lib.Redis]:
    return _redis_client


_bearer = HTTPBearer()
_optional_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
):
    from apps.api.models import User  # local import to avoid circular

    token = credentials.credentials
    payload = decode_jwt(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()  # noqa: E712
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")

    return user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_optional_bearer),
    db: Session = Depends(get_db),
) -> Optional["User"]:
    from apps.api.models import User  # local import to avoid circular

    if credentials is None:
        return None

    token = credentials.credentials
    payload = decode_jwt(token)
    if not payload:
        return None

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()  # noqa: E712
    if not user:
        return None

    return user


def get_current_provider(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from apps.api.models import Provider

    provider = db.query(Provider).filter(Provider.user_id == current_user.id).first()
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Provider profile not found"
        )
    return provider
