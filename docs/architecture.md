# Architecture

RigSight AI is organized as a small full-stack system:

```text
Synthetic Rig Simulator / Camera Capture
        |
        v
Backend API + Ingestion Service
        |
        +--> Database: readings, test runs, alerts, review labels
        |
        +--> Anomaly Detection Service
        |
        v
React Dashboard
        |
        +--> Live status
        +--> Time-series charts
        +--> Alert timeline
        +--> Review queue
        +--> Test run history
```

## Backend

The backend is a FastAPI application with route modules for health, readings, alerts, runs, review, and optional camera experiments. SQLAlchemy is used for persistence, with SQLite for local development and a structure that can later map to Postgres.

## Frontend

The frontend is a Vite React application written in TypeScript. The first milestone provides a dashboard shell and API health check. Later milestones will add live telemetry, charts, alerts, and review workflows.

## Data Source

All telemetry is synthetic. Optional camera features are disabled by default and only use local user-controlled camera inputs.
