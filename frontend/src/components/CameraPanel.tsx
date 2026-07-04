import { Camera, CameraOff } from "lucide-react";

import type { CameraStatusResponse } from "../api/client";
import { formatLabel } from "../utils/format";

type CameraPanelProps = {
  cameraStatus: CameraStatusResponse | null;
};

export function CameraPanel({ cameraStatus }: CameraPanelProps) {
  const isAvailable = cameraStatus?.status === "available";
  const Icon = isAvailable ? Camera : CameraOff;

  return (
    <section className="system-card camera-card">
      <Icon aria-hidden="true" />
      <h2>Camera lab</h2>
      <p>
        {cameraStatus?.message ??
          "Camera status is loading. The 1.0 release keeps camera capture optional and local."}
      </p>
      <dl className="compact-dl">
        <div>
          <dt>Status</dt>
          <dd>{formatLabel(cameraStatus?.status ?? "loading")}</dd>
        </div>
        <div>
          <dt>Enabled</dt>
          <dd>{cameraStatus?.enabled ? "Yes" : "No"}</dd>
        </div>
        <div>
          <dt>Snapshot</dt>
          <dd>{cameraStatus?.snapshot_available ? "Available" : "Unavailable"}</dd>
        </div>
      </dl>
    </section>
  );
}
