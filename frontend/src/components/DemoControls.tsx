import { DatabaseZap, RotateCcw, Sprout } from "lucide-react";
import { useMemo, useState } from "react";

import type { DemoScenario, TestRun } from "../api/client";
import { formatLabel } from "../utils/format";

type DemoControlsProps = {
  currentRun: TestRun | null;
  isRunning: boolean;
  message: string | null;
  onReset: (scenario: string) => void;
  onSeed: (scenario: string) => void;
  scenarios: DemoScenario[];
};

export function DemoControls({
  currentRun,
  isRunning,
  message,
  onReset,
  onSeed,
  scenarios,
}: DemoControlsProps) {
  const selectedDefault = currentRun?.scenario ?? scenarios[0]?.key ?? "baseline-with-seeded-faults";
  const [selectedScenario, setSelectedScenario] = useState(selectedDefault);
  const [isDemoModeEnabled, setIsDemoModeEnabled] = useState(false);
  const activeScenario = useMemo(
    () => scenarios.find((scenario) => scenario.key === selectedScenario) ?? scenarios[0],
    [scenarios, selectedScenario],
  );

  return (
    <section className="control-panel" aria-label="Demo controls">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Rig controls</p>
          <h2>Demo data</h2>
        </div>
        <DatabaseZap aria-hidden="true" />
      </div>

      <label className="field-control">
        <span>Scenario</span>
        <select
          onChange={(event) => setSelectedScenario(event.target.value)}
          value={selectedScenario}
        >
          {scenarios.map((scenario) => (
            <option key={scenario.key} value={scenario.key}>
              {scenario.name}
            </option>
          ))}
        </select>
      </label>

      <div className="scenario-note">
        <strong>{activeScenario?.name ?? formatLabel(selectedScenario)}</strong>
        <p>{activeScenario?.description ?? "Scenario metadata is loading from the API."}</p>
        <span>
          Fault windows:{" "}
          {activeScenario?.expected_faults.length
            ? activeScenario.expected_faults.map(formatLabel).join(", ")
            : "none"}
        </span>
      </div>

      <label className="demo-mode-toggle">
        <input
          checked={isDemoModeEnabled}
          onChange={(event) => setIsDemoModeEnabled(event.target.checked)}
          type="checkbox"
        />
        <span>Enable demo mode controls</span>
      </label>

      {isDemoModeEnabled ? (
        <div className="button-row">
          <button
            className="action-button action-button--primary"
            disabled={isRunning}
            onClick={() => onReset(selectedScenario)}
            type="button"
          >
            <RotateCcw aria-hidden="true" />
            Reset demo
          </button>
          <button
            className="action-button"
            disabled={isRunning}
            onClick={() => onSeed(selectedScenario)}
            type="button"
          >
            <Sprout aria-hidden="true" />
            Seed run
          </button>
        </div>
      ) : null}

      {message ? <p className="panel-message">{message}</p> : null}
    </section>
  );
}
