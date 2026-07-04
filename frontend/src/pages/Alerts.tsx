import { BrainCircuit, ShieldCheck } from "lucide-react";
import { useMemo, useState } from "react";

import { AlertTimeline } from "../components/AlertTimeline";
import { MetricCard } from "../components/MetricCard";
import { PageHeader } from "../components/PageHeader";
import { useRigSightData } from "../hooks/useRigSightData";

export function Alerts() {
  const data = useRigSightData();
  const [severityFilter, setSeverityFilter] = useState("all");
  const [sourceFilter, setSourceFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");
  const filteredAlerts = useMemo(
    () =>
      data.alerts.filter(
        (alert) =>
          (severityFilter === "all" || alert.severity === severityFilter) &&
          (sourceFilter === "all" || alert.detection_source === sourceFilter) &&
          (statusFilter === "all" || alert.review_status === statusFilter),
      ),
    [data.alerts, severityFilter, sourceFilter, statusFilter],
  );

  return (
    <>
      <PageHeader
        description="Compare deterministic rule alerts with the IsolationForest ML anomaly baseline on the same synthetic readings."
        eyebrow="Detection"
        title="Rules and ML alerts"
      />

      <section className="split-panel split-panel--summary">
        <div className="metric-strip" aria-label="Detection summary">
          <MetricCard
            detail={`${data.highSeverityCount} high-severity alerts are visible in the current alert page.`}
            icon={<ShieldCheck aria-hidden="true" />}
            label="Rule alerts"
            tone={data.highSeverityCount > 0 ? "warning" : "good"}
            value={String(data.alertSummary?.rules_count ?? 0)}
          />
          <MetricCard
            detail="IsolationForest flags unusual cross-sensor combinations."
            icon={<BrainCircuit aria-hidden="true" />}
            label="ML anomalies"
            tone={(data.alertSummary?.ml_count ?? 0) > 0 ? "warning" : "neutral"}
            value={String(data.alertSummary?.ml_count ?? 0)}
          />
        </div>

        <aside className="info-panel">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Detection notes</p>
              <h2>How it works</h2>
            </div>
            <ShieldCheck aria-hidden="true" />
          </div>
          <div className="explanation-list">
            <p>
              Rule alerts cover thresholds, drift, dropout, voltage drop, current anomaly,
              overheating, and vibration spikes.
            </p>
            <p>
              ML alerts use an IsolationForest baseline over numeric sensor features. The
              comparison shows where deterministic and statistical approaches overlap.
            </p>
          </div>
        </aside>
      </section>

      <section className="chart-card page-card-full">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Alert timeline</p>
            <h2>Newest detections</h2>
          </div>
          <span>{filteredAlerts.length} visible</span>
        </div>
        <div className="filter-bar" aria-label="Alert filters">
          <label>
            <span>Severity</span>
            <select onChange={(event) => setSeverityFilter(event.target.value)} value={severityFilter}>
              <option value="all">All severities</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </label>
          <label>
            <span>Source</span>
            <select onChange={(event) => setSourceFilter(event.target.value)} value={sourceFilter}>
              <option value="all">All sources</option>
              <option value="rules">Rules</option>
              <option value="ml">ML</option>
            </select>
          </label>
          <label>
            <span>Review</span>
            <select onChange={(event) => setStatusFilter(event.target.value)} value={statusFilter}>
              <option value="all">All states</option>
              <option value="unreviewed">Unreviewed</option>
              <option value="confirmed">Confirmed</option>
              <option value="dismissed">Dismissed</option>
              <option value="needs_followup">Needs follow-up</option>
            </select>
          </label>
        </div>
        <AlertTimeline alerts={filteredAlerts} isLoading={data.isLoading} limit={16} />
      </section>
    </>
  );
}
