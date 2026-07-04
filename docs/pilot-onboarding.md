# Pilot Onboarding Guide

RigSight AI is currently best suited to a paid pilot with an engineering test or validation team.

## Pilot Setup

1. Deploy the backend to a staging environment with managed Postgres.
2. Deploy the Vite frontend with `VITE_API_BASE_URL` pointing at the backend.
3. Configure `PILOT_API_KEY` for telemetry ingestion and review updates.
4. Set `PILOT_ORGANIZATION_ID` and `PILOT_ORGANIZATION_NAME` for the pilot workspace.
5. Keep demo controls enabled only for demonstrations and synthetic reset flows.
6. Configure alert thresholds for the pilot rig before reviewing imported data.

## Data Intake

Pilot customers can import non-sensitive sample telemetry through the Runs page CSV workflow or send structured telemetry to `POST /api/v1/readings/ingest`.

Required sensor fields:

- timestamp
- rpm
- torque_nm
- temperature_c
- vibration_mm_s
- current_a
- voltage_v
- pressure_bar

Imported data should avoid customer secrets, proprietary labels, personal data, and confidential test identifiers.

## Pilot Success Criteria

- Customer can load realistic sample telemetry.
- Test engineers can identify high-risk windows quickly.
- Review decisions are captured with reviewer and assignment context.
- A run report can be shared as HTML or printed to PDF.
- A generated PDF report can be downloaded for pilot readouts.
- Staging health, readiness, and metrics endpoints are monitored.
