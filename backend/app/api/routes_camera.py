from fastapi import APIRouter

router = APIRouter(prefix="/camera", tags=["camera"])


@router.get("/status")
def camera_status() -> dict[str, object]:
    return {
        "enabled": False,
        "status": "disabled",
        "message": "Camera lab is optional and arrives in Milestone 7.",
    }
