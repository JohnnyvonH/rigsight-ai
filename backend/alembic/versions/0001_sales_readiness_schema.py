"""sales readiness schema

Revision ID: 0001_sales_readiness
Revises:
Create Date: 2026-07-04
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_sales_readiness"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "test_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("organization_id", sa.String(length=80), nullable=False, server_default="demo-org"),
        sa.Column("rig_id", sa.String(length=80), nullable=False, server_default="synthetic-rig-01"),
        sa.Column("scenario", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="active"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
    )
    op.create_index("ix_test_runs_id", "test_runs", ["id"])

    op.create_table(
        "readings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("test_runs.id"), nullable=False),
        sa.Column("organization_id", sa.String(length=80), nullable=False, server_default="demo-org"),
        sa.Column("rig_id", sa.String(length=80), nullable=False, server_default="synthetic-rig-01"),
        sa.Column("source", sa.String(length=40), nullable=False, server_default="synthetic"),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("phase", sa.String(length=80), nullable=False),
        sa.Column("rpm", sa.Float(), nullable=False),
        sa.Column("torque_nm", sa.Float(), nullable=False),
        sa.Column("temperature_c", sa.Float(), nullable=False),
        sa.Column("vibration_mm_s", sa.Float(), nullable=False),
        sa.Column("current_a", sa.Float(), nullable=False),
        sa.Column("voltage_v", sa.Float(), nullable=False),
        sa.Column("pressure_bar", sa.Float(), nullable=False),
        sa.Column("fault_mode", sa.String(length=80), nullable=True),
    )
    op.create_index("ix_readings_id", "readings", ["id"])
    op.create_index("ix_readings_run_id", "readings", ["run_id"])
    op.create_index("ix_readings_timestamp", "readings", ["timestamp"])

    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("test_runs.id"), nullable=False),
        sa.Column("reading_id", sa.Integer(), sa.ForeignKey("readings.id"), nullable=False),
        sa.Column("organization_id", sa.String(length=80), nullable=False, server_default="demo-org"),
        sa.Column("rig_id", sa.String(length=80), nullable=False, server_default="synthetic-rig-01"),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("severity", sa.String(length=24), nullable=False),
        sa.Column("alert_type", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("detection_source", sa.String(length=32), nullable=False),
        sa.Column("observed_value", sa.Float(), nullable=True),
        sa.Column("threshold_value", sa.Float(), nullable=True),
        sa.Column("anomaly_score", sa.Float(), nullable=True),
        sa.Column("ml_is_anomaly", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("explanation", sa.Text(), nullable=False, server_default=""),
        sa.Column("recommended_action", sa.Text(), nullable=False, server_default=""),
        sa.Column("triggered_metric", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("expected_range", sa.String(length=120), nullable=False, server_default=""),
        sa.Column("actual_value", sa.String(length=120), nullable=False, server_default=""),
        sa.Column("review_status", sa.String(length=32), nullable=False, server_default="unreviewed"),
        sa.Column("review_notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("assigned_to", sa.String(length=120), nullable=False, server_default=""),
        sa.Column("reviewed_by", sa.String(length=120), nullable=False, server_default=""),
        sa.Column("review_history", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_alerts_id", "alerts", ["id"])
    op.create_index("ix_alerts_reading_id", "alerts", ["reading_id"])
    op.create_index("ix_alerts_run_id", "alerts", ["run_id"])
    op.create_index("ix_alerts_timestamp", "alerts", ["timestamp"])

    op.create_table(
        "alert_thresholds",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.String(length=80), nullable=False, server_default="demo-org"),
        sa.Column("rig_id", sa.String(length=80), nullable=False, server_default="synthetic-rig-01"),
        sa.Column("temperature_high_c", sa.Float(), nullable=False, server_default="82"),
        sa.Column("temperature_critical_c", sa.Float(), nullable=False, server_default="90"),
        sa.Column("temperature_drift_c", sa.Float(), nullable=False, server_default="3"),
        sa.Column("vibration_high_mm_s", sa.Float(), nullable=False, server_default="4"),
        sa.Column("rpm_dropout", sa.Float(), nullable=False, server_default="50"),
        sa.Column("torque_dropout_nm", sa.Float(), nullable=False, server_default="5"),
        sa.Column("current_high_a", sa.Float(), nullable=False, server_default="38"),
        sa.Column("voltage_low_v", sa.Float(), nullable=False, server_default="394"),
    )
    op.create_index("ix_alert_thresholds_id", "alert_thresholds", ["id"])


def downgrade() -> None:
    op.drop_table("alert_thresholds")
    op.drop_table("alerts")
    op.drop_table("readings")
    op.drop_table("test_runs")
