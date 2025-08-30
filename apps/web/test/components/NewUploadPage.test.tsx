import { render, screen, fireEvent, act, waitFor } from "@testing-library/react";
import NewUploadPage from "@/app/new/page";
import { useRouter } from "next/navigation";

// Mock the useRouter hook
jest.mock("next/navigation", () => ({
  useRouter: jest.fn(),
}));

// Mock the DemoBanner component
jest.mock("@/components/DemoBanner", () => {
  return function DummyDemoBanner() {
    return <div data-testid="demo-banner"></div>;
  };
});

describe("NewUploadPage State Machine", () => {
  beforeAll(() => {
    (useRouter as jest.Mock).mockReturnValue({
      push: jest.fn(),
    });
    // Set mock mode
    process.env.NEXT_PUBLIC_USE_MOCKS = "1";
    jest.useFakeTimers();
  });

  afterAll(() => {
    jest.useRealTimers();
  });

  test("advances through steps on a timer", () => {
    render(<NewUploadPage />);
    const file = new File(["contract"], "test.pdf", { type: "application/pdf" });

    const input = screen.getByTestId("file-input");
    act(() => {
      fireEvent.change(input, { target: { files: [file] } });
    });

    const stateMachine = screen.getByTestId("state-machine");
    expect(stateMachine).toHaveAttribute("data-state", "queued");

    act(() => {
      jest.runOnlyPendingTimers();
    });
    expect(stateMachine).toHaveAttribute("data-state", "extracting");

    act(() => {
      jest.runOnlyPendingTimers();
    });
    expect(stateMachine).toHaveAttribute("data-state", "detecting");

    act(() => {
      jest.runOnlyPendingTimers();
    });
    expect(stateMachine).toHaveAttribute("data-state", "reporting");

    act(() => {
      jest.runOnlyPendingTimers();
    });
    expect(stateMachine).toHaveAttribute("data-state", "done");
  });

  test("cancels the upload simulation", async () => {
    render(<NewUploadPage />);
    const file = new File(["contract"], "test.pdf", { type: "application/pdf" });

    const input = screen.getByTestId("file-input");
    act(() => {
      fireEvent.change(input, { target: { files: [file] } });
    });

    const stateMachine = screen.getByTestId("state-machine");
    expect(stateMachine).toHaveAttribute("data-state", "queued");

    act(() => {
      jest.runOnlyPendingTimers();
    });
    expect(stateMachine).toHaveAttribute("data-state", "extracting");

    const cancelButton = screen.getByRole("button", { name: /cancel/i });
    act(() => {
      fireEvent.click(cancelButton);
    });

    // It should not advance further
    act(() => {
      jest.runOnlyPendingTimers();
    });
    expect(stateMachine).toHaveAttribute("data-state", "extracting");
    await waitFor(() => {
      expect(screen.getByText(/Simulation canceled/)).toBeInTheDocument();
    });
  });

  test("resets the upload simulation", () => {
    render(<NewUploadPage />);
    const file = new File(["contract"], "test.pdf", { type: "application/pdf" });

    const input = screen.getByTestId("file-input");
    act(() => {
      fireEvent.change(input, { target: { files: [file] } });
    });

    expect(screen.getByText("Queued")).toBeInTheDocument();

    act(() => {
      jest.advanceTimersByTime(900);
    });
    expect(screen.getByText("Extracting")).toBeInTheDocument();

    const resetButton = screen.getByRole("button", { name: /start over/i });
    fireEvent.click(resetButton);

    // The dropzone should be visible again
    expect(screen.getByLabelText("File upload dropzone")).toBeInTheDocument();
    // The file name should be gone
    expect(screen.queryByText("test.pdf")).not.toBeInTheDocument();
  });
});
