import json
import re
from typing import Optional

import redis as redis_lib
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from apps.api.dependencies import get_current_user, get_db, get_redis
from apps.api.exceptions import INVALID_PHONE
from apps.api.services.export_service import export_user_data

router = APIRouter(prefix="/api/v1/user", tags=["user"])


# Pydantic models
class UserProfileUpdate(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None


class UserProfileResponse(BaseModel):
    id: str
    email: str
    name: Optional[str]
    phone: Optional[str]
    country_code: Optional[str]
    role: str


# Phone validation regex
PHONE_REGEX = re.compile(r"^[+\d][\d\s\(\)\-]{5,18}$")


def validate_phone(phone: str) -> Optional[str]:
    """Validate phone number format.
    
    Returns None if phone should be cleared (empty string),
    validated phone if valid, or raises INVALID_PHONE if invalid.
    """
    if phone == "":
        return None  # Clear the phone field
    
    if phone and not PHONE_REGEX.match(phone):
        raise INVALID_PHONE
    
    return phone


@router.get("/profile", response_model=dict)
def get_user_profile(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile."""
    return {
        "success": True,
        "data": {
            "id": str(current_user.id),
            "email": current_user.email,
            "name": current_user.name,
            "phone": current_user.phone,
            "country_code": current_user.country_code,
            "role": current_user.role
        }
    }


@router.patch("/profile", response_model=dict)
def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile."""
    # Validate phone if provided
    if profile_update.phone is not None:
        validated_phone = validate_phone(profile_update.phone)
        current_user.phone = validated_phone
    
    # Update name if provided
    if profile_update.name is not None:
        current_user.name = profile_update.name
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "success": True,
        "data": {
            "id": str(current_user.id),
            "email": current_user.email,
            "name": current_user.name,
            "phone": current_user.phone,
            "country_code": current_user.country_code,
            "role": current_user.role
        }
    }


@router.get("/export")
def export_user_data_endpoint(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
    redis_client: Optional[redis_lib.Redis] = Depends(get_redis)
):
    """Export all user data (GDPR Article 20)."""
    # Rate limit check
    rate_limit_key = f"export_rl:{current_user.id}"
    if redis_client and redis_client.exists(rate_limit_key):
        return JSONResponse(
            status_code=429,
            content={"detail": "export_rate_limit_exceeded"}
        )

    # Collect user data
    data = export_user_data(current_user.id, db)

    # Set rate limit key (24 hours)
    if redis_client:
        redis_client.setex(rate_limit_key, 86400, "1")

    # Return JSON file
    json_data = json.dumps(data, ensure_ascii=False, indent=2)

    return JSONResponse(
        content=json_data,
        media_type="application/json",
        headers={
            "Content-Disposition": 'attachment; filename="nevumo_export.json"',
            "Cache-Control": "no-store, no-cache, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )
