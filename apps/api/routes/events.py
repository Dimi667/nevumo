from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from models import LeadEvent
from schemas import EventCreate, EventCreatedResponse

router = APIRouter(prefix="/api/v1", tags=["events"])


@router.post("/events", response_model=EventCreatedResponse)
async def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
) -> EventCreatedResponse:
    event = LeadEvent(
        lead_id=payload.lead_id,
        event_type=payload.event_type,
        event_metadata=payload.metadata,
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    return EventCreatedResponse(data={"event_id": str(event.id)})
