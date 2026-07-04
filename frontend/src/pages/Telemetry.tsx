import { Activity, Thermometer, Zap } from "lucide-react";
import { useState } from "react";

import { MetricCard } from "../components/MetricCard";
import { PageHeader } from "../components/PageHeader";
import { chartSensors, TelemetryChart, type ChartSensorKey } from "../components/TelemetryChart";
import { useRigSightData } from "../hooks/useRigSightData";
import { formatFault, metricValue } from "../utils/format";

export function Telemetry() {
  const data = useRigSightData();
  const [selectedSensor, setSelectedSensor] = useState<ChartSensorKey>("temperature_c");
  const faultSamples = data.history.filter((reading) => reading.fault_mode);
  const activeScenario = data.scenarios.find(
    (scenario) => scenario.key === data.currentRun?.scenario,
  );

  return (
    <>
      <PageHeader
        description="Trend sensor values over the seeded endurance run and inspect the synthetic fault windows that drive alerts."
        eyebrow="Telemetry"
        title="Telemetry analysis"
      />

      <section className="content-grid content-grid--wide">
        <section className="chart-card">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Recent telemetry</p>
              <h2>Sensor trend</h2>
            </div>
            <span>{data.isLoading ? "Loading" : `${data.history.length} samples`}</span>
          </div>
          <div className="segmented-control" aria-label="Sensor chart view">
            {chartSensors.map((sensor) => (
              <button
                className={selectedSensor === sensor.key ? "is-active" : ""}
                key={sensor.key}
                onClick={() => setSelectedSensor(sensor.key)}
                type="button"
              >
                {sensor.name}
              </button>
            ))}
            <button
              className={selectedSensor === "all" ? "is-active" : ""}
              onClick={() => setSelectedSensor("all")}
              type="button"
            >
              Compare
            </button>
          </div>
          <TelemetryChart
            isLoading={data.isLoading}
            readings={data.history}
            selectedSensor={selectedSensor}
          />
        </section>

        <aside className="run-panel">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Fault windows</p>
              <h2>{faultSamples.length} samples</h2>
            </div>
            <Activity aria-hidden="true" />
          </div>
          <div className="explanation-list">
            <p>
              {activeScenario?.description ??
                "The synthetic run includes deterministic phases and clean-room readings."}
            </p>
            <p>
              Expected faults:{" "}
              {activeScenario?.expected_faults.length
                ? activeScenario.expected_faults.map(formatFault).join(", ")
                : "none for this scenario"}.
            </p>
          </div>
        </aside>
      </section>

      <section className="metrics-grid" aria-label="Latest telemetry details">
        <MetricCard
          detail={`Current phase: ${data.latestReading?.phase ?? "Loading"}`}
          icon={<Thermometer aria-hidden="true" />}
          label="Temperature"
          tone={data.latestReading && data.latestReading.temperature_c > 82 ? "warning" : "good"}
          value={metricValue(data.latestReading?.temperature_c, "C")}
        />
        <MetricCard
          detail={`Fault window: ${formatFault(data.latestFault)}`}
          icon={<Activity aria-hidden="true" />}
          label="Vibration"
          tone={data.latestFault ? "warning" : "neutral"}
          value={metricValue(data.latestReading?.vibration_mm_s, "mm/s", 2)}
        />
        <MetricCard
          detail={`Voltage ${data.latestReading?.voltage_v.toFixed(1) ?? "--"} V`}
          icon={<Zap aria-hidden="true" />}
          label="Current"
          tone={data.latestReading && data.latestReading.current_a > 38 ? "warning" : "neutral"}
          value={metricValue(data.latestReading?.current_a, "A")}
        />
      </section>
    </>
  );
}
