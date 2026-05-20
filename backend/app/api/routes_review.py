from fastapi import APIRouter

router = APIRouter(prefix="/review", tags=["review"])


@router.get("/queue")
def review_queue() -> dict[str, object]:
    return {
        "items": [],
        "message": "Human review workflow arrives in Milestone 6.",
    }
