from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.routes_readings import serialize_run
from app.database import get_db
from app.models import Alert, Reading
from app.services.demo_data import DEFAULT_SCENARIO, create_demo_run, reset_demo_data
from app.services.simulator import SCENARIOS

router = APIRouter(prefix="/demo", tags=["demo"])


class DemoSeedRequest(BaseModel):
    scenario: str = DEFAULT_SCENARIO


def serialize_scenario_catalog() -> list[dict[str, object]]:
    return [
        {
            "key": scenario.key,
            "name": scenario.name,
            "description": scenario.description,
            "expected_faults": list(scenario.expected_faults),
        }
        for scenario in SCENARIOS.values()
    ]


def demo_response(db: Session, run_id: int) -> dict[str, object]:
    reading_count = db.scalar(select(func.count()).select_from(Reading).where(Reading.run_id == run_id))
    alert_count = db.scalar(select(func.count()).select_from(Alert).where(Alert.run_id == run_id))

    return {
        "run_id": run_id,
        "readings_created": reading_count or 0,
        "alerts_created": alert_count or 0,
        "scenarios": serialize_scenario_catalog(),
    }


@router.get("/scenarios")
def list_demo_scenarios() -> dict[str, object]:
    return {"scenarios": serialize_scenario_catalog()}


@router.post("/seed")
def seed_demo(payload: DemoSeedRequest, db: Session = Depends(get_db)) -> dict[str, object]:
    run = create_demo_run(db, scenario=payload.scenario)
    return {"run": serialize_run(run), **demo_response(db, run.id)}


@router.post("/reset")
def reset_demo(payload: DemoSeedRequest, db: Session = Depends(get_db)) -> dict[str, object]:
    run = reset_demo_data(db, scenario=payload.scenario)
    return {"run": serialize_run(run), **demo_response(db, run.id)}
