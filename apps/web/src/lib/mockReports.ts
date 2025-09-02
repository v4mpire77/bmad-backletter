export interface ReportMeta {
  id: number;
  createdAt: string;
}

export const mockReports: ReportMeta[] = [];

export function addReport() {
  mockReports.push({
    id: mockReports.length + 1,
    createdAt: new Date().toISOString(),
  });
}

export function getReports() {
  return mockReports;
}
