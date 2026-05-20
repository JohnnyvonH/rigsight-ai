from datetime import UTC, datetime

from fastapi import APIRouter

from app.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "rigsight-api",
        "environment": settings.app_env,
        "timestamp": datetime.now(UTC).isoformat(),
    }
