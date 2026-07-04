from fastapi.testclient import TestClient

from app.main import create_app


def test_alerts_returns_rules_and_ml_detections() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/alerts?limit=100")

    assert response.status_code == 200
    body = response.json()
    alert_types = {alert["alert_type"] for alert in body["alerts"]}
    detection_sources = {alert["detection_source"] for alert in body["alerts"]}

    assert body["count"] > 0
    assert "temperature_high" in alert_types
    assert "ml_anomaly" in alert_types
    assert {"rules", "ml"}.issubset(detection_sources)
    assert body["summary"]["rules_count"] > 0
    assert body["summary"]["ml_count"] > 0


def test_review_queue_and_update_alert() -> None:
    with TestClient(create_app()) as client:
        queue_response = client.get("/review/queue")
        assert queue_response.status_code == 200
        queued_items = queue_response.json()["items"]
        assert queued_items

        alert_id = queued_items[0]["id"]
        update_response = client.patch(
            f"/review/{alert_id}",
            json={"review_status": "confirmed", "review_notes": "Synthetic fault confirmed."},
        )
        assert update_response.status_code == 200
        updated_alert = update_response.json()["alert"]
        assert updated_alert["review_status"] == "confirmed"
        assert updated_alert["review_notes"] == "Synthetic fault confirmed."
        assert updated_alert["reviewed_at"] is not None

        reset_response = client.patch(
            f"/review/{alert_id}",
            json={"review_status": "unreviewed", "review_notes": ""},
        )
        assert reset_response.status_code == 200
        assert reset_response.json()["alert"]["review_status"] == "unreviewed"


def test_review_update_rejects_unknown_status() -> None:
    with TestClient(create_app()) as client:
        response = client.patch(
            "/review/1",
            json={"review_status": "not_a_real_status", "review_notes": ""},
        )

    assert response.status_code == 422
