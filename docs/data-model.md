# Data Model

The planned data model includes:

- `test_runs`: a named execution window for a synthetic rig scenario
- `readings`: timestamped sensor telemetry for a run
- `alerts`: anomalies raised by rules or ML models
- `review_labels`: human-in-the-loop triage labels and notes
- `camera_snapshots`: optional local camera frames captured around interesting events

SQLite is used for the MVP. The schema should avoid SQLite-specific assumptions where practical so the project can move toward Postgres later.
