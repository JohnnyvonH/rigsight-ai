# RigSight AI 1.0 Release Checklist

Use this checklist before tagging the 1.0 release.

## Local Verification

- [ ] `python -m pytest` passes in `backend`
- [ ] `python -m ruff check app` passes in `backend`
- [ ] `npm run build` passes in `frontend`
- [ ] `docker compose up --build -d` starts both services
- [ ] `GET http://localhost:8000/health` returns version `1.0.0`
- [ ] `GET http://localhost:8000/runs` returns at least one run
- [ ] `GET http://localhost:8000/readings/latest` returns run context
- [ ] `GET http://localhost:8000/alerts` returns rules and ML summary counts
- [ ] `GET http://localhost:8000/camera/status` returns disabled or unavailable safely
- [ ] `GET http://localhost:8000/reports/run/{run_id}` returns a run summary

## Browser Verification

- [ ] `/` renders overview, rig controls, metrics, and walkthrough
- [ ] `/telemetry` renders the chart and scenario explanation
- [ ] `/alerts` renders the detection summary and alert timeline
- [ ] `/review` renders review actions and updates state
- [ ] `/runs` renders scenario controls, run list, and report export
- [ ] `/system` renders architecture notes, camera lab, and clean-room context
- [ ] Mobile navigation has no horizontal overflow

## Portfolio Assets

- [ ] Capture screenshots for Overview, Telemetry, Alerts, Review, Runs, and System
- [ ] Capture a short demo GIF/video showing reset -> telemetry -> alerts -> review -> report export
- [ ] Confirm screenshots do not show private data, private spaces, or proprietary artifacts
