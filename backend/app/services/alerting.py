"""Alert persistence helpers for synthetic telemetry."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Alert, Reading, TestRun
from app.services.anomaly_detection import detect_ml_alerts, detect_rule_alerts


def ensure_alerts_for_run(db: Session, run: TestRun) -> list[Alert]:
    existing_alerts = list(db.scalars(select(Alert).where(Alert.run_id == run.id)))
    if existing_alerts:
        return existing_alerts

    readings = list(
        db.scalars(select(Reading).where(Reading.run_id == run.id).order_by(Reading.timestamp.asc()))
    )
    candidates = [*detect_rule_alerts(readings), *detect_ml_alerts(readings)]
    alerts: list[Alert] = []
    seen: set[tuple[int, str, str]] = set()

    for candidate in candidates:
        key = (candidate.reading.id, candidate.detection_source, candidate.alert_type)
        if key in seen:
            continue
        seen.add(key)

        alert = Alert(
            run_id=run.id,
            reading_id=candidate.reading.id,
            organization_id=run.organization_id,
            rig_id=run.rig_id,
            timestamp=candidate.reading.timestamp,
            severity=candidate.severity,
            alert_type=candidate.alert_type,
            title=candidate.title,
            message=candidate.message,
            detection_source=candidate.detection_source,
            observed_value=candidate.observed_value,
            threshold_value=candidate.threshold_value,
            anomaly_score=candidate.anomaly_score,
            ml_is_anomaly=1 if candidate.ml_is_anomaly else 0,
        )
        db.add(alert)
        alerts.append(alert)

    db.commit()
    return alerts
