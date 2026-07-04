import { RotateCcw, Save, SlidersHorizontal } from "lucide-react";
import { useEffect, useState } from "react";

import type { TestRun, ThresholdProfile, ThresholdUpdate } from "../api/client";

const thresholdFields: Array<{
  key: keyof Omit<ThresholdUpdate, "rig_id">;
  label: string;
  unit: string;
}> = [
  { key: "temperature_high_c", label: "Temperature high", unit: "C" },
  { key: "temperature_critical_c", label: "Temperature critical", unit: "C" },
  { key: "temperature_drift_c", label: "Temperature drift", unit: "C/sample" },
  { key: "vibration_high_mm_s", label: "Vibration high", unit: "mm/s" },
  { key: "rpm_dropout", label: "RPM dropout", unit: "RPM" },
  { key: "torque_dropout_nm", label: "Torque dropout", unit: "Nm" },
  { key: "current_high_a", label: "Current high", unit: "A" },
  { key: "voltage_low_v", label: "Voltage low", unit: "V" },
];

type ThresholdPanelProps = {
  currentRun: TestRun | null;
  isRunning: boolean;
  message: string | null;
  onRecalculate: () => void;
  onReset: () => void;
  onSave: (thresholds: ThresholdUpdate) => void;
  thresholds: ThresholdProfile | null;
};

export function ThresholdPanel({
  currentRun,
  isRunning,
  message,
  onRecalculate,
  onReset,
  onSave,
  thresholds,
}: ThresholdPanelProps) {
  const [draft, setDraft] = useState<ThresholdUpdate | null>(null);

  useEffect(() => {
    if (thresholds) {
      const { organization_id: _organizationId, persisted: _persisted, ...editable } = thresholds;
      setDraft(editable);
    }
  }, [thresholds]);

  return (
    <section className="control-panel" aria-label="Alert threshold configuration">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Detection tuning</p>
          <h2>Alert thresholds</h2>
        </div>
        <SlidersHorizontal aria-hidden="true" />
      </div>

      <div className="threshold-grid">
        {thresholdFields.map((field) => (
          <label className="field-control" key={field.key}>
            <span>
              {field.label} ({field.unit})
            </span>
            <input
              disabled={!draft}
              onChange={(event) =>
                setDraft((current) =>
                  current
                    ? { ...current, [field.key]: Number(event.target.value) }
                    : current,
                )
              }
              step="0.1"
              type="number"
              value={draft ? draft[field.key] : ""}
            />
          </label>
        ))}
      </div>

      <div className="scenario-note">
        <strong>{draft?.rig_id ?? currentRun?.rig_id ?? "synthetic-rig-01"}</strong>
        <p>
          Saving updates the profile. Recalculate refreshes rules-based alerts for the current run
          while preserving matching review decisions.
        </p>
        <span>{thresholds?.persisted ? "Custom profile" : "Default profile"}</span>
      </div>

      <div className="button-row">
        <button
          className="action-button action-button--primary"
          disabled={!draft || isRunning}
          onClick={() => draft && onSave(draft)}
          type="button"
        >
          <Save aria-hidden="true" />
          Save thresholds
        </button>
        <button className="action-button" disabled={isRunning} onClick={onReset} type="button">
          <RotateCcw aria-hidden="true" />
          Reset
        </button>
        <button
          className="action-button"
          disabled={!currentRun || isRunning}
          onClick={onRecalculate}
          type="button"
        >
          Recalculate alerts
        </button>
      </div>
      {message ? <p className="panel-message">{message}</p> : null}
    </section>
  );
}
