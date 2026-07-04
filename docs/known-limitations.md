# Known Limitations

- Default telemetry is synthetic and clean-room.
- The ML detector is a lightweight IsolationForest baseline, not a validated production model.
- Camera capture is disabled by default and local-only when enabled.
- The current pilot auth model is API-key based, not full SSO/RBAC.
- SQLite remains supported for local development; paid pilots should use managed Postgres.
- Review assignment and audit history are present, but notification delivery is not yet implemented.
- HTML reports are browser-printable but not a generated PDF file yet.
- Ingestion supports structured JSON; CSV upload is still a future UI feature.
