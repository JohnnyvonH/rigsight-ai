import { Download, FileJson, Printer } from "lucide-react";

import type { RunReportResponse } from "../api/client";

type ReportPanelProps = {
  onExport: () => void;
  onExportHtml: () => void;
  report: RunReportResponse | null;
};

export function ReportPanel({ onExport, onExportHtml, report }: ReportPanelProps) {
  return (
    <section className="info-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Report export</p>
          <h2>Run summary</h2>
        </div>
        <FileJson aria-hidden="true" />
      </div>
      <dl className="compact-dl">
        <div>
          <dt>Readings</dt>
          <dd>{report?.summary.reading_count ?? "Pending"}</dd>
        </div>
        <div>
          <dt>Alerts</dt>
          <dd>{report?.summary.alert_count ?? "Pending"}</dd>
        </div>
        <div>
          <dt>Unreviewed</dt>
          <dd>{report?.summary.unreviewed_count ?? "Pending"}</dd>
        </div>
      </dl>
      <div className="button-row">
        <button className="action-button action-button--primary" onClick={onExportHtml} type="button">
          <Printer aria-hidden="true" />
          Open report
        </button>
        <button className="action-button" onClick={onExport} type="button">
          <Download aria-hidden="true" />
          Export JSON
        </button>
      </div>
    </section>
  );
}
