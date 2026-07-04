"""Alert persistence helpers for synthetic telemetry."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Alert, Reading, TestRun
from app.services.anomaly_detection import detect_ml_alerts, detect_rule_alerts
from app.services.thresholds import get_threshold_profile


def build_alert_from_candidate(
    run: TestRun,
    candidate,
    review_state: dict[str, object] | None = None,
) -> Alert:
    state = review_state or {}
    return Alert(
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
        explanation=candidate.explanation,
        recommended_action=candidate.recommended_action,
        triggered_metric=candidate.triggered_metric,
        expected_range=candidate.expected_range,
        actual_value=candidate.actual_value,
        review_status=str(state.get("review_status", "unreviewed")),
        review_notes=str(state.get("review_notes", "")),
        assigned_to=str(state.get("assigned_to", "")),
        reviewed_by=str(state.get("reviewed_by", "")),
        review_history=str(state.get("review_history", "[]")),
        reviewed_at=state.get("reviewed_at"),
    )


def ensure_alerts_for_run(db: Session, run: TestRun) -> list[Alert]:
    existing_alerts = list(db.scalars(select(Alert).where(Alert.run_id == run.id)))
    if existing_alerts:
        return existing_alerts

    readings = list(
        db.scalars(select(Reading).where(Reading.run_id == run.id).order_by(Reading.timestamp.asc()))
    )
    thresholds, _ = get_threshold_profile(
        db, organization_id=run.organization_id, rig_id=run.rig_id
    )
    candidates = [*detect_rule_alerts(readings, thresholds), *detect_ml_alerts(readings)]
    alerts: list[Alert] = []
    seen: set[tuple[int, str, str]] = set()

    for candidate in candidates:
        key = (candidate.reading.id, candidate.detection_source, candidate.alert_type)
        if key in seen:
            continue
        seen.add(key)

        alert = build_alert_from_candidate(run, candidate)
        db.add(alert)
        alerts.append(alert)

    db.commit()
    return alerts


def recalculate_rule_alerts_for_run(db: Session, run: TestRun) -> list[Alert]:
    existing_rule_alerts = list(
        db.scalars(
            select(Alert).where(Alert.run_id == run.id, Alert.detection_source == "rules")
        )
    )
    review_state_by_key = {
        (alert.reading_id, alert.alert_type): {
            "review_status": alert.review_status,
            "review_notes": alert.review_notes,
            "assigned_to": alert.assigned_to,
            "reviewed_by": alert.reviewed_by,
            "review_history": alert.review_history,
            "reviewed_at": alert.reviewed_at,
        }
        for alert in existing_rule_alerts
    }

    for alert in existing_rule_alerts:
        db.delete(alert)
    db.flush()

    readings = list(
        db.scalars(select(Reading).where(Reading.run_id == run.id).order_by(Reading.timestamp.asc()))
    )
    thresholds, _ = get_threshold_profile(
        db, organization_id=run.organization_id, rig_id=run.rig_id
    )
    candidates = detect_rule_alerts(readings, thresholds)
    alerts: list[Alert] = []
    seen: set[tuple[int, str, str]] = set()

    for candidate in candidates:
        key = (candidate.reading.id, candidate.detection_source, candidate.alert_type)
        if key in seen:
            continue
        seen.add(key)
        review_key = (candidate.reading.id, candidate.alert_type)
        alert = build_alert_from_candidate(run, candidate, review_state_by_key.get(review_key))
        db.add(alert)
        alerts.append(alert)

    db.commit()
    return alerts
