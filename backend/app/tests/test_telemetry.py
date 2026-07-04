from fastapi.testclient import TestClient

from app.main import create_app
from app.services.simulator import generate_demo_readings


def test_demo_simulator_includes_seeded_fault_modes() -> None:
    readings = generate_demo_readings()
    fault_modes = {reading.fault_mode for reading in readings if reading.fault_mode}

    assert len(readings) == 180
    assert {
        "overheating",
        "vibration_spike",
        "sensor_dropout",
        "temperature_drift",
        "current_anomaly",
    }.issubset(fault_modes)


def test_runs_returns_seeded_demo_run() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/runs")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    assert body["runs"][0]["scenario"] == "baseline-with-seeded-faults"


def test_latest_reading_returns_run_context() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/readings/latest")

    assert response.status_code == 200
    body = response.json()
    assert body["reading"]["id"] is not None
    assert body["reading"]["run_id"] == body["run"]["id"]
    assert body["reading"]["phase"]


def test_history_limit_returns_oldest_to_newest() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/readings/history?limit=12")

    assert response.status_code == 200
    body = response.json()
    readings = body["readings"]
    timestamps = [reading["timestamp"] for reading in readings]

    assert body["count"] == 12
    assert timestamps == sorted(timestamps)
