from fastapi import APIRouter

router = APIRouter(
    prefix="/api/evidence",
    tags=["Evidence"]
)

evidence = []


@router.get("")
def list_evidence():
    return evidence


@router.post("")
def create_evidence(item: dict):
    evidence.append(item)

    return {
        "message": "Evidence created successfully",
        "evidence": item
    }


@router.get("/{evidence_id}")
def get_evidence(evidence_id: str):
    item = next(
        (entry for entry in evidence if entry["id"] == evidence_id),
        None
    )

    if item is None:
        return {
            "error": "Evidence not found"
        }

    return item