import { useState } from "react";

import type { AlertRecord } from "../api/client";
import { formatLabel, formatScore, formatTime } from "../utils/format";

type AlertTimelineProps = {
  alerts: AlertRecord[];
  isLoading: boolean;
  limit?: number;
};

export function AlertTimeline({ alerts, isLoading, limit = 8 }: AlertTimelineProps) {
  const visibleAlerts = alerts.slice(0, limit);
  const [expandedAlertId, setExpandedAlertId] = useState<number | null>(null);

  if (visibleAlerts.length === 0) {
    return (
      <div className="empty-state" data-testid="alerts-empty">
        {isLoading ? "Loading alerts from the API." : "No alerts found."}
      </div>
    );
  }

  return (
    <div className="alert-list" data-testid="alert-list">
      {visibleAlerts.map((alert) => (
        <article className={`alert-row alert-row--${alert.severity}`} key={alert.id}>
          <div>
            <span className="alert-row__meta">
              {formatTime(alert.timestamp)} - {formatLabel(alert.detection_source)} -{" "}
              {formatLabel(alert.alert_type)}
            </span>
            <h3>{alert.title}</h3>
            <p>{alert.message}</p>
            {expandedAlertId === alert.id ? (
              <dl className="alert-explainability">
                <div>
                  <dt>Rig</dt>
                  <dd>{alert.rig_id}</dd>
                </div>
                <div>
                  <dt>Why this fired</dt>
                  <dd>{alert.explanation || alert.message}</dd>
                </div>
                <div>
                  <dt>Expected</dt>
                  <dd>{alert.expected_range || "Baseline behavior"}</dd>
                </div>
                <div>
                  <dt>Action</dt>
                  <dd>{alert.recommended_action || "Review the linked reading."}</dd>
                </div>
              </dl>
            ) : null}
          </div>
          <dl>
            <div>
              <dt>Severity</dt>
              <dd>{alert.severity}</dd>
            </div>
            <div>
              <dt>Observed</dt>
              <dd>{alert.observed_value ?? formatScore(alert.anomaly_score)}</dd>
            </div>
            <div>
              <dt>Status</dt>
              <dd>{formatLabel(alert.review_status)}</dd>
            </div>
            <div>
              <dt>Details</dt>
              <dd>
                <button
                  className="inline-link-button"
                  onClick={() =>
                    setExpandedAlertId(expandedAlertId === alert.id ? null : alert.id)
                  }
                  type="button"
                >
                  {expandedAlertId === alert.id ? "Hide" : "Open"}
                </button>
              </dd>
            </div>
          </dl>
        </article>
      ))}
    </div>
  );
}
