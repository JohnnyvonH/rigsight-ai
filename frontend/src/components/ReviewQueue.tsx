import { useState } from "react";

import type { AlertRecord, ReviewStatus } from "../api/client";
import { formatLabel, formatScore, formatTime } from "../utils/format";

type ReviewQueueProps = {
  isLoading: boolean;
  items: AlertRecord[];
  limit?: number;
  onReview: (alertId: number, reviewStatus: ReviewStatus, assignedTo?: string) => void;
  reviewingAlertId: number | null;
};

export function ReviewQueue({
  isLoading,
  items,
  limit,
  onReview,
  reviewingAlertId,
}: ReviewQueueProps) {
  const visibleItems = limit ? items.slice(0, limit) : items;
  const [assigneeByAlert, setAssigneeByAlert] = useState<Record<number, string>>({});

  if (visibleItems.length === 0) {
    return (
      <div className="empty-state" data-testid="review-empty">
        {isLoading ? "Loading review queue." : "All alerts reviewed."}
      </div>
    );
  }

  return (
    <div className="review-list" data-testid="review-queue">
      {visibleItems.map((alert) => (
        <article className="review-item" data-alert-id={alert.id} key={alert.id}>
          <span>{formatLabel(alert.detection_source)}</span>
          <strong>{alert.title}</strong>
          <p>
            {formatLabel(alert.alert_type)} - {formatTime(alert.timestamp)}
          </p>
          <dl className="review-detail-list">
            <div>
              <dt>Why flagged</dt>
              <dd>
                {alert.threshold_value !== null
                  ? `Observed ${alert.observed_value} exceeded ${alert.threshold_value}`
                  : `ML score ${formatScore(alert.anomaly_score)}`}
              </dd>
            </div>
            <div>
              <dt>Rig</dt>
              <dd>{alert.rig_id}</dd>
            </div>
            <div>
              <dt>Reviewer</dt>
              <dd>{alert.reviewed_by || "Unassigned"}</dd>
            </div>
          </dl>
          <label className="assignee-control">
            <span>Assign follow-up</span>
            <input
              onChange={(event) =>
                setAssigneeByAlert((current) => ({
                  ...current,
                  [alert.id]: event.target.value,
                }))
              }
              placeholder="Name or team"
              value={assigneeByAlert[alert.id] ?? alert.assigned_to}
            />
          </label>
          <div className="review-actions">
            <button
              disabled={reviewingAlertId === alert.id}
              onClick={() => onReview(alert.id, "confirmed", assigneeByAlert[alert.id])}
              type="button"
            >
              Confirm
            </button>
            <button
              disabled={reviewingAlertId === alert.id}
              onClick={() => onReview(alert.id, "dismissed", assigneeByAlert[alert.id])}
              type="button"
            >
              Dismiss
            </button>
            <button
              disabled={reviewingAlertId === alert.id}
              onClick={() => onReview(alert.id, "needs_followup", assigneeByAlert[alert.id])}
              type="button"
            >
              Follow up
            </button>
          </div>
        </article>
      ))}
    </div>
  );
}
