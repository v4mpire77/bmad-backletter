import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FindingsTable from "@/components/FindingsTable";
import type { Finding } from "@/lib/types";

function makeFinding(overrides: Partial<Finding> = {}): Finding {
  return {
    detector_id: overrides.detector_id ?? "A28_3_a_instructions",
    rule_id: overrides.rule_id ?? "art28_v1.A28_3_a_instructions",
    verdict: overrides.verdict ?? "pass",
    snippet: overrides.snippet ?? "process only on documented instructions",
    page: overrides.page ?? 1,
    start: overrides.start ?? 0,
    end: overrides.end ?? 10,
    rationale: overrides.rationale ?? "anchor present; no red flags",
    reviewed: overrides.reviewed ?? false,
  };
}

describe("FindingsTable", () => {
  test("filter by verdict shows empty-state when none match", async () => {
    const user = userEvent.setup();
    const findings: Finding[] = [
      makeFinding({ verdict: "pass" }),
      makeFinding({ detector_id: "A28_3_b_confidentiality", verdict: "weak" }),
    ];

    render(<FindingsTable findings={findings} onSelect={() => {}} />);

    const select = screen.getByLabelText(/filter by verdict/i) as HTMLSelectElement;
    await user.selectOptions(select, "missing");

    expect(
      screen.getByText(/No results. Try adjusting filters or search./i)
    ).toBeInTheDocument();
  });

  test("search filters by snippet/rationale/detector", async () => {
    const user = userEvent.setup();
    const findings: Finding[] = [
      makeFinding({ detector_id: "A28_3_c_security", snippet: "encryption and access controls" }),
      makeFinding({ detector_id: "A28_3_d_subprocessors", rationale: "hedged language near anchor", verdict: "weak" }),
    ];

    render(<FindingsTable findings={findings} onSelect={() => {}} />);

    const input = screen.getByLabelText(/search snippets/i);
    await user.type(input, "subprocessors");

    // Only the subprocessors row remains
    expect(screen.getByText("A28_3_d_subprocessors")).toBeInTheDocument();
    expect(screen.queryByText("A28_3_c_security")).not.toBeInTheDocument();
  });
});

