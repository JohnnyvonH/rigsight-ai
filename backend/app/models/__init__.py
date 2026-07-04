"""SQLAlchemy models for synthetic rig telemetry."""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TestRun(Base):
    __tablename__ = "test_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    organization_id: Mapped[str] = mapped_column(String(80), nullable=False, default="demo-org")
    rig_id: Mapped[str] = mapped_column(String(80), nullable=False, default="synthetic-rig-01")
    scenario: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")

    readings: Mapped[list["Reading"]] = relationship(
        back_populates="run",
        cascade="all, delete-orphan",
    )
    alerts: Mapped[list["Alert"]] = relationship(
        back_populates="run",
        cascade="all, delete-orphan",
    )


class Reading(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("test_runs.id"), nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(String(80), nullable=False, default="demo-org")
    rig_id: Mapped[str] = mapped_column(String(80), nullable=False, default="synthetic-rig-01")
    source: Mapped[str] = mapped_column(String(40), nullable=False, default="synthetic")
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    phase: Mapped[str] = mapped_column(String(80), nullable=False)
    rpm: Mapped[float] = mapped_column(Float, nullable=False)
    torque_nm: Mapped[float] = mapped_column(Float, nullable=False)
    temperature_c: Mapped[float] = mapped_column(Float, nullable=False)
    vibration_mm_s: Mapped[float] = mapped_column(Float, nullable=False)
    current_a: Mapped[float] = mapped_column(Float, nullable=False)
    voltage_v: Mapped[float] = mapped_column(Float, nullable=False)
    pressure_bar: Mapped[float] = mapped_column(Float, nullable=False)
    fault_mode: Mapped[str | None] = mapped_column(String(80), nullable=True)

    run: Mapped[TestRun] = relationship(back_populates="readings")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="reading")


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("test_runs.id"), nullable=False, index=True)
    reading_id: Mapped[int] = mapped_column(ForeignKey("readings.id"), nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(String(80), nullable=False, default="demo-org")
    rig_id: Mapped[str] = mapped_column(String(80), nullable=False, default="synthetic-rig-01")
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(24), nullable=False)
    alert_type: Mapped[str] = mapped_column(String(80), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    detection_source: Mapped[str] = mapped_column(String(32), nullable=False)
    observed_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    threshold_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    anomaly_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    ml_is_anomaly: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    review_status: Mapped[str] = mapped_column(String(32), nullable=False, default="unreviewed")
    review_notes: Mapped[str] = mapped_column(Text, nullable=False, default="")
    assigned_to: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    reviewed_by: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    review_history: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    run: Mapped[TestRun] = relationship(back_populates="alerts")
    reading: Mapped[Reading] = relationship(back_populates="alerts")
