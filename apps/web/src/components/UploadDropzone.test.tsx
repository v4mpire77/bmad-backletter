import React from "react";
import { render, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { vi } from "vitest";
import UploadDropzone, { UploadErrorBoundary } from "./UploadDropzone";

const pushMock = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: pushMock }),
}));

afterEach(() => {
  pushMock.mockReset();
});

describe("UploadDropzone", () => {
  it("shows progress and navigates on successful upload", async () => {
    class MockXHR {
      status = 200;
      responseText = JSON.stringify({ analysis_id: "a1", status: "queued" });
      upload: any = {};
      onload: Function = () => {};
      onerror: Function = () => {};
      open() {}
      send() {
        setTimeout(() => {
          this.upload.onprogress?.({
            lengthComputable: true,
            loaded: 50,
            total: 100,
          });
          this.upload.onprogress?.({
            lengthComputable: true,
            loaded: 100,
            total: 100,
          });
          setTimeout(() => {
            this.onload();
          }, 10);
        }, 0);
      }
    }
    global.XMLHttpRequest = MockXHR as any;

    const { container, getByText } = render(
      <UploadErrorBoundary>
        <UploadDropzone />
      </UploadErrorBoundary>
    );

    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const file = new File(["data"], "test.pdf", { type: "application/pdf" });

    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => expect(getByText(/100%/)).toBeInTheDocument());
    await waitFor(() => expect(pushMock).toHaveBeenCalledWith("/analyses/a1"));
  });

  it("renders error boundary on network failure", async () => {
    class MockXHR {
      upload: any = {};
      onload: Function = () => {};
      onerror: Function = () => {};
      open() {}
      send() {
        setTimeout(() => {
          this.onerror();
        }, 0);
      }
    }
    global.XMLHttpRequest = MockXHR as any;

    const { container, getByRole } = render(
      <UploadErrorBoundary>
        <UploadDropzone />
      </UploadErrorBoundary>
    );

    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const file = new File(["data"], "test.pdf", { type: "application/pdf" });

    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() =>
      expect(getByRole("alert")).toHaveTextContent(/upload failed/i)
    );
  });

  it("shows error for unsupported file type", () => {
    const { container, getByRole } = render(
      <UploadErrorBoundary>
        <UploadDropzone />
      </UploadErrorBoundary>
    );

    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const file = new File(["data"], "test.txt", { type: "text/plain" });

    fireEvent.change(input, { target: { files: [file] } });

    expect(getByRole("alert")).toHaveTextContent(/only pdf or docx files are allowed/i);
  });

  it("shows error for files over 10MB", () => {
    const { container, getByRole } = render(
      <UploadErrorBoundary>
        <UploadDropzone />
      </UploadErrorBoundary>
    );

    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const bigData = new Uint8Array(11 * 1024 * 1024);
    const file = new File([bigData], "big.pdf", { type: "application/pdf" });

    fireEvent.change(input, { target: { files: [file] } });

    expect(getByRole("alert")).toHaveTextContent(/file must be 10mb or less/i);
  });
});
