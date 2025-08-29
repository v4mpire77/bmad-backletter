// lib/api.ts
import type { OrgSettings, SettingsUpdateRequest } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${API_BASE}/api${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.message || `API error: ${res.status}`);
  }

  return res.json();
}

// Settings API
export async function getOrgSettings(): Promise<OrgSettings> {
  return apiCall<OrgSettings>("/admin/settings");
}

export async function updateOrgSettings(
  settings: SettingsUpdateRequest
): Promise<OrgSettings> {
  return apiCall<OrgSettings>("/admin/settings", {
    method: "PUT",
    body: JSON.stringify(settings),
  });
}

// Add other API functions here as needed
// For example:
// export async function uploadContract(file: File): Promise<JobStatusDto> { ... }
// export async function getJob(jobId: string): Promise<JobStatusDto> { ... }