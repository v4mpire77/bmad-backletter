import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FindingsTable from "@/components/FindingsTable";
import type { Finding } from "@/lib/types";

let findingCounter = 0;
function makeFinding(overrides: Partial<Finding> = {}): Finding {
  findingCounter++;
  return {
    finding_id: overrides.finding_id ?? `finding${findingCounter}`,
    rule_id: overrides.rule_id ?? "art28_v1.A28_3_a_instructions",
    rule_name: overrides.rule_name ?? "Instructions",
    category: overrides.category ?? "GDPR",
    severity: overrides.severity ?? "pass",
    text: overrides.text ?? "process only on documented instructions",
    start: overrides.start ?? 0,
    end: overrides.end ?? 10,
    evidence: overrides.evidence ?? "The processor shall only process personal data on documented instructions from the controller.",
    reviewed: overrides.reviewed ?? false,
  };
}

describe("FindingsTable", () => {
  test("filter by severity shows empty-state when none match", async () => {
    const user = userEvent.setup();
    const findings: Finding[] = [
      makeFinding({ severity: "pass" }),
      makeFinding({ rule_name: "Confidentiality", severity: "weak" }),
    ];

    render(<FindingsTable findings={findings} onSelect={() => {}} />);

    const select = screen.getByLabelText(/filter by severity/i) as HTMLSelectElement;
    await user.selectOptions(select, "missing");

    expect(
      screen.getByText(/No results. Try adjusting filters or search./i)
    ).toBeInTheDocument();
  });

  test("search filters by evidence/rule name", async () => {
    const user = userEvent.setup();
    const findings: Finding[] = [
      makeFinding({ rule_name: "Security", evidence: "encryption and access controls" }),
      makeFinding({ rule_name: "Subprocessors", evidence: "hedged language near anchor", severity: "weak" }),
    ];

    render(<FindingsTable findings={findings} onSelect={() => {}} />);

    const input = screen.getByLabelText(/search evidence/i);
    await user.type(input, "Subprocessors");

    // Only the subprocessors row remains
    expect(screen.getByText("Subprocessors")).toBeInTheDocument();
    expect(screen.queryByText("Security")).not.toBeInTheDocument();
  });
});

