// Returns decision: 'approve', 'comment', 'escalate', 'block', 'merge'
export function decide({ labels = [], author = "", checks = "unknown", changedPaths = [] }) {
  const labelNames = labels
    .map(l => (typeof l === "string" ? l : l?.name))
    .filter(Boolean);

  if (author === "jules[bot]" && labelNames.includes("low-risk") && checks === "success") {
    return "merge";
  }
  if (labelNames.includes("jules")) {
    return "approve";
  }
  return "comment";
}
