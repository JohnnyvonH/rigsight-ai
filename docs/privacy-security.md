# Privacy And Security Notes

RigSight AI is clean-room software using synthetic default data. For pilots, treat imported telemetry as customer confidential even when it is non-sensitive sample data.

## Current Controls

- Optional API-key check through `PILOT_API_KEY`.
- Organization and rig identifiers on runs, readings, and alerts.
- Review audit history with actor, role, status transition, assignee, and notes.
- CORS allowlist configured through `BACKEND_CORS_ORIGINS`.
- Camera capture disabled by default.

## Required Before Production

- Replace pilot API key with full identity provider integration.
- Enforce role-based access for admin, reviewer, and read-only users.
- Add managed secrets, encrypted backups, and database-level access controls.
- Add rate limits and request size limits to ingestion.
- Add formal vulnerability scanning and dependency update automation.

## Data Handling

Do not upload employer data, customer secrets, proprietary rig identifiers, or personal data to the demo environment. Use sanitized pilot extracts until customer contracts and production controls are in place.
