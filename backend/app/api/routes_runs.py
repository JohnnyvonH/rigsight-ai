from fastapi import APIRouter

router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("")
def list_runs() -> dict[str, object]:
    return {
        "runs": [],
        "message": "Test-run history arrives with synthetic ingestion.",
    }
