# Architecture

RigSight AI is organized as a small full-stack system:

```text
Synthetic Rig Simulator / Camera Capture
        |
        v
Backend API + Demo Control Service
        |
        +--> Database: readings, test runs, alerts, review labels
        |
        +--> Anomaly Detection Service
        |
        +--> Report Export + Optional Camera Status
        |
        v
React Dashboard
        |
        +--> Live status
        +--> Time-series charts
        +--> Alert timeline
        +--> Review queue
        +--> Test run history
        +--> Demo reset/seed controls
        +--> Camera lab status
```

## Backend

The backend is a FastAPI application with route modules for health, readings, alerts, runs, review, demo controls, report export, and optional camera experiments. SQLAlchemy is used for persistence, with SQLite for local development and a structure that can later map to Postgres.

On startup, the local demo environment seeds one deterministic synthetic run if no data exists. The demo API can reset or add deterministic scenarios. Rules-based detection persists threshold, drift, dropout, and power alerts. A lightweight IsolationForest baseline adds ML anomaly alerts for comparison.

## Frontend

The frontend is a Vite React application written in TypeScript. The dashboard displays backend health, latest readings, recent telemetry charts, rules-versus-ML alert summaries, local review queue, scenario controls, report export, optional camera status, and a guided 1.0 walkthrough.

## Data Source

All telemetry is synthetic. Optional camera features are disabled by default and only use local user-controlled camera inputs.
