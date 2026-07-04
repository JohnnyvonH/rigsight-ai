import { Database } from "lucide-react";

import { DemoControls } from "../components/DemoControls";
import { PageHeader } from "../components/PageHeader";
import { ReportPanel } from "../components/ReportPanel";
import { RunSummary } from "../components/RunSummary";
import { useRigSightData } from "../hooks/useRigSightData";
import { formatDateTime, formatLabel } from "../utils/format";

export function Runs() {
  const data = useRigSightData();
  const faultCount = data.history.filter((reading) => reading.fault_mode !== null).length;

  return (
    <>
      <PageHeader
        description="Inspect the seeded synthetic endurance run and how it supports telemetry, detection, and review workflows."
        eyebrow="Runs"
        title="Synthetic run history"
      />

      <section className="split-panel split-panel--runs">
        <RunSummary
          faultCount={faultCount}
          latestFault={data.latestFault}
          latestReading={data.latestReading}
          run={data.currentRun}
          runCount={data.runs.length}
        />

        <aside className="info-panel">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Scenario notes</p>
              <h2>Seeded endurance run</h2>
            </div>
            <Database aria-hidden="true" />
          </div>
          <div className="explanation-list">
            <p>
              The demo starts with one deterministic run so the telemetry, alert, and
              review pages are populated immediately after startup.
            </p>
            <p>
              Fault windows are injected into otherwise normal readings, making the
              timeline useful for explaining detection behavior without proprietary data.
            </p>
          </div>
        </aside>
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
        <ReportPanel
          onExport={data.exportRunReport}
          onExportHtml={data.exportRunReportHtml}
          report={data.report}
        />
      </section>

      <section className="chart-card page-card-full">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Run list</p>
            <h2>Available runs</h2>
          </div>
          <Database aria-hidden="true" />
        </div>

        <div className="table-list" data-testid="runs-list">
          {data.runs.map((run) => (
            <article className="table-row" key={run.id}>
              <div>
                <strong>{run.name}</strong>
                <span>{run.description}</span>
              </div>
              <dl>
                <div>
                  <dt>Scenario</dt>
                  <dd>{formatLabel(run.scenario)}</dd>
                </div>
                <div>
                  <dt>Status</dt>
                  <dd>{run.status}</dd>
                </div>
                <div>
                  <dt>Started</dt>
                  <dd>{formatDateTime(run.started_at)}</dd>
                </div>
              </dl>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
