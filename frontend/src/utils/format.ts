export function formatTime(value: string) {
  return new Date(value).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

export function formatDateTime(value: string) {
  return new Date(value).toLocaleString();
}

export function formatFault(value: string | null) {
  return value ? formatLabel(value) : "None";
}

export function formatLabel(value: string) {
  return value.replace(/_/g, " ");
}

export function formatScore(value: number | null) {
  return typeof value === "number" ? value.toFixed(3) : "--";
}

export function metricValue(value: number | undefined, suffix: string, digits = 1) {
  return typeof value === "number" ? `${value.toFixed(digits)} ${suffix}` : "--";
}
