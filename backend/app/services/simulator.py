"""Deterministic synthetic rig telemetry generation."""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from math import sin


@dataclass(frozen=True)
class SyntheticReading:
    timestamp: datetime
    phase: str
    rpm: float
    torque_nm: float
    temperature_c: float
    vibration_mm_s: float
    current_a: float
    voltage_v: float
    pressure_bar: float
    fault_mode: str | None


@dataclass(frozen=True)
class ScenarioDefinition:
    key: str
    name: str
    description: str
    expected_faults: tuple[str, ...]


PHASES = (
    "Warmup",
    "Steady load",
    "Ramp test",
    "Endurance hold",
    "Cooldown",
)

SCENARIOS: dict[str, ScenarioDefinition] = {
    "baseline-with-seeded-faults": ScenarioDefinition(
        key="baseline-with-seeded-faults",
        name="Synthetic endurance validation",
        description=(
            "Deterministic synthetic run with normal operation, overheating, vibration, "
            "dropout, drift, and current anomaly windows."
        ),
        expected_faults=(
            "overheating",
            "vibration_spike",
            "sensor_dropout",
            "temperature_drift",
            "current_anomaly",
        ),
    ),
    "normal-baseline": ScenarioDefinition(
        key="normal-baseline",
        name="Normal baseline validation",
        description="Deterministic synthetic run with normal readings and no seeded faults.",
        expected_faults=(),
    ),
    "fault-heavy-validation": ScenarioDefinition(
        key="fault-heavy-validation",
        name="Fault-heavy validation",
        description=(
            "Deterministic synthetic run with stronger overheating, vibration, dropout, "
            "drift, and power anomaly windows for a denser alert demo."
        ),
        expected_faults=(
            "overheating",
            "vibration_spike",
            "sensor_dropout",
            "temperature_drift",
            "current_anomaly",
        ),
    ),
}


def get_scenario_definition(scenario: str) -> ScenarioDefinition:
    return SCENARIOS.get(scenario, SCENARIOS["baseline-with-seeded-faults"])


def generate_demo_readings(
    *,
    count: int = 180,
    interval_seconds: int = 20,
    end_time: datetime | None = None,
    scenario: str = "baseline-with-seeded-faults",
) -> list[SyntheticReading]:
    """Generate repeatable readings with short synthetic fault windows."""

    if count < 1:
        return []

    final_time = end_time or datetime.now(UTC).replace(microsecond=0)
    start_time = final_time - timedelta(seconds=interval_seconds * (count - 1))
    readings: list[SyntheticReading] = []
    scenario_key = get_scenario_definition(scenario).key

    for index in range(count):
        timestamp = start_time + timedelta(seconds=interval_seconds * index)
        progress = index / max(count - 1, 1)
        phase = PHASES[min(int(progress * len(PHASES)), len(PHASES) - 1)]

        rpm = 1420 + 260 * sin(index / 11) + 90 * sin(index / 37)
        torque_nm = 84 + 10 * sin(index / 15) + 4 * sin(index / 5)
        temperature_c = 63 + 7 * sin(index / 18) + progress * 6
        vibration_mm_s = 1.7 + 0.35 * sin(index / 8)
        current_a = 28 + 3.4 * sin(index / 10)
        voltage_v = 399 + 1.8 * sin(index / 13)
        pressure_bar = 3.1 + 0.25 * sin(index / 12)
        fault_mode: str | None = None

        if scenario_key == "normal-baseline":
            pass
        elif 44 <= index <= 54:
            fault_mode = "overheating"
            intensity = 1.25 if scenario_key == "fault-heavy-validation" else 1
            temperature_c += (16 + (index - 44) * 0.8) * intensity
        elif 78 <= index <= 82:
            fault_mode = "vibration_spike"
            intensity = 1.3 if scenario_key == "fault-heavy-validation" else 1
            vibration_mm_s += (3.8 + (index - 78) * 0.35) * intensity
        elif 104 <= index <= 108:
            fault_mode = "sensor_dropout"
            rpm = 0
            torque_nm = 0
        elif 128 <= index <= 148:
            fault_mode = "temperature_drift"
            intensity = 1.2 if scenario_key == "fault-heavy-validation" else 1
            temperature_c += (index - 128) * 0.9 * intensity
        elif 158 <= index <= 164:
            fault_mode = "current_anomaly"
            intensity = 1.25 if scenario_key == "fault-heavy-validation" else 1
            current_a += (12 + 2 * sin(index)) * intensity
            voltage_v -= 8 if scenario_key == "fault-heavy-validation" else 7

        if scenario_key == "fault-heavy-validation" and 18 <= index <= 23:
            fault_mode = "vibration_spike"
            vibration_mm_s += 2.8

        readings.append(
            SyntheticReading(
                timestamp=timestamp,
                phase=phase,
                rpm=round(rpm, 1),
                torque_nm=round(torque_nm, 1),
                temperature_c=round(temperature_c, 1),
                vibration_mm_s=round(vibration_mm_s, 2),
                current_a=round(current_a, 1),
                voltage_v=round(voltage_v, 1),
                pressure_bar=round(pressure_bar, 2),
                fault_mode=fault_mode,
            )
        )

    return readings
