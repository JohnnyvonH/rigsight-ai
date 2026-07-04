import { AlertTriangle, CheckCircle2 } from "lucide-react";

import { MetricCard } from "../components/MetricCard";
import { PageHeader } from "../components/PageHeader";
import { ReviewQueue } from "../components/ReviewQueue";
import { useRigSightData } from "../hooks/useRigSightData";

export function Review() {
  const data = useRigSightData();
  const reviewedCount = Math.max(
    0,
    data.alerts.length - data.alerts.filter((alert) => alert.review_status === "unreviewed").length,
  );

  return (
    <>
      <PageHeader
        description="Triage synthetic detections with local review labels. No auth or external notifications are included in this MVP."
        eyebrow="Human-in-the-loop"
        title="Review queue"
      />

      <section className="split-panel split-panel--summary">
        <div className="metric-strip" aria-label="Review summary">
          <MetricCard
            detail="Loaded alerts still waiting for a decision."
            icon={<AlertTriangle aria-hidden="true" />}
            label="Queued alerts"
            tone={data.reviewQueue.length > 0 ? "warning" : "good"}
            value={String(data.reviewQueue.length)}
          />
          <MetricCard
            detail="Confirmed, dismissed, or marked for follow-up in this loaded window."
            icon={<CheckCircle2 aria-hidden="true" />}
            label="Reviewed"
            tone="good"
            value={String(reviewedCount)}
          />
        </div>

        <aside className="info-panel">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Review labels</p>
              <h2>Status model</h2>
            </div>
            <CheckCircle2 aria-hidden="true" />
          </div>
          <div className="explanation-list">
            <p>Confirmed alerts represent plausible synthetic faults.</p>
            <p>Dismissed alerts are false positives in the demo workflow.</p>
            <p>Follow-up alerts are preserved for later investigation or notes.</p>
          </div>
        </aside>
      </section>

      <section className="chart-card page-card-full">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Queue actions</p>
            <h2>Unreviewed alerts</h2>
          </div>
          <span>{data.alertSummary?.unreviewed_count ?? data.reviewQueue.length} total</span>
        </div>
        <ReviewQueue
          isLoading={data.isLoading}
          items={data.reviewQueue}
          limit={12}
          onReview={data.handleReview}
          reviewingAlertId={data.reviewingAlertId}
        />
      </section>
    </>
  );
}
