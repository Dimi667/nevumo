from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from apps.api.dependencies import get_db
from apps.api.models import PageEvent
from apps.api.schemas import PageEventCreate

router = APIRouter(prefix="/api/v1", tags=["page-events"])


@router.post("/page-events")
async def create_page_event(
    event: PageEventCreate,
    request: Request,
    db: Session = Depends(get_db),
) -> dict:
    db_event = PageEvent(
        event_type=event.event_type,
        page=event.page,
        event_metadata=event.metadata,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent", ""),
    )
    db.add(db_event)
    db.commit()
    return {"success": True}
