import { render, screen, fireEvent } from "@testing-library/react";
import EvidenceDrawer from "@/components/EvidenceDrawer";
import type { Finding } from "@/lib/types";

const baseFinding: Finding = {
  finding_id: "finding1",
  rule_id: "art28_v1.A28_3_g_deletion_return",
  rule_name: "Deletion/Return",
  category: "GDPR",
  severity: "pass",
  text: "Processor shall delete or return all the personal data upon termination.",
  start: 10,
  end: 80,
  evidence: "The processor shall, at the choice of the controller, delete or return all the personal data to the controller after the end of the provision of services relating to processing, and delete existing copies unless Union or Member State law requires storage of the personal data.",
  reviewed: false,
};

describe("EvidenceDrawer", () => {
  test("renders as dialog, highlights anchors, and closes on ESC", () => {
    const onClose = jest.fn();
    render(<EvidenceDrawer finding={baseFinding} onClose={onClose} />);

    const dialog = screen.getByRole("dialog");
    expect(dialog).toBeInTheDocument();

    // Highlighted <mark> should exist for anchor terms
    const marks = dialog.querySelectorAll("mark");
    expect(marks.length).toBeGreaterThan(0);

    // Close button focus on mount
    const closeBtn = screen.getByRole("button", { name: /close/i });
    expect(closeBtn).toHaveFocus();

    // ESC closes
    fireEvent.keyDown(window, { key: "Escape" });
    expect(onClose).toHaveBeenCalled();
  });
});


