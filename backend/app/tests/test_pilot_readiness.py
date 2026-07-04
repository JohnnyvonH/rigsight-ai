from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from app.main import create_app


def test_versioned_routes_and_operational_checks_are_available() -> None:
    with TestClient(create_app()) as client:
        runs_response = client.get("/api/v1/runs")
        ready_response = client.get("/api/v1/ready")
        metrics_response = client.get("/api/v1/metrics")

    assert runs_response.status_code == 200
    assert ready_response.status_code == 200
    assert ready_response.json()["database"] == "ok"
    assert metrics_response.status_code == 200
    assert metrics_response.json()["runs_total"] >= 1


def test_alert_filters_return_pagination_metadata() -> None:
    with TestClient(create_app()) as client:
        client.post("/demo/reset", json={"scenario": "fault-heavy-validation"})
        response = client.get("/api/v1/alerts?severity=high&detection_source=rules&limit=5")

    assert response.status_code == 200
    body = response.json()
    assert body["limit"] == 5
    assert body["offset"] == 0
    assert body["total_count"] >= body["count"]
    assert all(alert["severity"] == "high" for alert in body["alerts"])
    assert all(alert["detection_source"] == "rules" for alert in body["alerts"])


def test_ingest_creates_imported_run_readings_and_alerts() -> None:
    start = datetime.now(UTC).replace(microsecond=0) - timedelta(minutes=4)
    readings = [
        {
            "timestamp": (start + timedelta(minutes=index)).isoformat(),
            "phase": "Imported ramp",
            "rpm": 1400 + index,
            "torque_nm": 86,
            "temperature_c": 65 + index * 6,
            "vibration_mm_s": 1.8,
            "current_a": 29,
            "voltage_v": 399,
            "pressure_bar": 3.2,
            "fault_mode": "overheating" if index == 4 else None,
        }
        for index in range(5)
    ]

    with TestClient(create_app()) as client:
        response = client.post(
            "/api/v1/readings/ingest",
            json={
                "name": "Pilot import smoke test",
                "rig_id": "pilot-rig-smoke",
                "description": "Sanitized pilot sample",
                "readings": readings,
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["run"]["scenario"] == "customer-import"
    assert body["run"]["rig_id"] == "pilot-rig-smoke"
    assert body["readings_created"] == 5
    assert body["organization"]["id"] == "demo-org"


def test_review_update_captures_assignment_and_audit_history() -> None:
    with TestClient(create_app()) as client:
        client.post("/demo/reset", json={"scenario": "baseline-with-seeded-faults"})
        queue_response = client.get("/review/queue")
        alert_id = queue_response.json()["items"][0]["id"]
        response = client.patch(
            f"/api/v1/review/{alert_id}",
            headers={"X-RigSight-Actor": "pilot-reviewer"},
            json={
                "review_status": "needs_followup",
                "review_notes": "Check bearing temperature window.",
                "assigned_to": "validation-team",
            },
        )

    assert response.status_code == 200
    alert = response.json()["alert"]
    assert alert["assigned_to"] == "validation-team"
    assert alert["reviewed_by"] == "pilot-reviewer"
    assert "needs_followup" in alert["review_history"]


def test_html_report_endpoint_is_browser_printable() -> None:
    with TestClient(create_app()) as client:
        reset_response = client.post("/demo/reset", json={"scenario": "baseline-with-seeded-faults"})
        run_id = reset_response.json()["run"]["id"]
        response = client.get(f"/api/v1/reports/run/{run_id}/html")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "RigSight AI Run Report" in response.text
