from html import escape
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, Response
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.api.routes_alerts import serialize_alert
from app.api.routes_readings import serialize_reading, serialize_run
from app.database import get_db
from app.models import Alert, Reading, TestRun
from app.services.thresholds import get_threshold_profile, serialize_threshold_profile

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
    top_alerts = list(
        db.scalars(
            select(Alert)
            .options(joinedload(Alert.reading), joinedload(Alert.run))
            .where(Alert.run_id == run_id)
            .order_by(Alert.severity.desc(), Alert.timestamp.desc(), Alert.id.desc())
            .limit(10)
        )
    )
    threshold_profile, threshold_persisted = get_threshold_profile(
        db, organization_id=run.organization_id, rig_id=run.rig_id
    )

    return {
        "run": serialize_run(run),
        "latest_reading": serialize_reading(latest_reading) if latest_reading else None,
        "top_alerts": [serialize_alert(alert) for alert in top_alerts],
        "thresholds": serialize_threshold_profile(
            threshold_profile, persisted=threshold_persisted
        ),
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


@router.get("/run/{run_id}/pdf")
def run_report_pdf(run_id: int, db: Session = Depends(get_db)) -> Response:
    report = build_run_report(run_id, db)
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title=f"RigSight AI Run Report {run_id}")
    styles = getSampleStyleSheet()
    elements = [
        Paragraph("RigSight AI Run Report", styles["Title"]),
        Paragraph(str(report["run"]["name"]), styles["Heading2"]),
        Paragraph(f"Rig: {report['run']['rig_id']}", styles["Normal"]),
        Spacer(1, 14),
    ]

    summary_rows = [["Metric", "Value"]]
    summary_rows.extend(
        [key.replace("_", " ").title(), str(value)]
        for key, value in report["summary"].items()
    )
    summary_table = Table(summary_rows, hAlign="LEFT")
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#14213d")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#dbe3ee")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    elements.extend([Paragraph("Summary", styles["Heading2"]), summary_table, Spacer(1, 14)])

    threshold_rows = [["Threshold", "Value"]]
    threshold_rows.extend(
        [key.replace("_", " ").title(), str(value)]
        for key, value in report["thresholds"].items()
        if key not in {"organization_id", "rig_id", "persisted"}
    )
    threshold_table = Table(threshold_rows, hAlign="LEFT")
    threshold_table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.25, colors.grey)]))
    elements.extend([Paragraph("Threshold Profile", styles["Heading2"]), threshold_table, Spacer(1, 14)])

    alert_rows = [["Severity", "Type", "Recommendation"]]
    for alert in report["top_alerts"][:6]:
        alert_rows.append(
            [
                str(alert["severity"]),
                str(alert["alert_type"]),
                str(alert["recommended_action"] or alert["message"])[:100],
            ]
        )
    if len(alert_rows) == 1:
        alert_rows.append(["-", "No alerts", "-"])
    alert_table = Table(alert_rows, colWidths=[70, 110, 300], hAlign="LEFT")
    alert_table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.25, colors.grey)]))
    elements.extend([Paragraph("Top Alerts", styles["Heading2"]), alert_table, Spacer(1, 14)])

    elements.append(Paragraph(str(report["clean_room_note"]), styles["Italic"]))
    doc.build(elements)
    buffer.seek(0)
    return Response(
        content=buffer.read(),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="rigsight-run-{run_id}-report.pdf"'},
    )
