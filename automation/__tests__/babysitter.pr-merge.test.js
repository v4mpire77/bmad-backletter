import { describe, it, expect, vi, beforeEach } from "vitest";
import babysitter from "../vibeco-babysitter.js";

const mkGithub = (state = "success") => ({
  rest: {
    repos: {
      getCombinedStatusForRef: vi.fn().mockResolvedValue({ data: { state } })
    },
    pulls: {
      merge: vi.fn().mockResolvedValue({})
    },
    issues: { createComment: vi.fn() }
  }
});

const mkCore = () => ({ info: vi.fn(), warning: vi.fn(), error: vi.fn() });

const basePR = {
  number: 101,
  title: "Jules: deps",
  user: { login: "jules[bot]" },
  labels: [{ name: "low-risk" }],
  head: { sha: "abc123" },
  draft: false
};

describe("Auto-merge rules", () => {
  it("merges low-risk PR from jules[bot] when checks are green", async () => {
    const github = mkGithub("success");
    const core = mkCore();
    const context = {
      eventName: "pull_request",
      payload: { pull_request: basePR },
      repo: { owner: "v4mpire77", repo: "bmad-blackletter" }
    };

    await babysitter({ github, context, core, policy: {}, plan: {} });
    expect(github.rest.pulls.merge).toHaveBeenCalledWith(
      expect.objectContaining({ pull_number: 101, merge_method: "squash" })
    );
  });

  it("does not merge if checks are failing", async () => {
    const github = mkGithub("failure");
    const core = mkCore();
    const context = {
      eventName: "pull_request",
      payload: { pull_request: basePR },
      repo: { owner: "v4mpire77", repo: "bmad-blackletter" }
    };

    await babysitter({ github, context, core, policy: {}, plan: {} });
    expect(github.rest.pulls.merge).not.toHaveBeenCalled();
  });
});
