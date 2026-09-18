from fastapi import APIRouter

from app.services.database_service import get_patients

router = APIRouter(
    prefix="/api/patients",
    tags=["Patients"]
)


@router.get("")
def list_patients():
    return get_patients()

@router.post("")
def create_patient(patient: dict):
    patients = get_patients()

    patients.append(patient)

    return {
        "message": "Patient created successfully",
        "patient": patient
    }

@router.get("/{patient_id}")
def get_patient(patient_id: str):
    patients = get_patients()

    patient = next(
        (p for p in patients if p["id"] == patient_id),
        None
    )

    if patient is None:
        return {
            "error": "Patient not found"
        }

    return patient