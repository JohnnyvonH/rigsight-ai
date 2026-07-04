from fastapi.testclient import TestClient

from app.main import create_app
from app.services.simulator import generate_demo_readings


def test_demo_scenarios_include_baseline_and_fault_heavy() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/demo/scenarios")

    assert response.status_code == 200
    scenarios = {scenario["key"] for scenario in response.json()["scenarios"]}
    assert {"baseline-with-seeded-faults", "normal-baseline", "fault-heavy-validation"}.issubset(
        scenarios
    )


def test_normal_baseline_scenario_has_no_seeded_fault_modes() -> None:
    readings = generate_demo_readings(scenario="normal-baseline")

    assert len(readings) == 180
    assert {reading.fault_mode for reading in readings} == {None}


def test_demo_reset_creates_predictable_run_readings_and_alerts() -> None:
    with TestClient(create_app()) as client:
        response = client.post("/demo/reset", json={"scenario": "fault-heavy-validation"})
        runs_response = client.get("/runs")
        latest_response = client.get("/readings/latest")

        client.post("/demo/reset", json={"scenario": "baseline-with-seeded-faults"})

    assert response.status_code == 200
    body = response.json()
    assert body["run"]["scenario"] == "fault-heavy-validation"
    assert body["readings_created"] == 180
    assert body["alerts_created"] > 0
    assert runs_response.json()["runs"][0]["scenario"] == "fault-heavy-validation"
    assert latest_response.json()["run"]["scenario"] == "fault-heavy-validation"


def test_camera_status_is_disabled_by_default() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/camera/status")

    assert response.status_code == 200
    body = response.json()
    assert body["enabled"] is False
    assert body["status"] == "disabled"
    assert body["snapshot_available"] is False


def test_camera_snapshot_returns_unavailable_when_disabled() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/camera/snapshot")

    assert response.status_code == 503


def test_run_report_contains_1_0_summary_shape() -> None:
    with TestClient(create_app()) as client:
        reset_response = client.post("/demo/reset", json={"scenario": "baseline-with-seeded-faults"})
        run_id = reset_response.json()["run"]["id"]
        response = client.get(f"/reports/run/{run_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["run"]["id"] == run_id
    assert body["summary"]["reading_count"] == 180
    assert body["summary"]["alert_count"] > 0
    assert body["latest_reading"]["run_id"] == run_id
    assert "synthetic telemetry" in body["clean_room_note"]


def test_run_report_returns_404_for_unknown_run() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/reports/run/999999")

    assert response.status_code == 404
