import { RuleSet, Rule } from "../types/gdprRules";

export function validateRuleSet(json: unknown): { ok: true; data: RuleSet } | { ok: false; errors: string[] } {
  const errors: string[] = [];
  const obj = json as Partial<RuleSet>;

  if (!obj || typeof obj !== "object") return { ok: false, errors: ["Not an object"] };
  if (!obj.version) errors.push("Missing: version");
  if (!Array.isArray(obj.jurisdiction)) errors.push("Missing/invalid: jurisdiction[]");
  if (!obj.meta?.scoring?.weights) errors.push("Missing: meta.scoring.weights");
  if (typeof obj.meta?.scoring?.pass_threshold !== "number") errors.push("Missing: meta.scoring.pass_threshold");
  if (!Array.isArray(obj.rules) || obj.rules.length === 0) errors.push("Missing: rules[]");

  if (errors.length) return { ok: false, errors };

  // per‑rule checks
  const ids = new Set<string>();
  for (const r of obj.rules as Rule[]) {
    if (!r.id) errors.push("Rule missing id");
    else if (ids.has(r.id)) errors.push(`Duplicate rule id: ${r.id}`);
    else ids.add(r.id);

    if (!r.name) errors.push(`Rule ${r.id} missing name`);
    if (!["critical","high","medium","low"].includes(r.severity)) errors.push(`Rule ${r.id} invalid severity`);
    if (!Array.isArray(r.checks) || !r.checks.length) errors.push(`Rule ${r.id} has no checks`);

    for (const c of r.checks) {
      if (!c.type) errors.push(`Rule ${r.id} check missing type`);
      if (c.type === "regex_any" || c.type === "regex_all") {
        const patterns = (c as any).patterns;
        if (!Array.isArray(patterns) || !patterns.length) errors.push(`Rule ${r.id} ${c.type} without patterns`);
        else {
          // sanity: compile regex
          for (const p of patterns) try { new RegExp(p); } catch { errors.push(`Rule ${r.id} bad regex: ${p}`); }
        }
      }
      if (c.type === "negation_regex") {
        const pat = (c as any).pattern;
        if (!pat) errors.push(`Rule ${r.id} negation_regex missing pattern`);
        else { try { new RegExp(pat); } catch { errors.push(`Rule ${r.id} bad negation_regex: ${pat}`); } }
      }
    }
  }

  return errors.length ? { ok: false, errors } : { ok: true, data: obj as RuleSet };
}

// Usage example:
// import rules from "../../rules/gdpr_rules.json";
// import { validateRuleSet } from "../lib/validateRules";
// 
// const res = validateRuleSet(rules);
// if (!res.ok) throw new Error("Rules invalid:\n" + res.errors.join("\n"));