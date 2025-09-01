export type Severity = "critical" | "high" | "medium" | "low";

export interface Citation {
  doc_id: string;
  page: number;
  start: number;
  end: number;
}

export interface RuleMessage {
  pass?: string;
  warn?: string;
  fail?: string;
}

export interface ScoringAdjust {
  condition: string;   // e.g., "only_vague_language"
  delta: number;       // e.g., -0.3
}

export interface BaseCheck {
  type:
    | "regex_any"
    | "regex_all"
    | "negation_regex"
    | "flag_if_only_vague"
    | "conditional_pass"
    | "policy_evaluate";
  field: "full_text"; // keep extensible if you add structured fields later
  note?: string;
}

export interface RegexAnyCheck extends BaseCheck {
  type: "regex_any";
  patterns: string[];
  min_hits?: number;
}

export interface RegexAllCheck extends BaseCheck {
  type: "regex_all";
  patterns: string[];
}

export interface NegationRegexCheck extends BaseCheck {
  type: "negation_regex";
  pattern: string;
  must_not_match: boolean; // true = fail if it matches
}

export interface FlagIfOnlyVagueCheck extends BaseCheck {
  type: "flag_if_only_vague";
  patterns: string[];
  flag: "amber" | "warn";
}

export interface ConditionalPassCheck extends BaseCheck {
  type: "conditional_pass";
  condition: string; // free‑text; your engine interprets
}

export interface PolicyEvaluateCheck extends BaseCheck {
  type: "policy_evaluate";
  criteria: Record<string, {
    bad_signals?: string[];
    good_signals?: string[];
  }>;
}

export type RuleCheck =
  | RegexAnyCheck
  | RegexAllCheck
  | NegationRegexCheck
  | FlagIfOnlyVagueCheck
  | ConditionalPassCheck
  | PolicyEvaluateCheck;

export interface Rule {
  id: string;           // e.g., "R07"
  name: string;
  article?: string;     // GDPR reference
  severity: Severity;
  description: string;
  required: boolean;
  checks: RuleCheck[];
  messages?: RuleMessage;
  scoring_adjustments?: ScoringAdjust[];
  remediation?: string;
}

export interface RuleSetMeta {
  generated_at?: string;
  purpose?: string;
  scoring?: {
    weights: Record<Severity, number>;
    pass_threshold: number; // 0..1
  };
}

export interface RuleSet {
  version: string;
  jurisdiction: string[];
  meta: RuleSetMeta;
  rules: Rule[];
  // optional: report/extraction sections if you include them
}

// Finding types for API responses
export type Verdict = "compliant" | "non_compliant" | "weak" | "insufficient_context";

export interface Finding {
  rule_id: string;
  severity: Severity;          // from the rule (may be adjusted)
  verdict: Verdict;
  risk: "low"|"medium"|"high";
  rationale: string;
  snippet: string;
  improvements: string[];
  quotes: { text: string; citation: Citation }[];
}