import { render, screen } from "@testing-library/react";
import VerdictChips from "@/components/VerdictChips";

describe("VerdictChips", () => {
  test("exposes ARIA labels for counts", () => {
    render(
      <VerdictChips
        counts={{ pass_count: 2, weak_count: 1, missing_count: 0, needs_review_count: 3 }}
      />
    );

    expect(screen.getByLabelText("Pass: 2")).toBeInTheDocument();
    expect(screen.getByLabelText("Weak: 1")).toBeInTheDocument();
    expect(screen.getByLabelText("Missing: 0")).toBeInTheDocument();
    expect(screen.getByLabelText("Needs review: 3")).toBeInTheDocument();
  });

  test("invokes onSelect and toggles active state", () => {
    const onSelect = jest.fn();
    render(
      <VerdictChips
        counts={{ pass_count: 2, weak_count: 1, missing_count: 0, needs_review_count: 3 }}
        selected="all"
        onSelect={onSelect}
      />
    );

    const weakChip = screen.getByTestId("chip-weak");
    weakChip.click();
    expect(onSelect).toHaveBeenCalledWith("weak");
  });
});

