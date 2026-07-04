import { FileUp, UploadCloud } from "lucide-react";
import { useState } from "react";

import type { IngestRunRequest, Reading } from "../api/client";
import { parseTelemetryCsv } from "../utils/csv";
import { metricValue } from "../utils/format";

type CsvImportPanelProps = {
  isImporting: boolean;
  message: string | null;
  onImport: (payload: IngestRunRequest) => void;
};

export function CsvImportPanel({ isImporting, message, onImport }: CsvImportPanelProps) {
  const [payload, setPayload] = useState<IngestRunRequest | null>(null);
  const [preview, setPreview] = useState<Partial<Reading>[]>([]);
  const [errors, setErrors] = useState<string[]>([]);
  const [rowCount, setRowCount] = useState(0);

  const handleFile = (file: File | undefined) => {
    if (!file) {
      return;
    }
    file.text().then((contents) => {
      const result = parseTelemetryCsv(contents);
      setPayload(result.payload);
      setPreview(result.preview);
      setErrors(result.errors);
      setRowCount(result.rowCount);
    });
  };

  return (
    <section className="control-panel" aria-label="CSV telemetry import">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Pilot import</p>
          <h2>CSV telemetry</h2>
        </div>
        <FileUp aria-hidden="true" />
      </div>

      <label className="file-drop-control">
        <UploadCloud aria-hidden="true" />
        <span>Choose sanitized CSV</span>
        <input
          accept=".csv,text/csv"
          onChange={(event) => handleFile(event.target.files?.[0])}
          type="file"
        />
      </label>

      {errors.length > 0 ? (
        <div className="validation-panel" role="alert">
          {errors.slice(0, 6).map((error) => (
            <p key={error}>{error}</p>
          ))}
        </div>
      ) : null}

      {payload ? (
        <>
          <div className="scenario-note">
            <strong>{payload.name}</strong>
            <p>
              {rowCount} readings for {payload.rig_id}. Previewing the first {preview.length}.
            </p>
            <span>{payload.description}</span>
          </div>
          <div className="csv-preview-table">
            {preview.map((reading, index) => (
              <div key={`${reading.timestamp}-${index}`}>
                <span>{new Date(String(reading.timestamp)).toLocaleTimeString()}</span>
                <strong>{metricValue(reading.temperature_c, "C")}</strong>
                <span>{metricValue(reading.vibration_mm_s, "mm/s", 2)}</span>
              </div>
            ))}
          </div>
          <button
            className="action-button action-button--primary"
            disabled={isImporting}
            onClick={() => onImport(payload)}
            type="button"
          >
            <UploadCloud aria-hidden="true" />
            Import telemetry
          </button>
        </>
      ) : null}

      {message ? <p className="panel-message">{message}</p> : null}
    </section>
  );
}
