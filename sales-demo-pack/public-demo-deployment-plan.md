# RigSight AI Public Demo Deployment Plan

## Goal

Create a reliable private demo link for sales calls and pilot follow-up. This
should feel like a real product environment, but it should not imply full
self-serve SaaS readiness.

## Recommended First Deployment

Use a simple split deployment:

- Frontend: Vercel or Netlify hosting the Vite app.
- Backend: Render, Fly.io, Railway, or Azure Container Apps running FastAPI.
- Database: managed Postgres.
- Storage: no customer file retention for v1; parse CSV in browser and ingest
  JSON readings.
- Access: private demo URL protected by basic auth, platform password
  protection, or a lightweight reverse proxy.

## Environment Setup

Frontend variables:

```text
VITE_API_BASE_URL=https://api.demo.rigsight.ai
```

Backend variables:

```text
APP_ENV=demo
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/rigsight
BACKEND_CORS_ORIGINS=https://demo.rigsight.ai
PILOT_API_KEY=<generated-demo-key>
PILOT_ORGANIZATION_ID=demo-org
PILOT_ORGANIZATION_NAME=RigSight Demo Workspace
TELEMETRY_UPLOAD_ENABLED=true
CAMERA_ENABLED=false
```

## Deployment Steps

1. Create managed Postgres.
2. Deploy backend service from the repo.
3. Run Alembic migrations:

```bash
cd backend
python -m alembic upgrade head
```

4. Start backend and verify:

```bash
curl https://api.demo.rigsight.ai/ready
curl https://api.demo.rigsight.ai/api/v1/runs
```

5. Deploy frontend with `VITE_API_BASE_URL` pointing to backend.
6. Verify browser demo:
   - Overview loads.
   - Telemetry renders.
   - Alerts and review queue populate.
   - Runs page can download PDF.
   - System page loads thresholds.
7. Add uptime monitor for:
   - `/ready`
   - `/api/v1/runs`
8. Add a scheduled demo reset, either nightly or manually before each call.

## Demo Data Policy

- Use synthetic seeded data by default.
- Use prospect data only if sanitized and explicitly approved for the demo.
- Do not retain raw CSV files in v1.
- Do not enable camera capture in public demo.
- Make "Demo mode" visible when synthetic controls are available.

## Security Boundary For Demo

Minimum acceptable controls:

- Private demo URL.
- No open signup.
- No proprietary customer data in default demo.
- API CORS restricted to frontend origin.
- Demo database backed up or reseeded, but not treated as production evidence.
- Error logs should avoid raw telemetry payload dumps.

Not required for first guided demo:

- SSO.
- Full RBAC.
- Billing.
- Long-term customer data retention.
- Multi-tenant self-serve onboarding.

## Staging Smoke Checklist

Backend:

```bash
curl https://api.demo.rigsight.ai/health
curl https://api.demo.rigsight.ai/ready
curl https://api.demo.rigsight.ai/api/v1/thresholds?rig_id=synthetic-rig-01
curl -I https://api.demo.rigsight.ai/api/v1/reports/run/1/pdf
```

Frontend:

- Open demo URL in a clean browser profile.
- Confirm no console errors beyond known library warnings.
- Download the sample PDF.
- Import the CSV template after copying it and changing `run_name`.
- Reset demo state before the next prospect call.

## Suggested Timeline

Day 1:
- Provision managed Postgres.
- Deploy backend.
- Run migrations.
- Verify API health.

Day 2:
- Deploy frontend.
- Configure CORS and environment variables.
- Add uptime checks.
- Capture demo screenshots from the hosted URL.

Day 3:
- Run full sales script against hosted demo.
- Lock demo reset process.
- Prepare the prospect handoff email with demo URL, CSV template, and sample
  report.

## Recommended Next Build After Demo Deployment

1. Hosted demo reset button or admin command.
2. CSV mapping screen for alternate customer column names.
3. Branded report cover page with customer/run metadata.
4. Basic demo access gate.
5. Lightweight usage log for demo calls.
