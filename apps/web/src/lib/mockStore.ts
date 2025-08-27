export type ExportRecord = {
  id: string;
  analysis_id: string;
  filename: string;
  created_at: string; // ISO
  options: { includeLogo: boolean; includeMeta: boolean; dateFormat: string };
};

const KEY = "blackletter_mock_exports";

function readStore(): ExportRecord[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = sessionStorage.getItem(KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) return parsed as ExportRecord[];
  } catch {}
  return [];
}

function writeStore(list: ExportRecord[]) {
  if (typeof window === "undefined") return;
  try {
    sessionStorage.setItem(KEY, JSON.stringify(list));
  } catch {}
}

export function addExport(rec: ExportRecord) {
  const list = readStore();
  list.unshift(rec);
  writeStore(list.slice(0, 20)); // keep last 20
}

export function getExports(): ExportRecord[] {
  return readStore();
}

