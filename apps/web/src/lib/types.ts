export type Verdict = "pass" | "weak" | "missing" | "needs_review";

export type VerdictCounts = {
  pass_count: number;
  weak_count: number;
  missing_count: number;
  needs_review_count: number;
};

export type AnalysisSummary = {
  id: string;
  filename: string;
  created_at: string;
  size: number;
  verdicts: VerdictCounts;
};

export type Finding = {
  detector_id: string;
  rule_id: string;
  verdict: Verdict;
  snippet: string;
  page: number;
  start: number;
  end: number;
  rationale: string;
  reviewed: boolean;
};

export type JobState = "queued" | "running" | "done" | "error";

export type JobStatusDto = {
  id: string;
  status: JobState;
  analysis_id?: string;
  error_reason?: string;
  created_at?: string;
};
