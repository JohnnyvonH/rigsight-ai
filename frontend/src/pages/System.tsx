import { FileText, GitBranch, Server, ShieldCheck } from "lucide-react";

import logoUrl from "../assets/rig-sight-ai-logo.png";
import { CameraPanel } from "../components/CameraPanel";
import { DemoWalkthrough } from "../components/DemoWalkthrough";
import { PageHeader } from "../components/PageHeader";
import { ThresholdPanel } from "../components/ThresholdPanel";
import { useRigSightData } from "../hooks/useRigSightData";

const systemSections = [
  {
    title: "Architecture",
    icon: Server,
    text: "FastAPI exposes health, runs, readings, alerts, review, and camera placeholder routes. SQLAlchemy persists the local SQLite demo data.",
  },
  {
    title: "Demo data",
    icon: GitBranch,
    text: "Startup seeds one deterministic synthetic endurance run with normal readings plus overheating, vibration, dropout, drift, and current anomaly windows.",
  },
  {
    title: "Clean room",
    icon: ShieldCheck,
    text: "All telemetry, alerts, labels, and workflow states are synthetic. The app does not include private code, private data, or proprietary test artifacts.",
  },
  {
    title: "Roadmap",
    icon: FileText,
    text: "The pilot path now emphasizes hosted staging, managed Postgres, tenant context, review audit history, ingestion, reports, and observability.",
  },
  {
    title: "Pilot limits",
    icon: ShieldCheck,
    text: "Demo data is synthetic, camera capture is disabled by default, ML scoring is a baseline, and uploaded pilot samples should avoid sensitive customer data.",
  },
  {
    title: "Observability",
    icon: Server,
    text: "Health, readiness, and metrics endpoints support deployment checks and basic operational monitoring before a customer pilot.",
  },
];

export function System() {
  const data = useRigSightData();

  return (
    <>
      <PageHeader
        description="Project context for reviewers: what is implemented, how demo data is generated, and what remains intentionally out of scope."
        eyebrow="System notes"
        title="Architecture and demo story"
      />

      <section className="brand-panel">
        <img src={logoUrl} alt="Rig-Sight AI logo concept" />
        <div>
          <p className="eyebrow">Brand asset</p>
          <h2>RigSight AI</h2>
          <p>
            The logo concept is now available inside the app shell and here as a full-size
            project identity reference for screenshots, walkthroughs, and future polish.
          </p>
        </div>
      </section>

      <section className="content-grid page-card-full">
        <CameraPanel cameraStatus={data.cameraStatus} />
        <ThresholdPanel
          currentRun={data.currentRun}
          isRunning={data.isThresholdActionRunning}
          message={data.thresholdActionMessage}
          onRecalculate={data.recalculateCurrentRunAlerts}
          onReset={data.resetCurrentThresholds}
          onSave={data.updateCurrentThresholds}
          thresholds={data.thresholds}
        />
      </section>

      <section className="content-grid page-card-full">
        <DemoWalkthrough />
        <aside className="info-panel">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Future auth</p>
              <h2>SSO/RBAC boundary</h2>
            </div>
            <ShieldCheck aria-hidden="true" />
          </div>
          <div className="explanation-list">
            <p>
              The pilot keeps API-key context for ingestion and review actions. Full SSO,
              customer identity mapping, and role enforcement remain deferred until a paid
              customer requires them.
            </p>
          </div>
        </aside>
      </section>

      <section className="system-grid">
        {systemSections.map((section) => {
          const Icon = section.icon;
          return (
            <article className="system-card" key={section.title}>
              <Icon aria-hidden="true" />
              <h2>{section.title}</h2>
              <p>{section.text}</p>
            </article>
          );
        })}
      </section>
    </>
  );
}
