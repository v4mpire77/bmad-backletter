import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import AnalysisClient from "@/components/AnalysisClient";
import type { AnalysisSummary, Finding } from "@/lib/types";

jest.mock("next/navigation", () => ({
  useRouter: () => ({ push: jest.fn() }),
  usePathname: () => "/analyses/mock-1",
}));

const summary: AnalysisSummary = {
  id: "mock-1",
  filename: "mock-1.pdf",
  created_at: new Date().toISOString(),
  size: 12345,
  verdicts: { pass_count: 1, weak_count: 1, missing_count: 0, needs_review_count: 0 },
};

const findings: Finding[] = [
  {
    detector_id: "A28_3_a_instructions",
    rule_id: "art28_v1.A28_3_a_instructions",
    verdict: "pass",
    snippet: "process only on documented instructions",
    page: 1,
    start: 0,
    end: 10,
    rationale: "anchor present; no red flags",
    reviewed: false,
  },
  {
    detector_id: "A28_3_b_confidentiality",
    rule_id: "art28_v1.A28_3_b_confidentiality",
    verdict: "weak",
    snippet: "obligations may be reasonable",
    page: 1,
    start: 11,
    end: 30,
    rationale: "hedged language near anchor",
    reviewed: false,
  },
];

describe("AnalysisClient chips → table filtering", () => {
  test("clicking a chip filters findings by verdict", async () => {
    const user = userEvent.setup();
    render(<AnalysisClient summary={summary} findings={findings} />);

    // Initially both rows present
    expect(screen.getByText("A28_3_a_instructions")).toBeInTheDocument();
    expect(screen.getByText("A28_3_b_confidentiality")).toBeInTheDocument();

    const weakChip = screen.getByTestId("chip-weak");
    await user.click(weakChip);

    // Only weak remains
    expect(screen.queryByText("A28_3_a_instructions")).not.toBeInTheDocument();
    expect(screen.getByText("A28_3_b_confidentiality")).toBeInTheDocument();
  });
});


