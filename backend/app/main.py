from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.documents import router as documents_router
from app.routes.patients import router as patients_router
from app.routes.timeline import router as timeline_router
from app.routes.events import router as events_router

from app.services.database_service import (
    get_documents,
    get_patients,
    get_events,
)

app = FastAPI(
    title="ChronoMed API",
    description="Medical Document Intelligence and Patient Timeline API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router)
app.include_router(patients_router)
app.include_router(timeline_router)
app.include_router(events_router)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ChronoMed API",
    }


@app.get("/api/system/status")
def system_status():
    return {
        "backend": "online",
        "ai": "not_connected",
        "database": "not_connected",
    }


@app.get("/api/stats")
def get_stats():
    documents = get_documents()
    patients = get_patients()
    events = get_events()

    return {
        "patients": len(patients),
        "documents": len(documents),
        "events": len(events),
        "conflicts": 0,
    }