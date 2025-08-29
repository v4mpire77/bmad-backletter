import { ExportRecord } from './types';

const EXPORTS_KEY = 'mock_exports';

export function addExport(analysis_id: string, filename: string): void {
  if (typeof window === 'undefined') return;

  const newExport: ExportRecord = {
    id: `export-${Date.now()}`,
    analysis_id,
    filename,
    created_at: new Date().toISOString(),
    options: { // Add default options
      includeLogo: true,
      includeMeta: true,
      dateFormat: 'DD/MM/YYYY',
    }
  };

  const existingExports = getExports();
  const updatedExports = [...existingExports, newExport];

  sessionStorage.setItem(EXPORTS_KEY, JSON.stringify(updatedExports));
}

export function getExports(): ExportRecord[] {
  if (typeof window === 'undefined') return [];

  const storedExports = sessionStorage.getItem(EXPORTS_KEY);
  return storedExports ? JSON.parse(storedExports) : [];
}
