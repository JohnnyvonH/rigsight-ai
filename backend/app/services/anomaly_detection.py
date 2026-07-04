"""Rules-based and ML anomaly detection for synthetic telemetry."""

from dataclasses import dataclass

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from app.models import Reading
from app.services.thresholds import ThresholdProfile, default_threshold_profile


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
    explanation: str = ""
    recommended_action: str = ""
    triggered_metric: str = ""
    expected_range: str = ""
    actual_value: str = ""


def detect_rule_alerts(
    readings: list[Reading], thresholds: ThresholdProfile | None = None
) -> list[AlertCandidate]:
    profile = thresholds or default_threshold_profile()
    alerts: list[AlertCandidate] = []
    previous_temperature: float | None = None

    for reading in readings:
        if reading.temperature_c >= profile.temperature_high_c:
            alerts.append(
                AlertCandidate(
                    reading=reading,
                    severity=(
                        "high"
                        if reading.temperature_c >= profile.temperature_critical_c
                        else "medium"
                    ),
                    alert_type="temperature_high",
                    title="Elevated temperature",
                    message="Rig temperature exceeded the configured operating threshold.",
                    detection_source="rules",
                    observed_value=reading.temperature_c,
                    threshold_value=profile.temperature_high_c,
                    explanation=(
                        f"Temperature reached {reading.temperature_c:.1f} C, above the "
                        f"{profile.temperature_high_c:.1f} C configured limit."
                    ),
                    recommended_action=(
                        "Review cooling performance, inspect load conditions, and compare "
                        "nearby vibration/current readings before continuing the run."
                    ),
                    triggered_metric="temperature_c",
                    expected_range=f"< {profile.temperature_high_c:.1f} C",
                    actual_value=f"{reading.temperature_c:.1f} C",
                )
            )

        temperature_delta = (
            reading.temperature_c - previous_temperature
            if previous_temperature is not None
            else None
        )
        if temperature_delta is not None and temperature_delta >= profile.temperature_drift_c:
            alerts.append(
                AlertCandidate(
                    reading=reading,
                    severity="medium",
                    alert_type="temperature_drift",
                    title="Temperature drift",
                    message="Temperature rose faster than expected between samples.",
                    detection_source="rules",
                    observed_value=temperature_delta,
                    threshold_value=profile.temperature_drift_c,
                    explanation=(
                        f"Temperature rose by {temperature_delta:.1f} C between samples, "
                        f"above the {profile.temperature_drift_c:.1f} C drift limit."
                    ),
                    recommended_action=(
                        "Check whether the ramp is expected for this phase and review the "
                        "previous five samples for sustained drift."
                    ),
                    triggered_metric="temperature_delta_c",
                    expected_range=f"< {profile.temperature_drift_c:.1f} C/sample",
                    actual_value=f"{temperature_delta:.1f} C/sample",
                )
            )

        if reading.vibration_mm_s >= profile.vibration_high_mm_s:
            alerts.append(
                AlertCandidate(
                    reading=reading,
                    severity="high",
                    alert_type="vibration_spike",
                    title="Vibration spike",
                    message="Vibration exceeded the synthetic vibration safety threshold.",
                    detection_source="rules",
                    observed_value=reading.vibration_mm_s,
                    threshold_value=profile.vibration_high_mm_s,
                    explanation=(
                        f"Vibration reached {reading.vibration_mm_s:.2f} mm/s, above the "
                        f"{profile.vibration_high_mm_s:.2f} mm/s configured limit."
                    ),
                    recommended_action=(
                        "Pause or slow the run if this is unexpected, then inspect mounting, "
                        "bearings, balance, and nearby torque readings."
                    ),
                    triggered_metric="vibration_mm_s",
                    expected_range=f"< {profile.vibration_high_mm_s:.2f} mm/s",
                    actual_value=f"{reading.vibration_mm_s:.2f} mm/s",
                )
            )

        if reading.rpm <= profile.rpm_dropout and reading.torque_nm <= profile.torque_dropout_nm:
            alerts.append(
                AlertCandidate(
                    reading=reading,
                    severity="high",
                    alert_type="sensor_dropout",
                    title="Sensor dropout",
                    message="RPM and torque dropped to near-zero during an active run.",
                    detection_source="rules",
                    observed_value=reading.rpm,
                    threshold_value=profile.rpm_dropout,
                    explanation=(
                        f"RPM dropped to {reading.rpm:.1f} while torque was "
                        f"{reading.torque_nm:.1f} Nm, matching the configured dropout pattern."
                    ),
                    recommended_action=(
                        "Validate sensor connectivity and confirm whether the run phase "
                        "included an intentional stop or data gap."
                    ),
                    triggered_metric="rpm",
                    expected_range=(
                        f"> {profile.rpm_dropout:.1f} RPM or > "
                        f"{profile.torque_dropout_nm:.1f} Nm torque"
                    ),
                    actual_value=f"{reading.rpm:.1f} RPM / {reading.torque_nm:.1f} Nm",
                )
            )

        if reading.current_a >= profile.current_high_a:
            alerts.append(
                AlertCandidate(
                    reading=reading,
                    severity="medium",
                    alert_type="current_anomaly",
                    title="Current anomaly",
                    message="Current draw exceeded the expected synthetic envelope.",
                    detection_source="rules",
                    observed_value=reading.current_a,
                    threshold_value=profile.current_high_a,
                    explanation=(
                        f"Current draw reached {reading.current_a:.1f} A, above the "
                        f"{profile.current_high_a:.1f} A configured limit."
                    ),
                    recommended_action=(
                        "Check load demand, supply stability, and whether this aligns with "
                        "temperature or voltage movement."
                    ),
                    triggered_metric="current_a",
                    expected_range=f"< {profile.current_high_a:.1f} A",
                    actual_value=f"{reading.current_a:.1f} A",
                )
            )

        if reading.voltage_v <= profile.voltage_low_v:
            alerts.append(
                AlertCandidate(
                    reading=reading,
                    severity="medium",
                    alert_type="voltage_drop",
                    title="Voltage drop",
                    message="Voltage dipped below the expected synthetic operating band.",
                    detection_source="rules",
                    observed_value=reading.voltage_v,
                    threshold_value=profile.voltage_low_v,
                    explanation=(
                        f"Voltage fell to {reading.voltage_v:.1f} V, below the "
                        f"{profile.voltage_low_v:.1f} V configured lower bound."
                    ),
                    recommended_action=(
                        "Review power supply stability and inspect current draw at the "
                        "same timestamp."
                    ),
                    triggered_metric="voltage_v",
                    expected_range=f"> {profile.voltage_low_v:.1f} V",
                    actual_value=f"{reading.voltage_v:.1f} V",
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
    feature_names = (
        "rpm",
        "torque_nm",
        "temperature_c",
        "vibration_mm_s",
        "current_a",
        "voltage_v",
        "pressure_bar",
    )

    alerts: list[AlertCandidate] = []
    for index, (reading, prediction, score) in enumerate(
        zip(readings, predictions, scores, strict=True)
    ):
        if prediction != -1:
            continue

        anomaly_score = round(float(score), 4)
        deviations = sorted(
            (
                (feature_names[feature_index], abs(float(value)))
                for feature_index, value in enumerate(scaled_features[index])
            ),
            key=lambda item: item[1],
            reverse=True,
        )
        top_deviations = ", ".join(
            f"{name} z={deviation:.2f}" for name, deviation in deviations[:3]
        )
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
                explanation=(
                    "IsolationForest marked this sample as unusual across the sensor set. "
                    f"Largest standardized deviations: {top_deviations}."
                ),
                recommended_action=(
                    "Compare this timestamp with nearby rule alerts and inspect the run "
                    "phase before deciding whether to confirm or dismiss."
                ),
                triggered_metric="multi_sensor_anomaly",
                expected_range="Within learned synthetic baseline",
                actual_value=f"anomaly score {anomaly_score:.4f}",
            )
        )

    return alerts
