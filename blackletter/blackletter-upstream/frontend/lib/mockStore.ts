// A simple in-memory mock store for demo purposes
// In a real application, this would be replaced with API calls or a proper state management solution

// Define the structure of an export record
interface MockExport {
  id: string;
  fileName: string;
  exportedAt: string; // ISO string
  options: {
    includeLogo: boolean;
    includeMetadata: boolean;
    dateFormat: string;
  };
}

// In-memory array to store export records
let mockExports: MockExport[] = [];

// Get all mock exports
export function getMockExports(): MockExport[] {
  return [...mockExports]; // Return a copy to prevent direct mutation
}

// Add a new mock export
export function addMockExport(exportRecord: MockExport): void {
  mockExports.push(exportRecord);
}

// Clear all mock exports (useful for testing or reset)
export function clearMockExports(): void {
  mockExports = [];
}

// For demo purposes, we might want to pre-populate with some data
// This is optional and can be removed
export function initializeMockStore(): void {
  // Add a sample export if the store is empty
  if (mockExports.length === 0) {
    mockExports.push({
      id: 'export-1',
      fileName: 'ACME_DPA_MOCK.pdf',
      exportedAt: new Date().toISOString(),
      options: {
        includeLogo: true,
        includeMetadata: true,
        dateFormat: 'mm/dd/yyyy'
      }
    });
  }
}