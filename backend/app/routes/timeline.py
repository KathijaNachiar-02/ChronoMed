from fastapi import APIRouter

from app.services.database_service import get_events

router = APIRouter(
    prefix="/api/patients",
    tags=["Timeline"]
)


@router.get("/{patient_id}/timeline")
def get_patient_timeline(patient_id: str):
    events = get_events()

    patient_events = [
        event
        for event in events
        if event["patient_id"] == patient_id
    ]

    return {
        "patient_id": patient_id,
        "timeline": patient_events
    }