import type { IngestReadingInput, IngestRunRequest } from "../api/client";

const requiredColumns = [
  "timestamp",
  "rpm",
  "torque_nm",
  "temperature_c",
  "vibration_mm_s",
  "current_a",
  "voltage_v",
  "pressure_bar",
] as const;

type CsvParseResult = {
  payload: IngestRunRequest | null;
  preview: IngestReadingInput[];
  errors: string[];
  rowCount: number;
};

function splitCsvLine(line: string): string[] {
  const cells: string[] = [];
  let cell = "";
  let inQuotes = false;

  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    const nextChar = line[index + 1];
    if (char === '"' && nextChar === '"') {
      cell += '"';
      index += 1;
    } else if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === "," && !inQuotes) {
      cells.push(cell.trim());
      cell = "";
    } else {
      cell += char;
    }
  }

  cells.push(cell.trim());
  return cells;
}

function toNumber(value: string, column: string, rowNumber: number, errors: string[]) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    errors.push(`Row ${rowNumber}: ${column} must be numeric.`);
    return 0;
  }
  return parsed;
}

export function parseTelemetryCsv(source: string): CsvParseResult {
  const lines = source
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  const errors: string[] = [];
  if (lines.length < 2) {
    return { payload: null, preview: [], errors: ["CSV must include a header and at least one row."], rowCount: 0 };
  }

  const headers = splitCsvLine(lines[0]).map((header) => header.toLowerCase());
  const missingColumns = requiredColumns.filter((column) => !headers.includes(column));
  if (missingColumns.length > 0) {
    errors.push(`Missing required columns: ${missingColumns.join(", ")}.`);
  }

  const getCell = (cells: string[], column: string) => {
    const index = headers.indexOf(column);
    return index >= 0 ? cells[index] ?? "" : "";
  };

  const readings = lines.slice(1).map((line, index) => {
    const cells = splitCsvLine(line);
    const rowNumber = index + 2;
    const timestamp = getCell(cells, "timestamp");
    if (Number.isNaN(Date.parse(timestamp))) {
      errors.push(`Row ${rowNumber}: timestamp must be parseable.`);
    }
    const faultMode = getCell(cells, "fault_mode");
    return {
      timestamp,
      phase: getCell(cells, "phase") || "Imported",
      rpm: toNumber(getCell(cells, "rpm"), "rpm", rowNumber, errors),
      torque_nm: toNumber(getCell(cells, "torque_nm"), "torque_nm", rowNumber, errors),
      temperature_c: toNumber(getCell(cells, "temperature_c"), "temperature_c", rowNumber, errors),
      vibration_mm_s: toNumber(
        getCell(cells, "vibration_mm_s"),
        "vibration_mm_s",
        rowNumber,
        errors,
      ),
      current_a: toNumber(getCell(cells, "current_a"), "current_a", rowNumber, errors),
      voltage_v: toNumber(getCell(cells, "voltage_v"), "voltage_v", rowNumber, errors),
      pressure_bar: toNumber(getCell(cells, "pressure_bar"), "pressure_bar", rowNumber, errors),
      fault_mode: faultMode || null,
    };
  });

  const firstCells = splitCsvLine(lines[1]);
  const payload =
    errors.length === 0
      ? {
          name: getCell(firstCells, "run_name") || "CSV telemetry import",
          rig_id: getCell(firstCells, "rig_id") || "pilot-rig-01",
          description: getCell(firstCells, "description") || "Imported from CSV upload.",
          readings,
        }
      : null;

  return {
    payload,
    preview: readings.slice(0, 10),
    errors,
    rowCount: readings.length,
  };
}
