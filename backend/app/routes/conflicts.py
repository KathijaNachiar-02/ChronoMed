from fastapi import APIRouter

router = APIRouter(
    prefix="/api/conflicts",
    tags=["Conflicts"]
)

conflicts = []


@router.get("")
def list_conflicts():
    return conflicts


@router.post("")
def create_conflict(conflict: dict):
    conflicts.append(conflict)

    return {
        "message": "Conflict created successfully",
        "conflict": conflict
    }


@router.get("/{conflict_id}")
def get_conflict(conflict_id: str):
    conflict = next(
        (item for item in conflicts if item["id"] == conflict_id),
        None
    )

    if conflict is None:
        return {
            "error": "Conflict not found"
        }

    return conflict