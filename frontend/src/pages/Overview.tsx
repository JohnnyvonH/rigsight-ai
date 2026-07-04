import { Activity, AlertTriangle, BrainCircuit, ShieldCheck, Thermometer, Zap } from "lucide-react";

import { DemoControls } from "../components/DemoControls";
import { DemoWalkthrough } from "../components/DemoWalkthrough";
import { FleetHealthPanel } from "../components/FleetHealthPanel";
import { MetricCard } from "../components/MetricCard";
import { PageHeader } from "../components/PageHeader";
import { RunSummary } from "../components/RunSummary";
import { StatusPanel } from "../components/StatusPanel";
import { useRigSightData } from "../hooks/useRigSightData";
import { formatFault, metricValue } from "../utils/format";

export function Overview() {
  const data = useRigSightData();
  const faultCount = data.history.filter((reading) => reading.fault_mode !== null).length;

  return (
    <>
      <PageHeader
        description={
          data.currentRun?.description ??
          "Live synthetic telemetry, persisted alerts, and human review state from the FastAPI backend."
        }
        eyebrow="Operational workspace"
        title="RigSight AI overview"
      />

      <FleetHealthPanel
        alerts={data.alerts}
        health={data.health}
        latestReading={data.latestReading}
        reviewQueueCount={data.reviewQueue.length}
        runs={data.runs}
      />

      <section className="overview-grid">
        <RunSummary
          faultCount={faultCount}
          latestFault={data.latestFault}
          latestReading={data.latestReading}
          run={data.currentRun}
          runCount={data.runs.length}
        />
        <StatusPanel
          error={data.error}
          health={data.health}
          isOnline={data.isOnline}
          onRefresh={() => data.loadTelemetry()}
          sampleCount={data.history.length}
        />
      </section>

      <section className="content-grid page-card-full">
        <DemoControls
          currentRun={data.currentRun}
          isRunning={data.isDemoActionRunning}
          message={data.demoActionMessage}
          onReset={data.resetDemo}
          onSeed={data.seedDemo}
          scenarios={data.scenarios}
        />
        <DemoWalkthrough />
      </section>

      <section className="metrics-grid" aria-label="Latest sensor readings">
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
          detail={`RPM ${data.latestReading?.rpm.toFixed(0) ?? "--"} at ${
            data.latestReading?.voltage_v.toFixed(1) ?? "--"
          } V`}
          icon={<Zap aria-hidden="true" />}
          label="Power draw"
          tone={data.latestReading && data.latestReading.current_a > 38 ? "warning" : "neutral"}
          value={metricValue(data.latestReading?.current_a, "A")}
        />
      </section>

      <section className="alert-summary-grid" aria-label="Alert summary">
        <MetricCard
          detail={`${data.highSeverityCount} high-severity alerts in the current page of alerts.`}
          icon={<ShieldCheck aria-hidden="true" />}
          label="Rule alerts"
          tone={data.highSeverityCount > 0 ? "warning" : "good"}
          value={String(data.alertSummary?.rules_count ?? 0)}
        />
        <MetricCard
          detail="IsolationForest scores synthetic samples across the sensor set."
          icon={<BrainCircuit aria-hidden="true" />}
          label="ML anomalies"
          tone={(data.alertSummary?.ml_count ?? 0) > 0 ? "warning" : "neutral"}
          value={String(data.alertSummary?.ml_count ?? 0)}
        />
        <MetricCard
          detail={`${data.alertSummary?.unreviewed_count ?? 0} unreviewed alerts from the API.`}
          icon={<AlertTriangle aria-hidden="true" />}
          label="Review queue"
          tone={data.reviewQueue.length > 0 ? "warning" : "good"}
          value={String(data.reviewQueue.length)}
        />
      </section>

    </>
  );
}
