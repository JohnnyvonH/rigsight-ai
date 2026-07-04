import { useMemo } from "react";
import {
  Brush,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceDot,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { Reading } from "../api/client";
import { formatTime } from "../utils/format";

export const chartSensors = [
  { key: "temperature_c", name: "Temperature", unit: "C", color: "#c16d22", threshold: 82 },
  { key: "vibration_mm_s", name: "Vibration", unit: "mm/s", color: "#1f5b8c", threshold: 4.2 },
  { key: "current_a", name: "Current", unit: "A", color: "#1d7e6b", threshold: 38 },
] as const;

export type ChartSensorKey = (typeof chartSensors)[number]["key"] | "all";

type ChartPoint = Reading & {
  time: string;
};

type TelemetryChartProps = {
  isLoading: boolean;
  readings: Reading[];
  selectedSensor: ChartSensorKey;
};

export function TelemetryChart({ isLoading, readings, selectedSensor }: TelemetryChartProps) {
  const chartData = useMemo<ChartPoint[]>(
    () =>
      readings.map((reading) => ({
        ...reading,
        time: formatTime(reading.timestamp),
      })),
    [readings],
  );

  if (chartData.length === 0) {
    return (
      <div className="empty-state" data-testid="telemetry-empty">
        {isLoading ? "Loading telemetry from the API." : "No telemetry readings found."}
      </div>
    );
  }

  return (
    <div className="chart-frame" data-testid="telemetry-chart">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData} margin={{ top: 20, right: 24, bottom: 8, left: 0 }}>
          <CartesianGrid stroke="#e1e7ef" vertical={false} />
          <XAxis dataKey="time" tick={{ fill: "#66758a", fontSize: 12 }} />
          <YAxis tick={{ fill: "#66758a", fontSize: 12 }} width={52} />
          <Tooltip />
          <Legend />
          {chartSensors.map((sensor) => (
            selectedSensor === "all" || selectedSensor === sensor.key ? (
              <Line
                dataKey={sensor.key}
                dot={false}
                isAnimationActive={false}
                key={sensor.key}
                name={`${sensor.name} ${sensor.unit}`}
                stroke={sensor.color}
                strokeWidth={2}
                type="monotone"
              />
            ) : null
          ))}
          {chartSensors.map((sensor) =>
            selectedSensor === sensor.key ? (
              <ReferenceLine
                ifOverflow="extendDomain"
                key={`${sensor.key}-threshold`}
                label={`${sensor.name} threshold`}
                stroke={sensor.color}
                strokeDasharray="5 5"
                y={sensor.threshold}
              />
            ) : null,
          )}
          {chartData
            .filter((reading) => reading.fault_mode)
            .map((reading) => (
              <ReferenceDot
                fill="#a34922"
                key={`${reading.id}-${reading.fault_mode}`}
                r={4}
                stroke="#ffffff"
                x={reading.time}
                y={reading.temperature_c}
              />
            ))}
          <Brush dataKey="time" height={24} stroke="#1f5b8c" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
