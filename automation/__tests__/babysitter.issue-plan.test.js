import { describe, it, expect, vi, beforeEach } from "vitest";
import babysitter from "../vibeco-babysitter.js";

const mkGithub = () => ({
  rest: {
    issues: {
      createComment: vi.fn().mockResolvedValue({}),
      listComments: vi.fn().mockResolvedValue({ data: [] })
    },
    pulls: {},
    repos: {}
  },
  paginate: vi.fn()
});

const mkCore = () => ({ info: vi.fn(), warning: vi.fn(), error: vi.fn() });

describe("Plan auto-approval on jules-labeled issues", () => {
  let github, core, context, policy, plan;

  beforeEach(() => {
    github = mkGithub();
    core = mkCore();
    context = {
      eventName: "issues",
      payload: {
        action: "labeled",
        issue: {
          number: 42,
          title: "Story 1.1 — Upload & Job Orchestration",
          labels: [{ name: "jules" }, { name: "auto" }]
        }
      },
      repo: { owner: "v4mpire77", repo: "bmad-blackletter" }
    };
    policy = {
      decide: vi.fn().mockReturnValue("approve")
    };
    plan = {
      alignsWithAcceptance: vi.fn().mockReturnValue(true)
    };
  });

  it("posts an approval comment when aligned & jules labeled", async () => {
    await babysitter({ github, context, core, policy, plan });
    expect(github.rest.issues.createComment).toHaveBeenCalledWith(
      expect.objectContaining({
        issue_number: 42,
        body: expect.stringMatching(/Approved by policy/i)
      })
    );
  });

  it("escalates (no approval) when alignment fails", async () => {
    plan.alignsWithAcceptance.mockReturnValue(false);
    policy.decide.mockReturnValue("escalate");
    await babysitter({ github, context, core, policy, plan });
    const body = github.rest.issues.createComment.mock.calls[0][0].body;
    expect(body).toMatch(/escalate|needs human/i);
  });
});
