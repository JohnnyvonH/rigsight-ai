from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.api.routes_readings import serialize_reading, serialize_run
from app.database import get_db
from app.models import Alert

router = APIRouter(prefix="/alerts", tags=["alerts"])


def serialize_alert(alert: Alert) -> dict[str, object]:
    return {
        "id": alert.id,
        "run_id": alert.run_id,
        "reading_id": alert.reading_id,
        "organization_id": alert.organization_id,
        "rig_id": alert.rig_id,
        "timestamp": alert.timestamp.isoformat(),
        "severity": alert.severity,
        "alert_type": alert.alert_type,
        "title": alert.title,
        "message": alert.message,
        "detection_source": alert.detection_source,
        "observed_value": alert.observed_value,
        "threshold_value": alert.threshold_value,
        "anomaly_score": alert.anomaly_score,
        "ml_is_anomaly": bool(alert.ml_is_anomaly),
        "review_status": alert.review_status,
        "review_notes": alert.review_notes,
        "assigned_to": alert.assigned_to,
        "reviewed_by": alert.reviewed_by,
        "review_history": alert.review_history,
        "reviewed_at": alert.reviewed_at.isoformat() if alert.reviewed_at else None,
        "reading": serialize_reading(alert.reading),
        "run": serialize_run(alert.run),
    }


@router.get("")
def list_alerts(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    run_id: int | None = Query(default=None),
    rig_id: str | None = Query(default=None),
    severity: str | None = Query(default=None),
    detection_source: str | None = Query(default=None),
    review_status: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    query = select(Alert).options(joinedload(Alert.reading), joinedload(Alert.run))
    count_query = select(func.count()).select_from(Alert)

    filters = []
    if run_id is not None:
        filters.append(Alert.run_id == run_id)
    if rig_id:
        filters.append(Alert.rig_id == rig_id)
    if severity:
        filters.append(Alert.severity == severity)
    if detection_source:
        filters.append(Alert.detection_source == detection_source)
    if review_status:
        filters.append(Alert.review_status == review_status)

    for condition in filters:
        query = query.where(condition)
        count_query = count_query.where(condition)

    alerts = list(
        db.scalars(
            query.order_by(Alert.timestamp.desc(), Alert.id.desc()).offset(offset).limit(limit)
        )
    )
    total_count = db.scalar(count_query)

    unreviewed_count = db.scalar(
        select(func.count()).select_from(Alert).where(Alert.review_status == "unreviewed")
    )
    rules_count = db.scalar(
        select(func.count()).select_from(Alert).where(Alert.detection_source == "rules")
    )
    ml_count = db.scalar(select(func.count()).select_from(Alert).where(Alert.detection_source == "ml"))

    return {
        "alerts": [serialize_alert(alert) for alert in alerts],
        "count": len(alerts),
        "total_count": total_count or 0,
        "limit": limit,
        "offset": offset,
        "summary": {
            "unreviewed_count": unreviewed_count or 0,
            "rules_count": rules_count or 0,
            "ml_count": ml_count or 0,
        },
    }
