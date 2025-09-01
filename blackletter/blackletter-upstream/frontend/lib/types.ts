/**
 * Blackletter GDPR Processor - Type Definitions
 * Context Engineering Framework v2.0.0 Compliant
 * Matches backend Pydantic schemas exactly
 */

// Enum types matching backend
export type JobStatusEnum = "pending" | "processing" | "completed" | "failed" | "cancelled";
export type SeverityEnum = "High" | "Medium" | "Low";
export type IssueTypeEnum = "GDPR" | "Statute" | "Case Law";
export type IssueStatusEnum = "Open" | "In Review" | "Resolved";
export type CoverageStatusEnum = "OK" | "Partial" | "GAP";
export type CoverageStrengthEnum = "strong" | "medium" | "weak" | "absent";

// Core data types
export interface Issue {
  id: string;
  doc_id: string;
  clause_path: string;
  type: IssueTypeEnum;
  citation: string;
  severity: SeverityEnum;
  confidence: number;
  status: IssueStatusEnum;
  snippet: string;
  recommendation: string;
  created_at: string;
}

export interface Coverage {
  article: string;
  status: CoverageStatusEnum;
  confidence: number;
  present: boolean;
  strength: CoverageStrengthEnum;
}

// Job management types
export interface JobCreate {
  filename: string;
  content_type: string;
  file_size: number;
}

export interface JobStatus {
  job_id: string;
  status: JobStatusEnum;
  progress: number;
  created_at: string;
  updated_at?: string;
  message?: string;
}

export interface AnalysisResult {
  issues: Issue[];
  coverage: Coverage[];
  metadata: Record<string, any>;
}

export interface JobResult {
  job_id: string;
  status: JobStatusEnum;
  analysis?: AnalysisResult;
  error?: string;
  created_at: string;
  completed_at?: string;
  processing_time?: number;
}

// API response types
export interface JobCreateResponse {
  job_id: string;
  status: JobStatusEnum;
  message: string;
  location: string;
}

export interface ErrorResponse {
  error: string;
  status_code: number;
  path: string;
  timestamp: string;
}

export interface HealthResponse {
  status: string;
  environment: string;
  framework_compliance: number;
  timestamp: number;
}

// File upload types
export interface FileUpload {
  filename: string;
  content_type: string;
  size: number;
  checksum?: string;
}

// UI-specific types
export interface JobWithDetails extends JobStatus {
  filename?: string;
  file_size?: number;
  content_type?: string;
}

export interface DashboardStats {
  total_jobs: number;
  completed_results: number;
  status_breakdown: Record<JobStatusEnum, number>;
}

// API client configuration
export interface ApiConfig {
  baseURL: string;
  timeout: number;
  retries: number;
}

// Upload progress tracking
export interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
}

// GDPR Article 28(3) specific types
export interface GDPRArticle {
  article: string;
  name: string;
  description: string;
  required: boolean;
}

export const GDPR_ARTICLES: GDPRArticle[] = [
  {
    article: "28(3)(a)",
    name: "Processing Instructions",
    description: "Process only on documented instructions from controller",
    required: true
  },
  {
    article: "28(3)(b)",
    name: "Personnel Confidentiality",
    description: "Ensure personnel confidentiality commitments",
    required: true
  },
  {
    article: "28(3)(c)",
    name: "Security Measures",
    description: "Implement appropriate technical and organizational security measures",
    required: true
  },
  {
    article: "28(3)(d)",
    name: "Sub-processor Authorization",
    description: "Do not engage sub-processor without prior authorization",
    required: true
  },
  {
    article: "28(3)(e)",
    name: "Data Subject Rights",
    description: "Assist controller with data subject rights requests",
    required: true
  },
  {
    article: "28(3)(f)",
    name: "Breach Notification",
    description: "Notify controller of personal data breaches",
    required: true
  },
  {
    article: "28(3)(g)",
    name: "Data Deletion/Return",
    description: "Delete or return personal data at end of processing",
    required: true
  },
  {
    article: "28(3)(h)",
    name: "Audit and Inspection",
    description: "Allow audits and provide compliance information",
    required: true
  }
];

// Utility type guards
export function isJobStatus(value: any): value is JobStatus {
  return value && typeof value.job_id === 'string' && typeof value.status === 'string';
}

export function isJobResult(value: any): value is JobResult {
  return value && typeof value.job_id === 'string' && typeof value.status === 'string';
}

export function isIssue(value: any): value is Issue {
  return value && typeof value.id === 'string' && typeof value.severity === 'string';
}

export function isCoverage(value: any): value is Coverage {
  return value && typeof value.article === 'string' && typeof value.status === 'string';
}

// Color mapping utilities
export function getSeverityColor(severity: SeverityEnum): string {
  switch (severity) {
    case "High": return "text-red-700 bg-red-100 dark:text-red-400 dark:bg-red-950/20";
    case "Medium": return "text-yellow-700 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-950/20";
    case "Low": return "text-blue-700 bg-blue-100 dark:text-blue-400 dark:bg-blue-950/20";
    default: return "text-gray-700 bg-gray-100 dark:text-gray-400 dark:bg-gray-950/20";
  }
}

export function getCoverageStatusColor(status: CoverageStatusEnum): string {
  switch (status) {
    case "OK": return "text-green-700 bg-green-100 dark:text-green-400 dark:bg-green-950/20";
    case "Partial": return "text-yellow-700 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-950/20";
    case "GAP": return "text-red-700 bg-red-100 dark:text-red-400 dark:bg-red-950/20";
    default: return "text-gray-700 bg-gray-100 dark:text-gray-400 dark:bg-gray-950/20";
  }
}

export function getJobStatusColor(status: JobStatusEnum): string {
  switch (status) {
    case "completed": return "text-green-700 bg-green-100 dark:text-green-400 dark:bg-green-950/20";
    case "processing": return "text-blue-700 bg-blue-100 dark:text-blue-400 dark:bg-blue-950/20";
    case "pending": return "text-yellow-700 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-950/20";
    case "failed": return "text-red-700 bg-red-100 dark:text-red-400 dark:bg-red-950/20";
    case "cancelled": return "text-gray-700 bg-gray-100 dark:text-gray-400 dark:bg-gray-950/20";
    default: return "text-gray-700 bg-gray-100 dark:text-gray-400 dark:bg-gray-950/20";
  }
}