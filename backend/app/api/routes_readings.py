from fastapi import APIRouter

router = APIRouter(prefix="/readings", tags=["readings"])


@router.get("/latest")
def latest_readings() -> dict[str, object]:
    return {
        "readings": [],
        "message": "Synthetic readings arrive in Milestone 2.",
    }


@router.get("/history")
def readings_history() -> dict[str, object]:
    return {
        "readings": [],
        "message": "Time-windowed reading history arrives in Milestone 2.",
    }
