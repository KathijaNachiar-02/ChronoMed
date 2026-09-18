from fastapi import APIRouter
from app.services.database_service import get_events

router = APIRouter(
    prefix="/api/events",
    tags=["Events"]
)


@router.get("")
def list_events():
    return get_events()


@router.post("")
def create_event(event: dict):
    events = get_events()

    events.append(event)

    return {
        "message": "Event created successfully",
        "event": event
    }


@router.get("/{event_id}")
def get_event(event_id: str):
    events = get_events()

    event = next(
        (e for e in events if e["id"] == event_id),
        None
    )

    if event is None:
        return {
            "error": "Event not found"
        }

    return event