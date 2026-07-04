# Known Limitations

- Default telemetry is synthetic and clean-room.
- The ML detector is a lightweight IsolationForest baseline, not a validated production model.
- Camera capture is disabled by default and local-only when enabled.
- The current pilot auth model is API-key based, not full SSO/RBAC.
- SQLite remains supported for local development; paid pilots should use managed Postgres.
- Review assignment and audit history are present, but notification delivery is not yet implemented.
- PDF reports are generated on demand and are not retained server-side.
- CSV upload parses files in the browser and sends structured JSON ingestion payloads.
- Threshold profiles are rig-scoped but do not yet include a full approval workflow.
- Full SSO/RBAC is deferred until a paying customer requires identity-provider integration.
