from html import escape

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.routes_readings import serialize_reading, serialize_run
from app.database import get_db
from app.models import Alert, Reading, TestRun

router = APIRouter(prefix="/reports", tags=["reports"])


def build_run_report(run_id: int, db: Session) -> dict[str, object]:
    run = db.get(TestRun, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    latest_reading = db.scalar(
        select(Reading).where(Reading.run_id == run_id).order_by(Reading.timestamp.desc()).limit(1)
    )
    reading_count = db.scalar(select(func.count()).select_from(Reading).where(Reading.run_id == run_id))
    alert_count = db.scalar(select(func.count()).select_from(Alert).where(Alert.run_id == run_id))
    high_alert_count = db.scalar(
        select(func.count())
        .select_from(Alert)
        .where(Alert.run_id == run_id, Alert.severity == "high")
    )
    unreviewed_count = db.scalar(
        select(func.count())
        .select_from(Alert)
        .where(Alert.run_id == run_id, Alert.review_status == "unreviewed")
    )
    confirmed_count = db.scalar(
        select(func.count())
        .select_from(Alert)
        .where(Alert.run_id == run_id, Alert.review_status == "confirmed")
    )
    rules_count = db.scalar(
        select(func.count())
        .select_from(Alert)
        .where(Alert.run_id == run_id, Alert.detection_source == "rules")
    )
    ml_count = db.scalar(
        select(func.count())
        .select_from(Alert)
        .where(Alert.run_id == run_id, Alert.detection_source == "ml")
    )

    return {
        "run": serialize_run(run),
        "latest_reading": serialize_reading(latest_reading) if latest_reading else None,
        "summary": {
            "reading_count": reading_count or 0,
            "alert_count": alert_count or 0,
            "high_alert_count": high_alert_count or 0,
            "unreviewed_count": unreviewed_count or 0,
            "confirmed_count": confirmed_count or 0,
            "rules_count": rules_count or 0,
            "ml_count": ml_count or 0,
        },
        "clean_room_note": (
            "RigSight AI 1.0 uses synthetic telemetry, synthetic alerts, and local-only "
            "review states. It does not include proprietary test data or private artifacts."
        ),
    }


@router.get("/run/{run_id}")
def run_report(run_id: int, db: Session = Depends(get_db)) -> dict[str, object]:
    return build_run_report(run_id, db)


@router.get("/run/{run_id}/html", response_class=HTMLResponse)
def run_report_html(run_id: int, db: Session = Depends(get_db)) -> str:
    report = build_run_report(run_id, db)
    run = report["run"]
    latest = report["latest_reading"]
    summary = report["summary"]
    latest_rows = ""
    if latest:
        latest_rows = "".join(
            f"<tr><th>{escape(label)}</th><td>{escape(str(value))}</td></tr>"
            for label, value in (
                ("Temperature C", latest["temperature_c"]),
                ("Vibration mm/s", latest["vibration_mm_s"]),
                ("Current A", latest["current_a"]),
                ("Voltage V", latest["voltage_v"]),
                ("Fault mode", latest["fault_mode"] or "none"),
            )
        )

    summary_rows = "".join(
        f"<tr><th>{escape(key.replace('_', ' ').title())}</th><td>{value}</td></tr>"
        for key, value in summary.items()
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>RigSight AI Run Report - {escape(str(run["name"]))}</title>
  <style>
    body {{ font-family: Inter, Arial, sans-serif; margin: 40px; color: #14213d; }}
    header {{ border-bottom: 3px solid #1d7e6b; margin-bottom: 28px; padding-bottom: 18px; }}
    h1 {{ margin: 0 0 8px; font-size: 34px; }}
    h2 {{ margin-top: 28px; color: #0f1a2a; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    th, td {{ border-bottom: 1px solid #dbe3ee; padding: 10px 8px; text-align: left; }}
    th {{ color: #58677d; width: 42%; }}
    .note {{ background: #f3f6fa; border-left: 4px solid #1d7e6b; padding: 14px; }}
  </style>
</head>
<body>
  <header>
    <h1>RigSight AI Run Report</h1>
    <p>{escape(str(run["name"]))} - {escape(str(run["rig_id"]))}</p>
  </header>
  <section>
    <h2>Run Summary</h2>
    <table>{summary_rows}</table>
  </section>
  <section>
    <h2>Latest Reading</h2>
    <table>{latest_rows}</table>
  </section>
  <section class="note">
    <strong>Clean-room note:</strong> {escape(str(report["clean_room_note"]))}
  </section>
</body>
</html>"""
