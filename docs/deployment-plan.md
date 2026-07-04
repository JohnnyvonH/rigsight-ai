# Cloud Deployment Plan

RigSight AI 1.0 does not require a live hosted deployment. The intended cloud path is a lightweight staging environment that proves the app can move beyond local Docker.

## Recommended 1.1 Path

- Frontend: Vercel, Netlify, or static hosting for the Vite build.
- Backend: containerized FastAPI service on Render, Fly.io, Railway, Azure Container Apps, AWS ECS, or GCP Cloud Run.
- Database: managed Postgres.
- Storage: optional object storage for future camera snapshots and exported reports.
- Secrets: environment variables managed by the hosting provider.
- Observability: provider logs plus basic uptime checks.

## Pilot Environment Variables

- `DATABASE_URL`: managed Postgres connection string.
- `BACKEND_CORS_ORIGINS`: deployed frontend origin.
- `PILOT_API_KEY`: shared pilot ingestion/review key until SSO is implemented.
- `PILOT_ORGANIZATION_ID`: stable customer workspace identifier.
- `PILOT_ORGANIZATION_NAME`: customer-facing workspace name.
- `TELEMETRY_UPLOAD_ENABLED`: disable if a pilot is demo-only.

## Postgres Pilot Path

Local Postgres smoke path:

```bash
docker compose --profile postgres up -d postgres
cd backend
DATABASE_URL=postgresql+psycopg://rigsight:rigsight@localhost:5432/rigsight alembic upgrade head
DATABASE_URL=postgresql+psycopg://rigsight:rigsight@localhost:5432/rigsight uvicorn app.main:app --reload
```

Managed Postgres staging should run `alembic upgrade head` before starting the backend. Backups should be enabled before customer telemetry import, even for sanitized pilot data.

## Deployment Checks

- `GET /health`: process liveness.
- `GET /ready`: database readiness and run-count check.
- `GET /metrics`: basic JSON counters for runs, readings, alerts, and review backlog.
- `GET /api/v1/runs`: versioned API smoke check.
- `GET /api/v1/thresholds`: threshold profile check.
- `GET /api/v1/reports/run/{run_id}/pdf`: PDF generation check after demo data exists.

## CI/CD Direction

The current CI runs backend lint/tests, frontend build, Docker build, and Docker smoke checks. A later staging deployment can add:

- image publishing
- environment-specific database URL
- migration step
- smoke checks against staging URLs
- preview deployment links for pull requests
- database backup verification
- object storage for generated customer reports if reports are retained server-side

## Non-Goals For 1.0

- No mandatory live cloud environment
- No auth
- No external notification system
- No production camera capture
