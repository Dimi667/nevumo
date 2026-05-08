import hashlib
import uuid
from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.orm import Session

from apps.api.database import get_db
from apps.api.models import ConsentLog
from apps.api.schemas import ConsentLogCreate, ConsentLogResponse
from apps.api.dependencies import get_optional_current_user
from apps.api.models import User

router = APIRouter()


@router.post("/consent", response_model=ConsentLogResponse)
def create_consent_log(
    consent_data: ConsentLogCreate,
    request: Request,
    x_session_id: str | None = Header(None),
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    # Get client IP
    client_ip = request.client.host if request.client else "unknown"
    
    # Handle X-Forwarded-For header if present
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    
    # Generate session hash from header or create new UUID
    if x_session_id:
        session_hash = hashlib.sha256(x_session_id.encode()).hexdigest()
    else:
        session_hash = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    
    # Hash IP for privacy
    ip_hash = hashlib.sha256(client_ip.encode()).hexdigest()
    
    # Create consent log
    consent_log = ConsentLog(
        user_id=current_user.id if current_user else None,
        session_hash=session_hash,
        ip_hash=ip_hash,
        categories=consent_data.categories.model_dump(),
        policy_version=consent_data.policy_version,
    )
    
    db.add(consent_log)
    db.commit()
    db.refresh(consent_log)
    
    return consent_log
