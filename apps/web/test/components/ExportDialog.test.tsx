import { render, screen, fireEvent } from "@testing-library/react";
import ExportDialog from "@/components/ExportDialog";

describe("ExportDialog", () => {
  test("renders dialog with aria-modal and closes on ESC", () => {
    const onClose = jest.fn();
    render(<ExportDialog open={true} onClose={onClose} />);

    const dialog = screen.getByRole("dialog", { name: /export report/i });
    expect(dialog).toBeInTheDocument();
    expect(dialog).toHaveAttribute("aria-modal", "true");

    // Close button should be focused on open
    const closeBtn = screen.getByRole("button", { name: /close export dialog/i });
    expect(closeBtn).toHaveFocus();

    // ESC to close
    fireEvent.keyDown(window, { key: "Escape" });
    expect(onClose).toHaveBeenCalled();
  });
});


