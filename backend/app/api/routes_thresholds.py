from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.auth import PilotContext, get_pilot_context
from app.database import get_db
from app.services.thresholds import (
    THRESHOLD_FIELDS,
    get_threshold_profile,
    reset_threshold_profile,
    serialize_threshold_profile,
    upsert_threshold_profile,
)

router = APIRouter(prefix="/thresholds", tags=["thresholds"])


class ThresholdUpdate(BaseModel):
    rig_id: str = Field(default="synthetic-rig-01", max_length=80)
    temperature_high_c: float | None = Field(default=None, gt=0)
    temperature_critical_c: float | None = Field(default=None, gt=0)
    temperature_drift_c: float | None = Field(default=None, gt=0)
    vibration_high_mm_s: float | None = Field(default=None, gt=0)
    rpm_dropout: float | None = Field(default=None, ge=0)
    torque_dropout_nm: float | None = Field(default=None, ge=0)
    current_high_a: float | None = Field(default=None, gt=0)
    voltage_low_v: float | None = Field(default=None, gt=0)


class ThresholdReset(BaseModel):
    rig_id: str = Field(default="synthetic-rig-01", max_length=80)


@router.get("")
def read_thresholds(
    rig_id: str = Query(default="synthetic-rig-01"),
    context: PilotContext = Depends(get_pilot_context),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    profile, persisted = get_threshold_profile(
        db, organization_id=context.organization_id, rig_id=rig_id
    )
    return {"thresholds": serialize_threshold_profile(profile, persisted=persisted)}


@router.patch("")
def update_thresholds(
    payload: ThresholdUpdate,
    context: PilotContext = Depends(get_pilot_context),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    values = {
        field_name: value
        for field_name in THRESHOLD_FIELDS
        if (value := getattr(payload, field_name)) is not None
    }
    profile, created = upsert_threshold_profile(
        db,
        organization_id=context.organization_id,
        rig_id=payload.rig_id,
        values=values,
    )
    return {
        "thresholds": serialize_threshold_profile(profile, persisted=True),
        "created": created,
    }


@router.post("/reset")
def reset_thresholds(
    payload: ThresholdReset,
    context: PilotContext = Depends(get_pilot_context),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    profile = reset_threshold_profile(
        db, organization_id=context.organization_id, rig_id=payload.rig_id
    )
    return {"thresholds": serialize_threshold_profile(profile, persisted=False)}
