import {
  Activity,
  AlertTriangle,
  Database,
  FileText,
  Gauge,
  Home,
  ShieldCheck,
} from "lucide-react";
import type { ComponentType, SVGProps } from "react";

export type AppRoute = {
  path: string;
  label: string;
  icon: ComponentType<SVGProps<SVGSVGElement>>;
};

export const appRoutes: AppRoute[] = [
  { path: "/", label: "Overview", icon: Home },
  { path: "/telemetry", label: "Telemetry", icon: Activity },
  { path: "/alerts", label: "Alerts", icon: AlertTriangle },
  { path: "/review", label: "Review", icon: ShieldCheck },
  { path: "/runs", label: "Runs", icon: Database },
  { path: "/system", label: "System", icon: FileText },
];

export const pageTitles = {
  overview: "Operations overview",
  telemetry: "Telemetry analysis",
  alerts: "Detection workspace",
  review: "Human review queue",
  runs: "Synthetic run history",
  system: "System notes",
} as const;

export const OverviewIcon = Gauge;
