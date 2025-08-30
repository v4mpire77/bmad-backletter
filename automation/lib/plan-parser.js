// Parse Jules' plan text and check alignment with a plain string criteria.
export function alignsWithAcceptance({ planText = "", acceptance = "" }) {
  if (!planText || !acceptance) return false;
  return String(planText).toLowerCase().includes(String(acceptance).toLowerCase());
}
