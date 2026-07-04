"""Optional local camera capture helpers."""

from dataclasses import dataclass

from app.config import settings


@dataclass(frozen=True)
class CameraStatus:
    enabled: bool
    status: str
    message: str
    device_index: int
    snapshot_available: bool


def get_camera_status() -> CameraStatus:
    if not settings.camera_enabled:
        return CameraStatus(
            enabled=False,
            status="disabled",
            message="Camera lab is disabled by default for the clean-room 1.0 demo.",
            device_index=settings.camera_device_index,
            snapshot_available=False,
        )

    try:
        import cv2  # type: ignore[import-not-found]
    except ImportError:
        return CameraStatus(
            enabled=True,
            status="unavailable",
            message="Camera lab is enabled, but OpenCV is not installed in this environment.",
            device_index=settings.camera_device_index,
            snapshot_available=False,
        )

    capture = cv2.VideoCapture(settings.camera_device_index)
    is_open = bool(capture.isOpened())
    capture.release()

    return CameraStatus(
        enabled=True,
        status="available" if is_open else "unavailable",
        message="Local camera is available." if is_open else "No local camera device is available.",
        device_index=settings.camera_device_index,
        snapshot_available=is_open,
    )


def capture_snapshot_jpeg() -> bytes | None:
    status = get_camera_status()
    if not status.snapshot_available:
        return None

    import cv2  # type: ignore[import-not-found]

    capture = cv2.VideoCapture(settings.camera_device_index)
    ok, frame = capture.read()
    capture.release()
    if not ok:
        return None

    encoded, buffer = cv2.imencode(".jpg", frame)
    if not encoded:
        return None
    return bytes(buffer)
