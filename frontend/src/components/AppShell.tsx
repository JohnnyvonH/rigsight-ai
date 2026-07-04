import { NavLink, Outlet } from "react-router-dom";

import logoUrl from "../assets/rig-sight-ai-logo.png";
import { appRoutes } from "../routes";

export function AppShell() {
  return (
    <div className="workspace-shell">
      <aside className="sidebar" aria-label="Application navigation">
        <a className="brand" href="/" aria-label="RigSight AI overview">
          <img className="brand__image" src={logoUrl} alt="" />
          <span>
            RigSight AI
            <small>Track - Detect - Prevent</small>
          </span>
        </a>
        <nav className="sidebar__nav">
          {appRoutes.map((route) => {
            const Icon = route.icon;
            return (
              <NavLink
                className={({ isActive }) =>
                  isActive ? "sidebar__link sidebar__link--active" : "sidebar__link"
                }
                end={route.path === "/"}
                key={route.path}
                to={route.path}
              >
                <Icon aria-hidden="true" />
                <span>{route.label}</span>
              </NavLink>
            );
          })}
        </nav>
      </aside>
      <main className="workspace-main">
        <Outlet />
      </main>
    </div>
  );
}
