import type { ReactNode } from "react";

type MetricCardProps = {
  label: string;
  value: string;
  detail: string;
  icon: ReactNode;
  tone?: "neutral" | "good" | "warning";
};

export function MetricCard({ label, value, detail, icon, tone = "neutral" }: MetricCardProps) {
  return (
    <section className={`metric-card metric-card--${tone}`}>
      <div className="metric-card__header">
        <span>{label}</span>
        <span className="metric-card__icon">{icon}</span>
      </div>
      <strong>{value}</strong>
      <p>{detail}</p>
    </section>
  );
}
