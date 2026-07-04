import { describe, expect, it } from "vitest";

import { parseTelemetryCsv } from "./csv";

describe("parseTelemetryCsv", () => {
  it("parses valid telemetry CSV into an ingestion payload", () => {
    const result = parseTelemetryCsv(`timestamp,rpm,torque_nm,temperature_c,vibration_mm_s,current_a,voltage_v,pressure_bar,phase,rig_id,run_name,description
2026-07-04T10:00:00Z,1400,80,65,1.5,28,399,3.1,Warmup,pilot-rig,Customer sample,Sanitized data
2026-07-04T10:00:20Z,1410,81,66,1.6,29,398,3.2,Warmup,pilot-rig,Customer sample,Sanitized data`);

    expect(result.errors).toEqual([]);
    expect(result.rowCount).toBe(2);
    expect(result.payload?.rig_id).toBe("pilot-rig");
    expect(result.payload?.name).toBe("Customer sample");
    expect(result.payload?.readings[0].temperature_c).toBe(65);
  });

  it("reports missing required columns and invalid numeric values", () => {
    const result = parseTelemetryCsv(`timestamp,rpm,torque_nm,temperature_c,vibration_mm_s,current_a,voltage_v
not-a-date,nope,80,65,1.5,28,399`);

    expect(result.payload).toBeNull();
    expect(result.errors.join(" ")).toContain("Missing required columns");
    expect(result.errors.join(" ")).toContain("timestamp must be parseable");
    expect(result.errors.join(" ")).toContain("rpm must be numeric");
  });
});
