const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init);

  if (!response.ok) {
    throw new Error(`${path} failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export type HealthResponse = {
  status: string;
  service: string;
  version: string;
  environment: string;
  timestamp: string;
};

export type TestRun = {
  id: number;
  organization_id: string;
  rig_id: string;
  name: string;
  scenario: string;
  status: string;
  started_at: string;
  ended_at: string | null;
  description: string;
};

export type Reading = {
  id: number;
  run_id: number;
  organization_id: string;
  rig_id: string;
  source: string;
  timestamp: string;
  phase: string;
  rpm: number;
  torque_nm: number;
  temperature_c: number;
  vibration_mm_s: number;
  current_a: number;
  voltage_v: number;
  pressure_bar: number;
  fault_mode: string | null;
};

export type LatestReadingResponse = {
  reading: Reading | null;
  run: TestRun | null;
};

export type ReadingHistoryResponse = {
  readings: Reading[];
  count: number;
};

export type RunsResponse = {
  runs: TestRun[];
  count: number;
};

export type AlertRecord = {
  id: number;
  run_id: number;
  reading_id: number;
  organization_id: string;
  rig_id: string;
  timestamp: string;
  severity: "low" | "medium" | "high" | string;
  alert_type: string;
  title: string;
  message: string;
  detection_source: "rules" | "ml" | string;
  observed_value: number | null;
  threshold_value: number | null;
  anomaly_score: number | null;
  ml_is_anomaly: boolean;
  explanation: string;
  recommended_action: string;
  triggered_metric: string;
  expected_range: string;
  actual_value: string;
  review_status: "unreviewed" | "confirmed" | "dismissed" | "needs_followup" | string;
  review_notes: string;
  assigned_to: string;
  reviewed_by: string;
  review_history: string;
  reviewed_at: string | null;
  reading: Reading;
  run: TestRun;
};

export type AlertsResponse = {
  alerts: AlertRecord[];
  count: number;
  total_count: number;
  limit: number;
  offset: number;
  summary: {
    unreviewed_count: number;
    rules_count: number;
    ml_count: number;
  };
};

export type ReviewQueueResponse = {
  items: AlertRecord[];
  count: number;
};

export type ReviewStatus = "unreviewed" | "confirmed" | "dismissed" | "needs_followup";

export type AlertFilters = {
  detectionSource?: string;
  reviewStatus?: string;
  runId?: number;
  severity?: string;
};

export type DemoScenario = {
  key: string;
  name: string;
  description: string;
  expected_faults: string[];
};

export type DemoSeedResponse = {
  run: TestRun;
  run_id: number;
  readings_created: number;
  alerts_created: number;
  scenarios: DemoScenario[];
};

export type DemoScenariosResponse = {
  scenarios: DemoScenario[];
};

export type CameraStatusResponse = {
  enabled: boolean;
  status: "disabled" | "available" | "unavailable" | string;
  message: string;
  device_index: number;
  snapshot_available: boolean;
};

export type RunReportResponse = {
  run: TestRun;
  latest_reading: Reading | null;
  top_alerts: AlertRecord[];
  thresholds: ThresholdProfile;
  summary: {
    reading_count: number;
    alert_count: number;
    high_alert_count: number;
    unreviewed_count: number;
    confirmed_count: number;
    rules_count: number;
    ml_count: number;
  };
  clean_room_note: string;
};

export type IngestReadingInput = {
  timestamp: string;
  phase?: string;
  rpm: number;
  torque_nm: number;
  temperature_c: number;
  vibration_mm_s: number;
  current_a: number;
  voltage_v: number;
  pressure_bar: number;
  fault_mode?: string | null;
};

export type IngestRunRequest = {
  name: string;
  rig_id: string;
  description: string;
  readings: IngestReadingInput[];
};

export type IngestRunResponse = {
  run: TestRun;
  readings_created: number;
  alerts_created: number;
};

export type ThresholdProfile = {
  organization_id: string;
  rig_id: string;
  temperature_high_c: number;
  temperature_critical_c: number;
  temperature_drift_c: number;
  vibration_high_mm_s: number;
  rpm_dropout: number;
  torque_dropout_nm: number;
  current_high_a: number;
  voltage_low_v: number;
  persisted: boolean;
};

export type ThresholdUpdate = Omit<ThresholdProfile, "organization_id" | "persisted">;

export type ThresholdResponse = {
  thresholds: ThresholdProfile;
  created?: boolean;
};

export function getHealth(init?: RequestInit): Promise<HealthResponse> {
  return fetchJson<HealthResponse>("/health", init);
}

export function getLatestReading(init?: RequestInit): Promise<LatestReadingResponse> {
  return fetchJson<LatestReadingResponse>("/readings/latest", init);
}

export function getReadingHistory(
  limit = 100,
  init?: RequestInit,
): Promise<ReadingHistoryResponse> {
  return fetchJson<ReadingHistoryResponse>(`/readings/history?limit=${limit}`, init);
}

export function getRuns(init?: RequestInit): Promise<RunsResponse> {
  return fetchJson<RunsResponse>("/runs", init);
}

export function getAlerts(
  limit = 50,
  init?: RequestInit,
  filters: AlertFilters = {},
): Promise<AlertsResponse> {
  const params = new URLSearchParams({ limit: String(limit) });
  if (filters.severity) params.set("severity", filters.severity);
  if (filters.detectionSource) params.set("detection_source", filters.detectionSource);
  if (filters.reviewStatus) params.set("review_status", filters.reviewStatus);
  if (filters.runId) params.set("run_id", String(filters.runId));
  return fetchJson<AlertsResponse>(`/alerts?${params.toString()}`, init);
}

export function getReviewQueue(init?: RequestInit): Promise<ReviewQueueResponse> {
  return fetchJson<ReviewQueueResponse>("/review/queue", init);
}

export function getDemoScenarios(init?: RequestInit): Promise<DemoScenariosResponse> {
  return fetchJson<DemoScenariosResponse>("/demo/scenarios", init);
}

export function resetDemoData(scenario: string): Promise<DemoSeedResponse> {
  return fetchJson<DemoSeedResponse>("/demo/reset", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ scenario }),
  });
}

export function seedDemoData(scenario: string): Promise<DemoSeedResponse> {
  return fetchJson<DemoSeedResponse>("/demo/seed", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ scenario }),
  });
}

export function getCameraStatus(init?: RequestInit): Promise<CameraStatusResponse> {
  return fetchJson<CameraStatusResponse>("/camera/status", init);
}

export function getRunReport(runId: number, init?: RequestInit): Promise<RunReportResponse> {
  return fetchJson<RunReportResponse>(`/reports/run/${runId}`, init);
}

export function getRunReportHtmlUrl(runId: number): string {
  return `${API_BASE_URL}/reports/run/${runId}/html`;
}

export function getRunReportPdfUrl(runId: number): string {
  return `${API_BASE_URL}/reports/run/${runId}/pdf`;
}

export function ingestReadings(payload: IngestRunRequest): Promise<IngestRunResponse> {
  return fetchJson<IngestRunResponse>("/readings/ingest", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export function getThresholds(rigId: string, init?: RequestInit): Promise<ThresholdResponse> {
  return fetchJson<ThresholdResponse>(`/thresholds?rig_id=${encodeURIComponent(rigId)}`, init);
}

export function updateThresholds(payload: ThresholdUpdate): Promise<ThresholdResponse> {
  return fetchJson<ThresholdResponse>("/thresholds", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export function resetThresholds(rigId: string): Promise<ThresholdResponse> {
  return fetchJson<ThresholdResponse>("/thresholds/reset", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ rig_id: rigId }),
  });
}

export function recalculateRunAlerts(runId: number): Promise<{ rules_count: number; ml_count: number }> {
  return fetchJson<{ rules_count: number; ml_count: number }>(
    `/runs/${runId}/alerts/recalculate`,
    {
      method: "POST",
    },
  );
}

export function updateAlertReview(
  alertId: number,
  reviewStatus: ReviewStatus,
  reviewNotes = "",
  assignedTo = "",
): Promise<{ alert: AlertRecord }> {
  return fetchJson<{ alert: AlertRecord }>(`/review/${alertId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      review_status: reviewStatus,
      review_notes: reviewNotes,
      assigned_to: assignedTo,
    }),
  });
}
