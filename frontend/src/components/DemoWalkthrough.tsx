import { Activity, AlertTriangle, Database, FileText, ShieldCheck } from "lucide-react";
import { Link } from "react-router-dom";

const walkthroughSteps = [
  { to: "/runs", label: "Current run", icon: Database },
  { to: "/telemetry", label: "Telemetry", icon: Activity },
  { to: "/alerts", label: "Alerts", icon: AlertTriangle },
  { to: "/review", label: "Review", icon: ShieldCheck },
  { to: "/system", label: "System notes", icon: FileText },
];

export function DemoWalkthrough() {
  return (
    <section className="walkthrough-panel" aria-label="1.0 demo walkthrough">
      <div className="section-heading">
        <div>
          <p className="eyebrow">1.0 walkthrough</p>
          <h2>Demo path</h2>
        </div>
      </div>
      <div className="walkthrough-steps">
        {walkthroughSteps.map((step, index) => {
          const Icon = step.icon;
          return (
            <Link className="walkthrough-step" key={step.to} to={step.to}>
              <span>{index + 1}</span>
              <Icon aria-hidden="true" />
              <strong>{step.label}</strong>
            </Link>
          );
        })}
      </div>
    </section>
  );
}
