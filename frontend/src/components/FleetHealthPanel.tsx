import { AlertTriangle, Factory, Server, ShieldCheck } from "lucide-react";

import type { AlertRecord, HealthResponse, Reading, TestRun } from "../api/client";
import { formatLabel } from "../utils/format";

type FleetHealthPanelProps = {
  alerts: AlertRecord[];
  health: HealthResponse | null;
  latestReading: Reading | null;
  reviewQueueCount: number;
  runs: TestRun[];
};

export function FleetHealthPanel({
  alerts,
  health,
  latestReading,
  reviewQueueCount,
  runs,
}: FleetHealthPanelProps) {
  const activeRigIds = new Set(runs.map((run) => run.rig_id));
  const activeRunCount = runs.filter((run) => run.status === "active").length;
  const highAlertCount = alerts.filter((alert) => alert.severity === "high").length;
  const highestRiskAlert = alerts.find((alert) => alert.severity === "high") ?? alerts[0];

  return (
    <section className="fleet-panel" aria-label="Fleet health overview">
      <div className="fleet-panel__header">
        <div>
          <p className="eyebrow">Fleet health</p>
          <h2>{highAlertCount > 0 ? "Action required" : "Pilot workspace stable"}</h2>
        </div>
        <Factory aria-hidden="true" />
      </div>

      <div className="fleet-scoreboard">
        <div>
          <span>Rigs monitored</span>
          <strong>{activeRigIds.size || 1}</strong>
        </div>
        <div>
          <span>Active runs</span>
          <strong>{activeRunCount}</strong>
        </div>
        <div>
          <span>High alerts</span>
          <strong>{highAlertCount}</strong>
        </div>
        <div>
          <span>Review backlog</span>
          <strong>{reviewQueueCount}</strong>
        </div>
      </div>

      <div className="fleet-detail-grid">
        <article>
          <ShieldCheck aria-hidden="true" />
          <div>
            <span>System health</span>
            <strong>{health?.status === "ok" ? "API online" : "Waiting for API"}</strong>
          </div>
        </article>
        <article>
          <AlertTriangle aria-hidden="true" />
          <div>
            <span>Top risk</span>
            <strong>{highestRiskAlert ? highestRiskAlert.title : "No active alerts"}</strong>
          </div>
        </article>
        <article>
          <Server aria-hidden="true" />
          <div>
            <span>Latest phase</span>
            <strong>{latestReading ? formatLabel(latestReading.phase) : "Pending telemetry"}</strong>
          </div>
        </article>
      </div>
    </section>
  );
}
