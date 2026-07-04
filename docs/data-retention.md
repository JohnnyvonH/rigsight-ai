# Data Retention Policy

This policy describes the intended pilot behavior for RigSight AI.

## Demo Data

Synthetic demo data can be reset at any time. It has no retention guarantee and should not be used as a customer record.

## Pilot Data

Pilot telemetry should be retained only for the agreed pilot period. A default target is 30-90 days unless the customer requests earlier deletion.

## Reports

Exported JSON and HTML reports are customer artifacts. Store them in the customer-approved location and avoid committing them to the repository.

## Deletion

Before production, RigSight needs an operator workflow for deleting a pilot workspace, including runs, readings, alerts, review notes, and generated reports.
