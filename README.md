# RigSight AI

**AI-enabled autonomous test-rig monitoring sandbox using synthetic telemetry, anomaly detection, live dashboards, camera experiments, and human-in-the-loop alert review.**

RigSight AI 1.0 is a clean-room public project designed to demonstrate applied AI and backend engineering for physical test and validation environments. It simulates a test rig with multiple sensor streams, injects realistic fault conditions, detects anomalies, and presents alerts through a multi-page React monitoring workspace.

## Why This Exists

Engineering test teams often generate large volumes of telemetry across sensors, rigs, devices, and validation runs. Manually reviewing that data can be slow, inconsistent, and reactive. RigSight AI explores how applied AI and good software architecture can help surface anomalies earlier, improve visibility, and support better engineering decisions.

## Core Features

- Synthetic rig telemetry generator
- Multi-sensor readings and test phases
- Fault injection for overheating, vibration spikes, sensor dropout, drift, and current anomalies
- FastAPI backend with REST endpoints
- SQL-backed readings, runs, alerts, and review labels
- Rules-based anomaly detection baseline
- ML-based anomaly scoring with scikit-learn
- React dashboard for live status and time-series charts
- Alert triage and human-in-the-loop review workflow
- Demo reset/seed controls with multiple deterministic scenarios
- JSON run report export
- Browser-printable HTML run report
- Versioned `/api/v1` API surface
- Pilot telemetry ingestion endpoint for sanitized customer samples
- CSV telemetry import workflow in the frontend
- Configurable alert thresholds per rig
- Rules-based alert recalculation after threshold updates
- PDF run report export
- Alert explanations and recommended actions
- Review assignment and audit history fields
- Health, readiness, and metrics endpoints for deployment checks
- Optional local camera lab, disabled by default
- Docker Compose and CI smoke checks

## Tech Stack

- Python, FastAPI, SQLAlchemy, scikit-learn, OpenCV
- React, Vite, TypeScript, Recharts
- SQLite locally with a Postgres-compatible data model direction
- Docker Compose

## Quick Start

```bash
docker compose up --build
```

Then open:

- Backend health: http://localhost:8000/health
- API docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

## Demo Data

On startup, the backend creates a deterministic synthetic endurance run when the local database is empty. The app can reset or seed demo data with these scenarios:

- `baseline-with-seeded-faults`: normal operation plus overheating, vibration, dropout, drift, and current anomaly windows
- `normal-baseline`: normal readings with no seeded faults
- `fault-heavy-validation`: stronger fault windows for a denser alert demo

Rules-based alerts and IsolationForest ML anomaly alerts are persisted so the dashboard has telemetry, alert, and review data immediately.

Key API routes:

- `GET /runs`
- `GET /api/v1/runs`
- `GET /readings/latest`
- `GET /readings/history?limit=100`
- `POST /readings/ingest`
- `GET /thresholds?rig_id=synthetic-rig-01`
- `PATCH /thresholds`
- `POST /thresholds/reset`
- `POST /runs/{run_id}/alerts/recalculate`
- `GET /alerts?limit=50`
- `GET /review/queue`
- `PATCH /review/{alert_id}`
- `GET /demo/scenarios`
- `POST /demo/reset`
- `POST /demo/seed`
- `GET /camera/status`
- `GET /reports/run/{run_id}`
- `GET /reports/run/{run_id}/html`
- `GET /reports/run/{run_id}/pdf`
- `GET /ready`
- `GET /metrics`

## 1.0 Demo Walkthrough

1. Start with `docker compose up --build`.
2. Open the Overview page and confirm backend health, latest readings, and review counts.
3. Use Rig Controls to reset the demo to a baseline, normal, or fault-heavy scenario.
4. Open Telemetry to inspect sensor trends and seeded fault windows.
5. Open Alerts to compare rules-based detections with ML anomaly scoring.
6. Open Review to confirm, dismiss, or mark alerts for follow-up.
7. Open Runs to export a JSON run report.
8. Open System Notes for architecture, camera lab status, and clean-room context.

## Local Development

Backend:

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Postgres pilot profile:

```bash
docker compose --profile postgres up -d postgres
cd backend
$env:DATABASE_URL="postgresql+psycopg://rigsight:rigsight@localhost:5432/rigsight"
alembic upgrade head
uvicorn app.main:app --reload
```

## Architecture

```text
Synthetic rig simulator / optional camera capture
        -> Backend ingestion API
        -> Database
        -> Anomaly detection service
        -> React dashboard and review workflow
```

Detailed docs:

- [Architecture](docs/architecture.md)
- [Data model](docs/data-model.md)
- [Camera lab](docs/camera-lab.md)
- [Cloud deployment plan](docs/deployment-plan.md)
- [Release checklist](docs/release-checklist.md)
- [Demo media guide](docs/demo-media.md)
- [Pilot onboarding guide](docs/pilot-onboarding.md)
- [Privacy and security notes](docs/privacy-security.md)
- [Data retention policy](docs/data-retention.md)
- [Known limitations](docs/known-limitations.md)
- [Customer demo script](docs/customer-demo-script.md)

## Clean-Room Statement

This project is built from scratch using synthetic data and generic engineering concepts. It does not include employer code, employer data, internal screenshots, internal architecture, proprietary workflows, or confidential information.

## Roadmap

- [x] Repository bootstrap
- [x] Synthetic rig simulator
- [x] Backend ingestion API
- [x] Live dashboard
- [x] Rules-based alerts
- [x] ML anomaly detection
- [x] Human review labels
- [x] Optional camera lab status
- [x] Docker Compose setup
- [x] Demo media capture guide
- [x] Cloud infrastructure deployment plan
- [x] Run report export
- [x] CI Docker smoke checks
- [x] Versioned API routing
- [x] Pilot ingestion endpoint
- [x] Review audit metadata
- [x] HTML report view
- [x] Readiness and metrics endpoints
- [x] CSV import workflow
- [x] Configurable thresholds
- [x] PDF report export
- [x] Postgres migration path

## Portfolio Summary

RigSight AI demonstrates applied AI engineering across telemetry ingestion, anomaly detection, backend API design, full-stack dashboards, and human-in-the-loop review workflows for synthetic autonomous test-rig environments.
