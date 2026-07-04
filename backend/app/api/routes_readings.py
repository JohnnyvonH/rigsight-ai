from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.api.auth import PilotContext, get_pilot_context
from app.config import settings
from app.database import get_db
from app.models import Reading, TestRun
from app.services.alerting import ensure_alerts_for_run

router = APIRouter(prefix="/readings", tags=["readings"])


class IngestReading(BaseModel):
    timestamp: datetime
    phase: str = "Imported"
    rpm: float
    torque_nm: float
    temperature_c: float
    vibration_mm_s: float
    current_a: float
    voltage_v: float
    pressure_bar: float
    fault_mode: str | None = None


class IngestRunRequest(BaseModel):
    name: str = Field(default="Customer telemetry import", max_length=120)
    rig_id: str = Field(default="pilot-rig-01", max_length=80)
    description: str = Field(default="Pilot telemetry import", max_length=500)
    readings: list[IngestReading] = Field(min_length=1, max_length=1000)


def serialize_run(run: TestRun) -> dict[str, object]:
    return {
        "id": run.id,
        "organization_id": run.organization_id,
        "rig_id": run.rig_id,
        "name": run.name,
        "scenario": run.scenario,
        "status": run.status,
        "started_at": run.started_at.isoformat(),
        "ended_at": run.ended_at.isoformat() if run.ended_at else None,
        "description": run.description,
    }


def serialize_reading(reading: Reading) -> dict[str, object]:
    return {
        "id": reading.id,
        "run_id": reading.run_id,
        "organization_id": reading.organization_id,
        "rig_id": reading.rig_id,
        "source": reading.source,
        "timestamp": reading.timestamp.isoformat(),
        "phase": reading.phase,
        "rpm": reading.rpm,
        "torque_nm": reading.torque_nm,
        "temperature_c": reading.temperature_c,
        "vibration_mm_s": reading.vibration_mm_s,
        "current_a": reading.current_a,
        "voltage_v": reading.voltage_v,
        "pressure_bar": reading.pressure_bar,
        "fault_mode": reading.fault_mode,
    }


@router.get("/latest")
def latest_readings(db: Session = Depends(get_db)) -> dict[str, object]:
    reading = db.scalar(
        select(Reading).options(joinedload(Reading.run)).order_by(Reading.timestamp.desc()).limit(1)
    )

    if reading is None:
        return {"reading": None, "run": None}

    return {
        "reading": serialize_reading(reading),
        "run": serialize_run(reading.run),
    }


@router.get("/history")
def readings_history(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    run_id: int | None = Query(default=None),
    rig_id: str | None = Query(default=None),
    fault_only: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    query = select(Reading)
    if run_id is not None:
        query = query.where(Reading.run_id == run_id)
    if rig_id:
        query = query.where(Reading.rig_id == rig_id)
    if fault_only:
        query = query.where(Reading.fault_mode.is_not(None))

    newest_readings = list(db.scalars(query.order_by(Reading.timestamp.desc()).offset(offset).limit(limit)))
    readings = list(reversed(newest_readings))

    return {
        "readings": [serialize_reading(reading) for reading in readings],
        "count": len(readings),
        "limit": limit,
        "offset": offset,
    }


@router.post("/ingest")
def ingest_readings(
    payload: IngestRunRequest,
    context: PilotContext = Depends(get_pilot_context),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    if not settings.telemetry_upload_enabled:
        raise HTTPException(status_code=403, detail="Telemetry upload is disabled")

    first_reading = payload.readings[0]
    last_reading = payload.readings[-1]
    run = TestRun(
        name=payload.name,
        organization_id=context.organization_id,
        rig_id=payload.rig_id,
        scenario="customer-import",
        status="imported",
        started_at=first_reading.timestamp,
        ended_at=last_reading.timestamp,
        description=payload.description,
    )
    db.add(run)
    db.flush()

    for incoming in payload.readings:
        db.add(
            Reading(
                run_id=run.id,
                organization_id=context.organization_id,
                rig_id=payload.rig_id,
                source="import",
                timestamp=incoming.timestamp,
                phase=incoming.phase,
                rpm=incoming.rpm,
                torque_nm=incoming.torque_nm,
                temperature_c=incoming.temperature_c,
                vibration_mm_s=incoming.vibration_mm_s,
                current_a=incoming.current_a,
                voltage_v=incoming.voltage_v,
                pressure_bar=incoming.pressure_bar,
                fault_mode=incoming.fault_mode,
            )
        )

    db.commit()
    db.refresh(run)
    alerts = ensure_alerts_for_run(db, run)

    return {
        "run": serialize_run(run),
        "readings_created": len(payload.readings),
        "alerts_created": len(alerts),
        "organization": {
            "id": context.organization_id,
            "name": context.organization_name,
            "actor": context.actor,
            "role": context.role,
        },
    }
