export interface ExportRecord {
  id: string;
  analysis_id: string;
  filename: string;
  created_at: string;
  options: any;
}

const exports: ExportRecord[] = [];

export function addExport(exportRecord: ExportRecord) {
  exports.push(exportRecord);
}

export function getExports(): ExportRecord[] {
  return [...exports];
}

export function getExportById(id: string): ExportRecord | undefined {
  return exports.find(exp => exp.id === id);
}
