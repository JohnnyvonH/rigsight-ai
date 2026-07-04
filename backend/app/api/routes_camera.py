from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.services.camera_capture import capture_snapshot_jpeg, get_camera_status

router = APIRouter(prefix="/camera", tags=["camera"])


@router.get("/status")
def camera_status() -> dict[str, object]:
    status = get_camera_status()
    return {
        "enabled": status.enabled,
        "status": status.status,
        "message": status.message,
        "device_index": status.device_index,
        "snapshot_available": status.snapshot_available,
    }


@router.get("/snapshot")
def camera_snapshot() -> Response:
    snapshot = capture_snapshot_jpeg()
    if snapshot is None:
        raise HTTPException(status_code=503, detail="Camera snapshot unavailable")
    return Response(content=snapshot, media_type="image/jpeg")
