from dataclasses import asdict, dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AlertThreshold


@dataclass(frozen=True)
class ThresholdProfile:
    organization_id: str = "demo-org"
    rig_id: str = "synthetic-rig-01"
    temperature_high_c: float = 82.0
    temperature_critical_c: float = 90.0
    temperature_drift_c: float = 3.0
    vibration_high_mm_s: float = 4.0
    rpm_dropout: float = 50.0
    torque_dropout_nm: float = 5.0
    current_high_a: float = 38.0
    voltage_low_v: float = 394.0


THRESHOLD_FIELDS = (
    "temperature_high_c",
    "temperature_critical_c",
    "temperature_drift_c",
    "vibration_high_mm_s",
    "rpm_dropout",
    "torque_dropout_nm",
    "current_high_a",
    "voltage_low_v",
)


def default_threshold_profile(
    *, organization_id: str = "demo-org", rig_id: str = "synthetic-rig-01"
) -> ThresholdProfile:
    return ThresholdProfile(organization_id=organization_id, rig_id=rig_id)


def serialize_threshold_profile(profile: ThresholdProfile, *, persisted: bool) -> dict[str, object]:
    return {**asdict(profile), "persisted": persisted}


def threshold_model_to_profile(model: AlertThreshold) -> ThresholdProfile:
    return ThresholdProfile(
        organization_id=model.organization_id,
        rig_id=model.rig_id,
        temperature_high_c=model.temperature_high_c,
        temperature_critical_c=model.temperature_critical_c,
        temperature_drift_c=model.temperature_drift_c,
        vibration_high_mm_s=model.vibration_high_mm_s,
        rpm_dropout=model.rpm_dropout,
        torque_dropout_nm=model.torque_dropout_nm,
        current_high_a=model.current_high_a,
        voltage_low_v=model.voltage_low_v,
    )


def get_threshold_model(
    db: Session, *, organization_id: str, rig_id: str
) -> AlertThreshold | None:
    return db.scalar(
        select(AlertThreshold).where(
            AlertThreshold.organization_id == organization_id,
            AlertThreshold.rig_id == rig_id,
        )
    )


def get_threshold_profile(
    db: Session, *, organization_id: str, rig_id: str
) -> tuple[ThresholdProfile, bool]:
    model = get_threshold_model(db, organization_id=organization_id, rig_id=rig_id)
    if model is None:
        return default_threshold_profile(organization_id=organization_id, rig_id=rig_id), False
    return threshold_model_to_profile(model), True


def upsert_threshold_profile(
    db: Session,
    *,
    organization_id: str,
    rig_id: str,
    values: dict[str, float],
) -> tuple[ThresholdProfile, bool]:
    model = get_threshold_model(db, organization_id=organization_id, rig_id=rig_id)
    created = model is None
    if model is None:
        model = AlertThreshold(organization_id=organization_id, rig_id=rig_id)
        db.add(model)

    for field_name in THRESHOLD_FIELDS:
        if field_name in values:
            setattr(model, field_name, values[field_name])

    db.commit()
    db.refresh(model)
    return threshold_model_to_profile(model), created


def reset_threshold_profile(
    db: Session, *, organization_id: str, rig_id: str
) -> ThresholdProfile:
    model = get_threshold_model(db, organization_id=organization_id, rig_id=rig_id)
    if model is not None:
        db.delete(model)
        db.commit()
    return default_threshold_profile(organization_id=organization_id, rig_id=rig_id)
