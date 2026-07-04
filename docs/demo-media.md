# Demo Media Guide

Capture these assets after the UI is accepted for the 1.0 release.

## Screenshots

- Overview: backend health, rig controls, latest metrics, and walkthrough
- Telemetry: chart plus scenario/fault explanation
- Alerts: rules vs ML summary and alert timeline
- Review: queue with review buttons
- Runs: scenario controls, report export, and run list
- System: logo, architecture notes, camera lab, and clean-room note

## Demo GIF / Video

Recommended flow:

1. Start from `docker compose up --build`.
2. Open `http://localhost:5173`.
3. Reset to `fault-heavy-validation`.
4. Open Telemetry and show the chart.
5. Open Alerts and show rules/ML detections.
6. Open Review and confirm one alert.
7. Open Runs and export the JSON report.
8. End on System Notes with the clean-room statement.

Keep the clip under two minutes and avoid showing local files, terminal secrets, browser profiles, or private directories.
