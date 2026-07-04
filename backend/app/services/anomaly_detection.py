"""Rules-based and ML anomaly detection for synthetic telemetry."""

from dataclasses import dataclass

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from app.models import Reading


@dataclass(frozen=True)
class AlertCandidate:
    reading: Reading
    severity: str
    alert_type: str
    title: str
    message: str
    detection_source: str
    observed_value: float | None = None
    threshold_value: float | None = None
    anomaly_score: float | None = None
    ml_is_anomaly: bool = False


def detect_rule_alerts(readings: list[Reading]) -> list[AlertCandidate]:
    alerts: list[AlertCandidate] = []
    previous_temperature: float | None = None

    for reading in readings:
        if reading.temperature_c >= 82:
            alerts.append(
                AlertCandidate(
                    reading=reading,
                    severity="high" if reading.temperature_c >= 90 else "medium",
                    alert_type="temperature_high",
                    title="Elevated temperature",
                    message="Rig temperature exceeded the synthetic operating threshold.",
                    detection_source="rules",
                    observed_value=reading.temperature_c,
                    threshold_value=82,
                )
            )

        if previous_temperature is not None and reading.temperature_c - previous_temperature >= 3:
            alerts.append(
                AlertCandidate(
                    reading=reading,
                    severity="medium",
                    alert_type="temperature_drift",
                    title="Temperature drift",
                    message="Temperature rose faster than expected between samples.",
                    detection_source="rules",
                    observed_value=reading.temperature_c - previous_temperature,
                    threshold_value=3,
                )
            )

        if reading.vibration_mm_s >= 4:
            alerts.append(
                AlertCandidate(
                    reading=reading,
                    severity="high",
                    alert_type="vibration_spike",
                    title="Vibration spike",
                    message="Vibration exceeded the synthetic vibration safety threshold.",
                    detection_source="rules",
                    observed_value=reading.vibration_mm_s,
                    threshold_value=4,
                )
            )

        if reading.rpm <= 50 and reading.torque_nm <= 5:
            alerts.append(
                AlertCandidate(
                    reading=reading,
                    severity="high",
                    alert_type="sensor_dropout",
                    title="Sensor dropout",
                    message="RPM and torque dropped to near-zero during an active run.",
                    detection_source="rules",
                    observed_value=reading.rpm,
                    threshold_value=50,
                )
            )

        if reading.current_a >= 38:
            alerts.append(
                AlertCandidate(
                    reading=reading,
                    severity="medium",
                    alert_type="current_anomaly",
                    title="Current anomaly",
                    message="Current draw exceeded the expected synthetic envelope.",
                    detection_source="rules",
                    observed_value=reading.current_a,
                    threshold_value=38,
                )
            )

        if reading.voltage_v <= 394:
            alerts.append(
                AlertCandidate(
                    reading=reading,
                    severity="medium",
                    alert_type="voltage_drop",
                    title="Voltage drop",
                    message="Voltage dipped below the expected synthetic operating band.",
                    detection_source="rules",
                    observed_value=reading.voltage_v,
                    threshold_value=394,
                )
            )

        previous_temperature = reading.temperature_c

    return alerts


def detect_ml_alerts(readings: list[Reading]) -> list[AlertCandidate]:
    if len(readings) < 20:
        return []

    features = [
        [
            reading.rpm,
            reading.torque_nm,
            reading.temperature_c,
            reading.vibration_mm_s,
            reading.current_a,
            reading.voltage_v,
            reading.pressure_bar,
        ]
        for reading in readings
    ]
    scaled_features = StandardScaler().fit_transform(features)
    model = IsolationForest(contamination=0.12, random_state=42)
    predictions = model.fit_predict(scaled_features)
    scores = model.decision_function(scaled_features)

    alerts: list[AlertCandidate] = []
    for reading, prediction, score in zip(readings, predictions, scores, strict=True):
        if prediction != -1:
            continue

        anomaly_score = round(float(score), 4)
        alerts.append(
            AlertCandidate(
                reading=reading,
                severity="medium" if anomaly_score > -0.08 else "high",
                alert_type="ml_anomaly",
                title="ML anomaly score",
                message="IsolationForest marked this sample as unusual across the sensor set.",
                detection_source="ml",
                anomaly_score=anomaly_score,
                ml_is_anomaly=True,
            )
        )

    return alerts
