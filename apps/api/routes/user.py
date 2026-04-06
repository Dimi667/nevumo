import re
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from dependencies import get_current_user, get_db
from exceptions import INVALID_PHONE

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
