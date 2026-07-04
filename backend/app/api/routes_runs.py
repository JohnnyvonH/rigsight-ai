from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.api.routes_alerts import serialize_alert
from app.api.routes_readings import serialize_run
from app.database import get_db
from app.models import Alert, TestRun
from app.services.alerting import recalculate_rule_alerts_for_run

router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("")
def list_runs(
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    scenario: str | None = Query(default=None),
    status: str | None = Query(default=None),
    rig_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    query = select(TestRun)
    count_query = select(func.count()).select_from(TestRun)
    filters = []
    if scenario:
        filters.append(TestRun.scenario == scenario)
    if status:
        filters.append(TestRun.status == status)
    if rig_id:
        filters.append(TestRun.rig_id == rig_id)

    for condition in filters:
        query = query.where(condition)
        count_query = count_query.where(condition)

    runs = list(db.scalars(query.order_by(TestRun.started_at.desc()).offset(offset).limit(limit)))
    total_count = db.scalar(count_query)

    return {
        "runs": [serialize_run(run) for run in runs],
        "count": len(runs),
        "total_count": total_count or 0,
        "limit": limit,
        "offset": offset,
    }


@router.post("/{run_id}/alerts/recalculate")
def recalculate_run_alerts(run_id: int, db: Session = Depends(get_db)) -> dict[str, object]:
    run = db.get(TestRun, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    recalculate_rule_alerts_for_run(db, run)
    rule_alerts = list(
        db.scalars(
            select(Alert)
            .options(joinedload(Alert.reading), joinedload(Alert.run))
            .where(Alert.run_id == run.id, Alert.detection_source == "rules")
            .order_by(Alert.timestamp.desc(), Alert.id.desc())
            .limit(25)
        )
    )
    ml_count = db.scalar(
        select(func.count())
        .select_from(Alert)
        .where(Alert.run_id == run.id, Alert.detection_source == "ml")
    )

    return {
        "run": serialize_run(run),
        "rules_count": db.scalar(
            select(func.count())
            .select_from(Alert)
            .where(Alert.run_id == run.id, Alert.detection_source == "rules")
        )
        or 0,
        "ml_count": ml_count or 0,
        "alerts": [serialize_alert(alert) for alert in rule_alerts[:25]],
    }
