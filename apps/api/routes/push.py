from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from apps.api.database import get_db
from apps.api.models import PushSubscription, User
from apps.api.auth import get_current_user
from apps.api.config import settings
import uuid

router = APIRouter(prefix="/push", tags=["push"])


class PushSubscribeRequest(BaseModel):
    endpoint: str
    p256dh: str
    auth: str
    device_info: str | None = None


@router.get("/vapid-public-key")
def get_vapid_public_key() -> dict:
    return {"public_key": settings.vapid_public_key}


@router.post("/subscribe", status_code=201)
def subscribe(
    payload: PushSubscribeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    existing = db.query(PushSubscription).filter(
        PushSubscription.endpoint == payload.endpoint
    ).first()

    if existing:
        existing.p256dh = payload.p256dh
        existing.auth = payload.auth
        existing.device_info = payload.device_info
        db.commit()
        return {"status": "updated"}

    sub = PushSubscription(
        id=uuid.uuid4(),
        user_id=current_user.id,
        endpoint=payload.endpoint,
        p256dh=payload.p256dh,
        auth=payload.auth,
        device_info=payload.device_info,
    )
    db.add(sub)
    db.commit()
    return {"status": "subscribed"}


@router.delete("/unsubscribe")
def unsubscribe(
    payload: PushSubscribeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    db.query(PushSubscription).filter(
        PushSubscription.endpoint == payload.endpoint,
        PushSubscription.user_id == current_user.id,
    ).delete()
    db.commit()
    return {"status": "unsubscribed"}
