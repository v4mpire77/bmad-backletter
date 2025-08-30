import { describe, it, expect, vi } from "vitest";
import babysitter from "../vibeco-babysitter.js";

function mkGithub({ hasRetried = false } = {}) {
  return {
    rest: {
      pulls: {
        list: vi.fn().mockResolvedValue({
          data: [
            {
              number: 77,
              user: { login: "jules[bot]" },
              head: { sha: "deadbeef" },
              title: "Jules: fix something"
            }
          ]
        })
      },
      issues: {
        listComments: vi.fn().mockResolvedValue({
          data: hasRetried ? [{ body: "Retry triggered by policy." }] : []
        }),
        createComment: vi.fn().mockResolvedValue({})
      },
      actions: {
        reRunJobsForWorkflowRun: vi.fn().mockResolvedValue({})
      }
    }
  };
}

const mkCore = () => ({ info: vi.fn(), warning: vi.fn(), error: vi.fn() });

it("retries once on failing checks, then escalates next time", async () => {
  // First failure → retry
  let github = mkGithub({ hasRetried: false });
  let context = {
    eventName: "check_suite",
    payload: { check_suite: { conclusion: "failure", workflow_run: { id: 999 } } },
    repo: { owner: "v4mpire77", repo: "bmad-blackletter" }
  };
  await babysitter({ github, context, core: mkCore(), policy: {}, plan: {} });
  expect(github.rest.issues.createComment.mock.calls[0][0].body)
    .toMatch(/Retry triggered by policy/);

  // Second failure → escalate issue
  github = mkGithub({ hasRetried: true });
  await babysitter({ github, context, core: mkCore(), policy: {}, plan: {} });
  const comment = github.rest.issues.createComment.mock.calls.at(-1)[0].body;
  expect(comment).toMatch(/Escalation|Human review required/i);
});
