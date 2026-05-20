import { Activity, AlertTriangle, CheckCircle2, Gauge, RadioTower } from "lucide-react";
import { useEffect, useState } from "react";

import { getHealth, type HealthResponse } from "../api/client";
import { MetricCard } from "../components/MetricCard";

const roadmapItems = [
  "Synthetic telemetry generator",
  "Fault injection controls",
  "Rules and ML anomaly detection",
  "Human review queue",
  "Optional camera lab",
];

export function Dashboard() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthError, setHealthError] = useState<string | null>(null);

  useEffect(() => {
    let ignore = false;

    getHealth()
      .then((result) => {
        if (!ignore) {
          setHealth(result);
          setHealthError(null);
        }
      })
      .catch((error: Error) => {
        if (!ignore) {
          setHealthError(error.message);
        }
      });

    return () => {
      ignore = true;
    };
  }, []);

  return (
    <main className="app-shell">
      <nav className="topbar" aria-label="Primary navigation">
        <a className="brand" href="/">
          <span className="brand__mark">RS</span>
          <span>RigSight AI</span>
        </a>
        <div className="topbar__links" aria-label="Roadmap sections">
          <a href="#dashboard">Dashboard</a>
          <a href="#architecture">Architecture</a>
          <a href="#roadmap">Roadmap</a>
        </div>
      </nav>

      <section className="hero" id="dashboard">
        <div className="hero__copy">
          <h1>Autonomous test-rig monitoring with synthetic telemetry.</h1>
          <p>
            A clean-room sandbox for streaming sensor data, detecting anomalies, triaging
            alerts, and reviewing test-run history without private code or data.
          </p>
        </div>

        <div className="status-panel" aria-live="polite">
          <div className="status-panel__header">
            <div>
              <span>Backend health</span>
              <strong>{health?.status === "ok" ? "Online" : "Waiting"}</strong>
            </div>
            {health?.status === "ok" ? (
              <CheckCircle2 aria-hidden="true" />
            ) : (
              <RadioTower aria-hidden="true" />
            )}
          </div>
          <dl>
            <div>
              <dt>Service</dt>
              <dd>{health?.service ?? "rigsight-api"}</dd>
            </div>
            <div>
              <dt>Environment</dt>
              <dd>{health?.environment ?? "development"}</dd>
            </div>
            <div>
              <dt>Last check</dt>
              <dd>{health ? new Date(health.timestamp).toLocaleTimeString() : "Pending"}</dd>
            </div>
          </dl>
          {healthError ? <p className="status-panel__error">{healthError}</p> : null}
        </div>
      </section>

      <section className="metrics-grid" aria-label="MVP status cards">
        <MetricCard
          label="Rig health"
          value="Nominal"
          detail="Seeded synthetic readings arrive in the next milestone."
          icon={<Gauge aria-hidden="true" />}
          tone="good"
        />
        <MetricCard
          label="Telemetry"
          value="Skeleton"
          detail="Readings routes are in place for latest and historical data."
          icon={<Activity aria-hidden="true" />}
        />
        <MetricCard
          label="Alerts"
          value="Planned"
          detail="Rules and ML alerts will feed this panel as the simulator lands."
          icon={<AlertTriangle aria-hidden="true" />}
          tone="warning"
        />
      </section>

      <section className="content-band" id="architecture">
        <div>
          <h2>System shape</h2>
          <p>
            The MVP starts with a FastAPI ingestion layer and a React dashboard. The next
            slice adds stored readings, seeded fault modes, time-windowed history, and live
            chart updates.
          </p>
        </div>
        <ol className="flow-list">
          <li>Synthetic rig simulator</li>
          <li>Backend API and database</li>
          <li>Anomaly detection service</li>
          <li>Dashboard and review workflow</li>
        </ol>
      </section>

      <section className="roadmap" id="roadmap">
        <h2>Next build slices</h2>
        <ul>
          {roadmapItems.map((item) => (
            <li key={item}>
              <CheckCircle2 aria-hidden="true" />
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
