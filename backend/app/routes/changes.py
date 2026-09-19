from fastapi import APIRouter

router = APIRouter(
    prefix="/api/changes",
    tags=["What Changed"]
)

changes = []


@router.get("")
def list_changes():
    return changes


@router.post("")
def create_change(change: dict):
    changes.append(change)

    return {
        "message": "Change created successfully",
        "change": change
    }


@router.get("/{change_id}")
def get_change(change_id: str):
    change = next(
        (item for item in changes if item["id"] == change_id),
        None
    )

    if change is None:
        return {
            "error": "Change not found"
        }

    return change