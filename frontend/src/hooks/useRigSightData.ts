import { useCallback, useEffect, useMemo, useState } from "react";

import {
  getAlerts,
  getCameraStatus,
  getDemoScenarios,
  getHealth,
  getLatestReading,
  getReadingHistory,
  getReviewQueue,
  getRunReport,
  getRunReportHtmlUrl,
  getRuns,
  resetDemoData,
  seedDemoData,
  updateAlertReview,
  type AlertRecord,
  type AlertsResponse,
  type CameraStatusResponse,
  type DemoScenario,
  type HealthResponse,
  type Reading,
  type ReviewStatus,
  type RunReportResponse,
  type TestRun,
} from "../api/client";
import { formatLabel } from "../utils/format";

export type RigSightData = {
  alertSummary: AlertsResponse["summary"] | null;
  alerts: AlertRecord[];
  cameraStatus: CameraStatusResponse | null;
  currentRun: TestRun | null;
  demoActionMessage: string | null;
  error: string | null;
  exportRunReport: () => void;
  exportRunReportHtml: () => void;
  handleReview: (alertId: number, reviewStatus: ReviewStatus, assignedTo?: string) => void;
  health: HealthResponse | null;
  highSeverityCount: number;
  history: Reading[];
  isLoading: boolean;
  isOnline: boolean;
  isDemoActionRunning: boolean;
  latestAlerts: AlertRecord[];
  latestFault: string | null;
  latestReading: Reading | null;
  loadTelemetry: (signal?: AbortSignal) => void;
  report: RunReportResponse | null;
  resetDemo: (scenario: string) => void;
  reviewQueue: AlertRecord[];
  reviewingAlertId: number | null;
  runs: TestRun[];
  scenarios: DemoScenario[];
  seedDemo: (scenario: string) => void;
};

export function useRigSightData(): RigSightData {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [latestReading, setLatestReading] = useState<Reading | null>(null);
  const [currentRun, setCurrentRun] = useState<TestRun | null>(null);
  const [runs, setRuns] = useState<TestRun[]>([]);
  const [history, setHistory] = useState<Reading[]>([]);
  const [alerts, setAlerts] = useState<AlertRecord[]>([]);
  const [alertSummary, setAlertSummary] = useState<AlertsResponse["summary"] | null>(null);
  const [reviewQueue, setReviewQueue] = useState<AlertRecord[]>([]);
  const [scenarios, setScenarios] = useState<DemoScenario[]>([]);
  const [cameraStatus, setCameraStatus] = useState<CameraStatusResponse | null>(null);
  const [report, setReport] = useState<RunReportResponse | null>(null);
  const [reviewingAlertId, setReviewingAlertId] = useState<number | null>(null);
  const [isDemoActionRunning, setIsDemoActionRunning] = useState(false);
  const [demoActionMessage, setDemoActionMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadTelemetry = useCallback((signal?: AbortSignal) => {
    setIsLoading(true);

    Promise.all([
      getHealth({ signal }),
      getLatestReading({ signal }),
      getReadingHistory(120, { signal }),
      getRuns({ signal }),
      getAlerts(50, { signal }),
      getReviewQueue({ signal }),
      getDemoScenarios({ signal }),
      getCameraStatus({ signal }),
    ])
      .then(
        ([
          healthResult,
          latestResult,
          historyResult,
          runsResult,
          alertsResult,
          queueResult,
          scenariosResult,
          cameraResult,
        ]) => {
        setHealth(healthResult);
        setLatestReading(latestResult.reading);
        setCurrentRun(latestResult.run ?? runsResult.runs[0] ?? null);
        setHistory(historyResult.readings);
        setRuns(runsResult.runs);
        setAlerts(alertsResult.alerts);
        setAlertSummary(alertsResult.summary);
        setReviewQueue(queueResult.items);
        setScenarios(scenariosResult.scenarios);
        setCameraStatus(cameraResult);
        setError(null);
        },
      )
      .catch((loadError: Error) => {
        if (loadError.name !== "AbortError") {
          setError(loadError.message);
        }
      })
      .finally(() => {
        if (!signal?.aborted) {
          setIsLoading(false);
        }
      });
  }, []);

  useEffect(() => {
    const controller = new AbortController();

    loadTelemetry(controller.signal);

    return () => {
      controller.abort();
    };
  }, [loadTelemetry]);

  const highSeverityCount = useMemo(
    () => alerts.filter((alert) => alert.severity === "high").length,
    [alerts],
  );
  const latestAlerts = useMemo(() => alerts.slice(0, 8), [alerts]);
  const latestFault = latestReading?.fault_mode ?? null;
  const isOnline = health?.status === "ok" && !error;

  const handleReview = useCallback(
    (alertId: number, reviewStatus: ReviewStatus, assignedTo = "") => {
      setReviewingAlertId(alertId);
      updateAlertReview(
        alertId,
        reviewStatus,
        `Marked ${formatLabel(reviewStatus)} in dashboard.`,
        assignedTo,
      )
        .then(() => loadTelemetry())
        .catch((reviewError: Error) => setError(reviewError.message))
        .finally(() => setReviewingAlertId(null));
    },
    [loadTelemetry],
  );

  const refreshReport = useCallback((runId: number) => {
    getRunReport(runId)
      .then((runReport) => {
        setReport(runReport);
        setError(null);
      })
      .catch((reportError: Error) => setError(reportError.message));
  }, []);

  useEffect(() => {
    if (currentRun) {
      refreshReport(currentRun.id);
    }
  }, [currentRun, refreshReport]);

  const runDemoAction = useCallback(
    (action: "reset" | "seed", scenario: string) => {
      setIsDemoActionRunning(true);
      setDemoActionMessage(null);
      const request = action === "reset" ? resetDemoData(scenario) : seedDemoData(scenario);

      request
        .then((result) => {
          setDemoActionMessage(
            `${action === "reset" ? "Reset" : "Seeded"} ${result.readings_created} readings and ${result.alerts_created} alerts for ${result.run.name}.`,
          );
          loadTelemetry();
        })
        .catch((demoError: Error) => setError(demoError.message))
        .finally(() => setIsDemoActionRunning(false));
    },
    [loadTelemetry],
  );

  const exportRunReport = useCallback(() => {
    if (!currentRun) {
      setError("No current run is available to export.");
      return;
    }

    getRunReport(currentRun.id)
      .then((runReport) => {
        setReport(runReport);
        const blob = new Blob([JSON.stringify(runReport, null, 2)], {
          type: "application/json",
        });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `rigsight-run-${currentRun.id}-report.json`;
        link.click();
        URL.revokeObjectURL(url);
      })
      .catch((reportError: Error) => setError(reportError.message));
  }, [currentRun]);

  const exportRunReportHtml = useCallback(() => {
    if (!currentRun) {
      setError("No current run is available to export.");
      return;
    }
    window.open(getRunReportHtmlUrl(currentRun.id), "_blank", "noopener,noreferrer");
  }, [currentRun]);

  return {
    alertSummary,
    alerts,
    cameraStatus,
    currentRun,
    demoActionMessage,
    error,
    exportRunReport,
    exportRunReportHtml,
    handleReview,
    health,
    highSeverityCount,
    history,
    isLoading,
    isOnline,
    isDemoActionRunning,
    latestAlerts,
    latestFault,
    latestReading,
    loadTelemetry,
    report,
    resetDemo: (scenario: string) => runDemoAction("reset", scenario),
    reviewQueue,
    reviewingAlertId,
    runs,
    scenarios,
    seedDemo: (scenario: string) => runDemoAction("seed", scenario),
  };
}
