// Returns decision: 'approve', 'comment', 'escalate', 'block', 'merge'
export function decide({ labels = [], author = "", checks = "unknown", changedPaths = [] }) {
  // TODO: implement using simple rules; tests define expected behavior
  return "comment";
}
