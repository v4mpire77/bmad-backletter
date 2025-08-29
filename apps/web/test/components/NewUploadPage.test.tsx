
import { render, screen, fireEvent, act } from "@testing-library/react";
import NewUploadPage from "@/app/new/page";
import "@testing-library/jest-dom";

// Mock the useRouter hook
jest.mock("next/navigation", () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

describe("NewUploadPage State Machine (Mock Mode)", () => {
  beforeAll(() => {
    // Ensure mock mode is enabled for these tests
    process.env.NEXT_PUBLIC_USE_MOCKS = "1";
    jest.useFakeTimers();
  });

  afterAll(() => {
    jest.useRealTimers();
  });

  it("should initialize in the dropzone state", () => {
    render(<NewUploadPage />);
    expect(screen.getByLabelText("File upload dropzone")).toBeInTheDocument();
    expect(screen.queryByLabelText("Upload steps")).not.toBeInTheDocument();
  });

  it("should start the stepper when a file is picked", () => {
    render(<NewUploadPage />);
    const file = new File(["contract"], "contract.pdf", { type: "application/pdf" });
    const input = screen.getByLabelText("File upload dropzone").querySelector("input[type='file']");
    fireEvent.change(input!, { target: { files: [file] } });

    expect(screen.getByLabelText("Upload steps")).toBeInTheDocument();
    expect(screen.getByText("Queued")).toBeInTheDocument();
  });

  it("should advance through steps automatically", () => {
    render(<NewUploadPage />);
    const file = new File(["contract"], "contract.pdf", { type: "application/pdf" });
    const input = screen.getByLabelText("File upload dropzone").querySelector("input[type='file']");
    fireEvent.change(input!, { target: { files: [file] } });

    expect(screen.getByText("Queued")).toBeInTheDocument();

    act(() => {
      jest.advanceTimersByTime(900);
    });
    expect(screen.getByText("Extracting")).toBeInTheDocument();

    act(() => {
      jest.advanceTimersByTime(900);
    });
    expect(screen.getByText("Detecting")).toBeInTheDocument();
  });

  it("should show View Findings and Start Over when done", () => {
    render(<NewUploadPage />);
    const file = new File(["contract"], "contract.pdf", { type: "application/pdf" });
    const input = screen.getByLabelText("File upload dropzone").querySelector("input[type='file']");
    fireEvent.change(input!, { target: { files: [file] } });

    act(() => {
      // Advance through all steps
      jest.advanceTimersByTime(900 * 5);
    });

    expect(screen.getByText("Done")).toBeInTheDocument();
    expect(screen.getByText("View Findings")).toBeInTheDocument();
    expect(screen.getByText("Start over")).toBeInTheDocument();
  });

  it("should cancel the simulation when Escape key is pressed", () => {
    render(<NewUploadPage />);
    const file = new File(["contract"], "contract.pdf", { type: "application/pdf" });
    const input = screen.getByLabelText("File upload dropzone").querySelector("input[type='file']");
    fireEvent.change(input!, { target: { files: [file] } });

    act(() => {
      jest.advanceTimersByTime(900);
    });
    expect(screen.getByText("Extracting")).toBeInTheDocument();

    fireEvent.keyDown(window, { key: "Escape", code: "Escape" });

    act(() => {
      // This timer should not advance the state
      jest.advanceTimersByTime(900);
    });
    expect(screen.getByText("Extracting")).toBeInTheDocument(); // Still on the same step
    expect(screen.getByText(/Simulation canceled/)).toBeInTheDocument();
  });

  it("should reset the state when Start Over is clicked", () => {
    render(<NewUploadPage />);
    const file = new File(["contract"], "contract.pdf", { type: "application/pdf" });
    const input = screen.getByLabelText("File upload dropzone").querySelector("input[type='file']");
    fireEvent.change(input!, { target: { files: [file] } });

    act(() => {
      jest.advanceTimersByTime(900);
    });
    expect(screen.getByText("Extracting")).toBeInTheDocument();

    fireEvent.click(screen.getByText("Start over"));

    expect(screen.getByLabelText("File upload dropzone")).toBeInTheDocument();
    expect(screen.queryByLabelText("Upload steps")).not.toBeInTheDocument();
  });
});
