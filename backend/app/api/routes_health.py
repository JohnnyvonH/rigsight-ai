from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Alert, Reading, TestRun

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "rigsight-api",
        "version": settings.app_version,
        "environment": settings.app_env,
        "timestamp": datetime.now(UTC).isoformat(),
    }


@router.get("/ready")
def readiness(db: Session = Depends(get_db)) -> dict[str, object]:
    run_count = db.scalar(select(func.count()).select_from(TestRun)) or 0
    return {
        "status": "ready",
        "database": "ok",
        "run_count": run_count,
        "timestamp": datetime.now(UTC).isoformat(),
    }


@router.get("/metrics")
def metrics(db: Session = Depends(get_db)) -> dict[str, object]:
    return {
        "runs_total": db.scalar(select(func.count()).select_from(TestRun)) or 0,
        "readings_total": db.scalar(select(func.count()).select_from(Reading)) or 0,
        "alerts_total": db.scalar(select(func.count()).select_from(Alert)) or 0,
        "unreviewed_alerts": db.scalar(
            select(func.count()).select_from(Alert).where(Alert.review_status == "unreviewed")
        )
        or 0,
        "environment": settings.app_env,
        "version": settings.app_version,
    }
