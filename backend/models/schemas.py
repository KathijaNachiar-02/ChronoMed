from pydantic import BaseModel
from typing import Optional


class DocumentResponse(BaseModel):
    id: str
    filename: str
    status: str
    patient_id: Optional[str] = None


class PatientResponse(BaseModel):
    id: str
    name: str


class EventResponse(BaseModel):
    id: str
    patient_id: str
    event_type: str
    date: str
    description: str