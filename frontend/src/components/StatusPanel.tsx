import { CheckCircle2, RadioTower, RefreshCw } from "lucide-react";

import type { HealthResponse } from "../api/client";

type StatusPanelProps = {
  error: string | null;
  health: HealthResponse | null;
  isOnline: boolean;
  onRefresh: () => void;
  sampleCount: number;
};

export function StatusPanel({ error, health, isOnline, onRefresh, sampleCount }: StatusPanelProps) {
  return (
    <section className="status-panel" aria-live="polite">
      <div className="status-panel__header">
        <div>
          <span>Backend health</span>
          <strong>{isOnline ? "Online" : "Waiting"}</strong>
        </div>
        {isOnline ? <CheckCircle2 aria-hidden="true" /> : <RadioTower aria-hidden="true" />}
      </div>
      <dl>
        <div>
          <dt>Service</dt>
          <dd>{health?.service ?? "rigsight-api"}</dd>
        </div>
        <div>
          <dt>Version</dt>
          <dd>{health?.version ?? "1.0.0"}</dd>
        </div>
        <div>
          <dt>Environment</dt>
          <dd>{health?.environment ?? "development"}</dd>
        </div>
        <div>
          <dt>Last check</dt>
          <dd>{health ? new Date(health.timestamp).toLocaleTimeString() : "Pending"}</dd>
        </div>
        <div>
          <dt>Samples</dt>
          <dd>{sampleCount || "Pending"}</dd>
        </div>
      </dl>
      {error ? <p className="status-panel__error">{error}</p> : null}
      <button className="refresh-button" type="button" onClick={onRefresh}>
        <RefreshCw aria-hidden="true" />
        Refresh
      </button>
    </section>
  );
}
