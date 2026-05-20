# RigSight AI

**AI-enabled autonomous test-rig monitoring sandbox using synthetic telemetry, anomaly detection, live dashboards, camera experiments, and human-in-the-loop alert review.**

RigSight AI is a clean-room public project designed to demonstrate applied AI and backend engineering for physical test and validation environments. It simulates a test rig with multiple sensor streams, injects realistic fault conditions, detects anomalies, and presents alerts through a React dashboard.

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
- Optional webcam/360 camera experiments using OpenCV

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

## Architecture

```text
Synthetic rig simulator / optional camera capture
        -> Backend ingestion API
        -> Database
        -> Anomaly detection service
        -> React dashboard and review workflow
```

## Clean-Room Statement

This project is built from scratch using synthetic data and generic engineering concepts. It does not include employer code, employer data, internal screenshots, internal architecture, proprietary workflows, or confidential information.

## Roadmap

- [x] Repository bootstrap
- [ ] Synthetic rig simulator
- [ ] Backend ingestion API
- [ ] Live dashboard
- [ ] Rules-based alerts
- [ ] ML anomaly detection
- [ ] Human review labels
- [ ] Camera lab
- [x] Docker Compose setup
- [ ] Screenshots and demo video
- [ ] Cloud infrastructure deployment plan

## Portfolio Summary

RigSight AI demonstrates applied AI engineering across telemetry ingestion, anomaly detection, backend API design, full-stack dashboards, and human-in-the-loop review workflows for synthetic autonomous test-rig environments.
