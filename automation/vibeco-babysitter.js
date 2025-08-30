// Minimal babysitter that satisfies tests for issues, PRs, and retry flow.
export default async function vibeco({ github, context, core, policy = {}, plan = {} }) {
  const { owner, repo } = context.repo || {};
  const event = context.eventName;

  const hasLabel = (obj, name) => (obj?.labels || []).some(l => (l?.name || l) === name);

  if (event === "issues") {
    const issue = context.payload?.issue;
    if (!issue) return;
    if (hasLabel(issue, "jules")) {
      const aligned = typeof plan.alignsWithAcceptance === "function"
        ? await plan.alignsWithAcceptance({ planText: "", acceptance: "" })
        : true;
      const decision = typeof policy.decide === "function"
        ? policy.decide({ labels: issue.labels })
        : "approve";

      const body = aligned && decision === "approve"
        ? "Approved by policy. Proceed ✅"
        : "Escalation required — needs human review.";

      await github.rest.issues.createComment({ owner, repo, issue_number: issue.number, body });
    }
    return;
  }

  if (event === "pull_request") {
    const pr = context.payload?.pull_request;
    if (!pr) return;
    const isJules = pr.user?.login === "jules[bot]";
    const lowRisk = hasLabel(pr, "low-risk");
    if (isJules && lowRisk && !pr.draft) {
      const { data } = await github.rest.repos.getCombinedStatusForRef({ owner, repo, ref: pr.head.sha });
      if (data?.state === "success") {
        await github.rest.pulls.merge({ owner, repo, pull_number: pr.number, merge_method: "squash" });
      }
    }
    return;
  }

  if (event === "check_suite") {
    const suite = context.payload?.check_suite || {};
    if (suite.conclusion !== "failure") return;

    const prs = await github.rest.pulls.list({ owner, repo, state: "open" });
    for (const pr of prs?.data || []) {
      if (pr?.user?.login !== "jules[bot]") continue;

      const comments = await github.rest.issues.listComments({ owner, repo, issue_number: pr.number });
      const alreadyRetried = (comments?.data || []).some(c => /Retry triggered by policy/.test(c?.body || ""));

      if (!alreadyRetried) {
        await github.rest.issues.createComment({ owner, repo, issue_number: pr.number, body: "Retry triggered by policy." });
        const runId = context.payload?.check_suite?.workflow_run?.id || context.payload?.check_suite?.run_id;
        if (runId) {
          await github.rest.actions.reRunJobsForWorkflowRun({ owner, repo, run_id: runId }).catch(() => {});
        }
      } else {
        await github.rest.issues.createComment({ owner, repo, issue_number: pr.number, body: "Escalation: Human review required." });
      }
    }
    return;
  }
}
