import { lazy, Suspense } from "react";
import { Navigate, Route, Routes } from "react-router-dom";

import { AppShell } from "./components/AppShell";

const Alerts = lazy(() => import("./pages/Alerts").then((module) => ({ default: module.Alerts })));
const Overview = lazy(() =>
  import("./pages/Overview").then((module) => ({ default: module.Overview })),
);
const Review = lazy(() => import("./pages/Review").then((module) => ({ default: module.Review })));
const Runs = lazy(() => import("./pages/Runs").then((module) => ({ default: module.Runs })));
const System = lazy(() => import("./pages/System").then((module) => ({ default: module.System })));
const Telemetry = lazy(() =>
  import("./pages/Telemetry").then((module) => ({ default: module.Telemetry })),
);

export default function App() {
  return (
    <Suspense fallback={<main className="workspace-main">Loading RigSight AI.</main>}>
      <Routes>
        <Route element={<AppShell />}>
          <Route element={<Overview />} index />
          <Route element={<Telemetry />} path="telemetry" />
          <Route element={<Alerts />} path="alerts" />
          <Route element={<Review />} path="review" />
          <Route element={<Runs />} path="runs" />
          <Route element={<System />} path="system" />
          <Route element={<Navigate replace to="/" />} path="*" />
        </Route>
      </Routes>
    </Suspense>
  );
}
