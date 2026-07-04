"""Demo data creation for the local telemetry sandbox."""

from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Reading, TestRun
from app.services.alerting import ensure_alerts_for_run
from app.services.simulator import generate_demo_readings, get_scenario_definition


DEFAULT_SCENARIO = "baseline-with-seeded-faults"


def ensure_demo_data(db: Session) -> TestRun:
    existing_run = db.scalar(select(TestRun).order_by(TestRun.started_at.desc()).limit(1))
    reading_count = db.scalar(select(func.count()).select_from(Reading)) or 0

    if existing_run and reading_count > 0:
        ensure_alerts_for_run(db, existing_run)
        return existing_run

    return create_demo_run(db, scenario=DEFAULT_SCENARIO)


def create_demo_run(db: Session, *, scenario: str = DEFAULT_SCENARIO) -> TestRun:
    definition = get_scenario_definition(scenario)
    run = TestRun(
        name=definition.name,
        organization_id="demo-org",
        rig_id="synthetic-rig-01",
        scenario=definition.key,
        status="active",
        started_at=datetime.now(UTC).replace(microsecond=0) - timedelta(minutes=60),
        description=definition.description,
    )
    db.add(run)
    db.flush()

    for synthetic in generate_demo_readings(scenario=definition.key):
        db.add(
            Reading(
                run_id=run.id,
                organization_id=run.organization_id,
                rig_id=run.rig_id,
                source="synthetic",
                timestamp=synthetic.timestamp,
                phase=synthetic.phase,
                rpm=synthetic.rpm,
                torque_nm=synthetic.torque_nm,
                temperature_c=synthetic.temperature_c,
                vibration_mm_s=synthetic.vibration_mm_s,
                current_a=synthetic.current_a,
                voltage_v=synthetic.voltage_v,
                pressure_bar=synthetic.pressure_bar,
                fault_mode=synthetic.fault_mode,
            )
        )

    db.commit()
    db.refresh(run)
    ensure_alerts_for_run(db, run)
    return run


def reset_demo_data(db: Session, *, scenario: str = DEFAULT_SCENARIO) -> TestRun:
    for run in db.scalars(select(TestRun)):
        db.delete(run)
    db.commit()
    return create_demo_run(db, scenario=scenario)
