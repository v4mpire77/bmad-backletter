import type { AnalysisSummary, Finding, Verdict, VerdictCounts } from "./types";

function seededRandom(seed: number) {
  let x = Math.sin(seed) * 10000;
  return () => {
    x = Math.sin(x) * 10000;
    return x - Math.floor(x);
  };
}

function hashStringToSeed(str: string): number {
  let h = 0;
  for (let i = 0; i < str.length; i++) h = (h << 5) - h + str.charCodeAt(i);
  return Math.abs(h || 1);
}

function verdictChipCounts(rng: () => number): VerdictCounts {
  const pass_count = Math.floor(rng() * 6);
  const weak_count = Math.floor(rng() * 3);
  const missing_count = Math.floor(rng() * 2);
  const needs_review_count = Math.floor(rng() * 2);
  return { pass_count, weak_count, missing_count, needs_review_count };
}

const DETECTORS = [
  "A28_3_a_instructions",
  "A28_3_b_confidentiality",
  "A28_3_c_security",
  "A28_3_d_subprocessors",
  "A28_3_e_data_subjects",
  "A28_3_f_assistance",
  "A28_3_g_deletion_return",
  "A28_3_h_audit",
];

const VERDICT_ORDER: Verdict[] = ["pass", "weak", "missing", "needs_review"];

export function getMockAnalyses(limit = 10): AnalysisSummary[] {
  const res: AnalysisSummary[] = [];
  const rng = seededRandom(42);
  for (let i = 0; i < limit; i++) {
    const id = `mock-${i + 1}`;
    const filename = `sample_${i + 1}.pdf`;
    const created_at = new Date(Date.now() - i * 3600_000).toISOString();
    const size = Math.floor(rng() * 1024 * 150) + 50_000;
    const verdicts = verdictChipCounts(rng);
    res.push({ id, filename, created_at, size, verdicts });
  }
  return res;
}

export function getMockAnalysisSummary(id: string): AnalysisSummary {
  const rng = seededRandom(hashStringToSeed(id));
  return {
    id,
    filename: `${id}.pdf`,
    created_at: new Date().toISOString(),
    size: Math.floor(rng() * 1024 * 300) + 120_000,
    verdicts: verdictChipCounts(rng),
  };
}

export function getMockFindings(id: string): Finding[] {
  const rng = seededRandom(hashStringToSeed(id) + 7);
  return DETECTORS.map((det, idx) => {
    const v = VERDICT_ORDER[Math.floor(rng() * VERDICT_ORDER.length)];
    const start = Math.floor(rng() * 2000);
    const end = start + Math.floor(120 + rng() * 200);
    const page = 1 + Math.floor(rng() * 12);
    const snippet = buildSnippet(det, v, rng);
    return {
      detector_id: det,
      rule_id: `art28_v1.${det}`,
      verdict: v,
      snippet,
      page,
      start,
      end,
      rationale:
        v === "missing"
          ? "no explicit anchor found in evidence window"
          : v === "weak"
          ? "hedged language near anchor"
          : v === "needs_review"
          ? "token cap or ambiguous phrasing"
          : "anchor present; no red flags",
      reviewed: false,
    };
  });
}

function buildSnippet(detectorId: string, verdict: Verdict, rng: () => number): string {
  const lower = detectorId.toLowerCase();
  const hedge = ["where appropriate", "as necessary", "reasonable", "may", "endeavour to" ];
  const maybeHedge = () => (verdict === "weak" ? ` ${hedge[Math.floor(rng() * hedge.length)]}` : "");

  if (lower.includes("security")) {
    if (verdict === "missing") {
      return "The processor shall implement measures appropriate to the service. Measures should consider contemporary practices.";
    }
    return `The processor shall implement${maybeHedge()} technical and organisational measures to ensure a level of security appropriate to the risk. Measures include encryption and access controls.`;
  }
  if (lower.includes("confidentiality")) {
    if (verdict === "missing") {
      return "Personnel with access to data are trained regularly on privacy obligations.";
    }
    return `The processor imposes${maybeHedge()} confidentiality obligations on all persons authorised to process personal data. Obligations survive termination.`;
  }
  if (lower.includes("subprocessors")) {
    if (verdict === "missing") {
      return "The processor may engage third parties for certain services.";
    }
    return `The controller authorises${maybeHedge()} the use of sub-processors only with prior written authorisation. The processor shall remain fully liable for the performance of sub-processors.`;
  }
  if (lower.includes("deletion_return")) {
    if (verdict === "missing") {
      return "Upon termination the service will be discontinued and related materials archived.";
    }
    return `Upon termination of services the processor shall, at the choice of the controller, delete or return all the personal data. Deletion will be certified upon request.`;
  }
  if (lower.includes("assistance")) {
    if (verdict === "missing") {
      return "The processor cooperates with the controller.";
    }
    return `The processor shall assist the controller${maybeHedge()} in ensuring compliance with obligations pursuant to Articles 32 to 36. Assistance includes breach notifications and DPIA support.`;
  }
  if (lower.includes("audit")) {
    if (verdict === "missing") {
      return "The processor will provide information about its services.";
    }
    return `The processor shall make available to the controller all information necessary to demonstrate compliance and allow for audits, including inspections conducted by the controller or another auditor mandated by the controller.`;
  }
  if (lower.includes("instructions")) {
    if (verdict === "missing") {
      return "The processor provides services as agreed in the order form.";
    }
    return `The processor shall process personal data only on documented instructions from the controller. Instructions may be updated in writing.`;
  }
  if (lower.includes("data_subjects")) {
    if (verdict === "missing") {
      return "The processor will forward certain requests to the controller.";
    }
    return `Taking into account the nature of the processing, the processor shall assist the controller by appropriate technical and organisational measures, insofar as this is possible, for the fulfilment of the controller's obligation to respond to requests for exercising the data subject's rights.`;
  }
  return "The parties shall cooperate in good faith to ensure data protection.";
}
