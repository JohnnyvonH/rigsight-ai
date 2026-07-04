import { AlertTriangle, Database } from "lucide-react";

import type { Reading, TestRun } from "../api/client";
import { formatDateTime, formatFault } from "../utils/format";

type RunSummaryProps = {
  faultCount: number;
  latestFault: string | null;
  latestReading: Reading | null;
  run: TestRun | null;
  runCount: number;
};

export function RunSummary({
  faultCount,
  latestFault,
  latestReading,
  run,
  runCount,
}: RunSummaryProps) {
  return (
    <section className="run-panel run-panel--primary" id="runs">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Current run</p>
          <h2>{run?.name ?? "Active run"}</h2>
          <span className={`status-pill status-pill--${run?.status ?? "pending"}`}>
            {run?.status ?? "Pending"}
          </span>
        </div>
        <Database aria-hidden="true" />
      </div>
      <dl>
        <div>
          <dt>Scenario</dt>
          <dd>{run?.scenario ?? "Loading"}</dd>
        </div>
        <div>
          <dt>Rig</dt>
          <dd>{run?.rig_id ?? "Pending"}</dd>
        </div>
        <div>
          <dt>Workspace</dt>
          <dd>{run?.organization_id ?? "Pending"}</dd>
        </div>
        <div>
          <dt>Started</dt>
          <dd>{run ? formatDateTime(run.started_at) : "Pending"}</dd>
        </div>
        <div>
          <dt>Latest phase</dt>
          <dd>{latestReading?.phase ?? "Pending"}</dd>
        </div>
        <div>
          <dt>Fault samples</dt>
          <dd>{faultCount}</dd>
        </div>
        <div>
          <dt>Total runs</dt>
          <dd>{runCount}</dd>
        </div>
      </dl>

      <div className="fault-panel">
        <AlertTriangle aria-hidden="true" />
        <div>
          <span>Seeded fault mode</span>
          <strong>{formatFault(latestFault)}</strong>
        </div>
      </div>
    </section>
  );
}
