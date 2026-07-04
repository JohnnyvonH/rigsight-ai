# Data Model

The planned data model includes:

- `test_runs`: a named execution window for a synthetic rig scenario
- `readings`: timestamped sensor telemetry for a run
- `alerts`: anomalies raised by rules or ML models
- `review_labels`: human-in-the-loop triage labels and notes
- `camera_snapshots`: optional local camera frames captured around interesting events
- `run_reports`: generated JSON summaries derived from existing run, reading, alert, and review data

SQLite is used for the MVP. The schema should avoid SQLite-specific assumptions where practical so the project can move toward Postgres later.

Current 1.0 implementation persists `test_runs`, `readings`, and `alerts`. Alert records include the detection source (`rules` or `ml`), severity, linked reading/run context, optional threshold/observed values, optional ML anomaly score, and review status/notes. Run reports are generated on demand and do not require a separate table.
