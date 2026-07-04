# RigSight AI Sales Demo Script

## Demo Goal

Show an engineering validation team that RigSight can turn sanitized telemetry
into a practical review workflow: import data, see run health, investigate
alerts, make review decisions, and export a customer-ready report.

## Positioning

RigSight is not being sold as a broad enterprise monitoring platform yet. The
first offer is a guided paid pilot for teams that already collect sensor data
but spend too much time reviewing anomalies and assembling run evidence.

## Opening

"Most test teams already have the data. The harder part is deciding what
changed, whether it matters, who reviewed it, and what evidence gets sent after
the run. RigSight is designed to make that workflow faster using sanitized CSV
telemetry, configurable thresholds, explainable alerts, and report export."

## Demo Flow

### 1. Start On Overview

Page: `Overview`

Point to:
- Fleet health: action required.
- Current run: active run is the primary workspace object.
- High alerts and review backlog.
- Latest phase and top risk.

Talk track:
"The first screen is intentionally operational. We are not leading with system
health or architecture. The team sees the active run, the current risk state,
and what needs review."

Transition:
"From here, the natural question is what changed in the telemetry."

### 2. Show Telemetry Investigation

Page: `Telemetry`

Point to:
- Sensor trend chart.
- Current phase.
- Latest reading cards.
- Fault-window context.

Talk track:
"This is where an engineer can inspect the sensor behavior behind the alert
queue. The important point is that alerts are tied back to run readings, not
detached from the test context."

Transition:
"Now we can look at how the system explains what it found."

### 3. Show Alerts And Explainability

Page: `Alerts`

Point to:
- Rule alert count.
- ML anomaly count.
- Filters.
- Open an alert detail if presenting live.

Talk track:
"Rules catch known threshold and dropout conditions. The ML baseline catches
unusual cross-sensor combinations. The alert detail explains why it fired, what
value was observed, what range was expected, and the recommended next action."

Optional line:
"This is intentionally explainable before it is fully automated. The pilot goal
is to help engineers review faster, not replace their judgment."

Transition:
"The next step is the human decision."

### 4. Show Review Queue

Page: `Review`

Point to:
- Unreviewed alert cards.
- Why flagged.
- Recommended action.
- Assignment field.
- Confirm, dismiss, follow-up buttons.

Talk track:
"This turns detection into a review process. A team can assign follow-up,
confirm or dismiss alerts, and keep the decision with the run evidence."

Transition:
"Now we can show how a prospect gets their own data into the workflow."

### 5. Show CSV Import And Report Export

Page: `Runs`

Point to:
- CSV telemetry import.
- CSV contract.
- Report summary.
- Download PDF.
- Export JSON.

Talk track:
"For a pilot, we do not need a heavy integration on day one. A prospect can
share sanitized CSV telemetry using the template, preview validation, import
the readings, and then use the same review workflow."

Use the provided CSV:
`sales-demo-pack/rigsight-pilot-import-template.csv`

Use the provided report:
`sales-demo-pack/sample-run-report.pdf`

Transition:
"If their rig has different operating limits, we can tune the rules."

### 6. Show Threshold Tuning

Page: `System`

Point to:
- Alert thresholds panel.
- Temperature, vibration, current, voltage, dropout settings.
- Recalculate alerts.
- SSO/RBAC boundary note.

Talk track:
"Thresholds are configurable by rig. If the customer has known limits, those
can be set before the pilot review. We are intentionally deferring SSO and RBAC
until a real customer asks for it, because the immediate pilot value is data
ingestion, detection, review, and reporting."

## Close

"The pilot offer is simple: send us a sanitized CSV from one test run, we tune
the thresholds with your engineer, run the data through RigSight, review the
alerts together, and deliver a report. If the workflow saves review time or
improves confidence in run decisions, we scope the next integration."

## Discovery Questions

- How do you review failed or suspicious test runs today?
- Where does the telemetry live after a run?
- Which thresholds are currently checked manually?
- Who decides whether an anomaly is real?
- What evidence goes into the final run report?
- Could you provide a sanitized CSV sample for a pilot?
- What would make a 4-6 week pilot worth paying for?

## Suggested Pilot Offer

- Duration: 4-6 weeks.
- Inputs: 1-3 sanitized CSV test runs.
- Setup: threshold configuration for one rig or test stand.
- Workflow: alert triage, review decisions, notes/follow-up, report export.
- Output: sample run reports and pilot findings.
- Success criteria: faster review, clearer anomaly explanation, reusable report
  evidence, and customer confidence in next integration.
