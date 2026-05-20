from fastapi import APIRouter

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("")
def list_alerts() -> dict[str, object]:
    return {
        "alerts": [],
        "message": "Alert generation arrives with anomaly detection milestones.",
    }
