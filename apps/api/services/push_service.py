from pywebpush import webpush, WebPushException
from sqlalchemy.orm import Session
from models import PushSubscription
from config import settings
import json
import logging

logger = logging.getLogger(__name__)

def send_push_notification(
    db: Session,
    user_id: str,
    title: str,
    body: str,
    url: str = "/",
) -> int:
    """
    Send push notification to all subscriptions of a user.
    Returns count of successful sends.
    """
    subscriptions = db.query(PushSubscription).filter(
        PushSubscription.user_id == user_id
    ).all()

    if not subscriptions:
        return 0

    sent = 0
    failed_endpoints = []

    for sub in subscriptions:
        try:
            webpush(
                subscription_info={
                    "endpoint": sub.endpoint,
                    "keys": {
                        "p256dh": sub.p256dh,
                        "auth": sub.auth,
                    },
                },
                data=json.dumps({"title": title, "body": body, "url": url}),
                vapid_private_key=settings.vapid_private_key,
                vapid_claims={
                    "sub": f"mailto:{settings.vapid_claims_email}"
                },
            )
            sent += 1
        except WebPushException as e:
            status_code = getattr(e.response, "status_code", None)
            if status_code in (404, 410):
                failed_endpoints.append(sub.endpoint)
            else:
                logger.error(f"Push failed for endpoint {sub.endpoint}: {e}")

    # Remove expired/invalid subscriptions
    if failed_endpoints:
        db.query(PushSubscription).filter(
            PushSubscription.endpoint.in_(failed_endpoints)
        ).delete(synchronize_session=False)
        db.commit()

    return sent
