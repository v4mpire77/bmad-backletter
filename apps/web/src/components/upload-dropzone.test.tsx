import React from "react";
import { render, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { vi } from "vitest";
import { UploadDropzone } from "./upload-dropzone";

describe("UploadDropzone", () => {
  it("calls onUpload for valid file", async () => {
    const onUpload = vi.fn().mockResolvedValue(undefined);
    const { container } = render(<UploadDropzone onUpload={onUpload} />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const file = new File(["data"], "test.pdf", { type: "application/pdf" });

    await waitFor(() => {
      fireEvent.change(input, { target: { files: [file] } });
    });

    await waitFor(() => expect(onUpload).toHaveBeenCalledWith(file));
  });

  it("shows error for unsupported file type", () => {
    const onUpload = vi.fn();
    const { container, getByRole } = render(<UploadDropzone onUpload={onUpload} />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const file = new File(["data"], "test.txt", { type: "text/plain" });

    fireEvent.change(input, { target: { files: [file] } });

    expect(getByRole("alert")).toHaveTextContent(/only pdf or docx files are allowed/i);
    expect(onUpload).not.toHaveBeenCalled();
  });

  it("shows error for files over 10MB", () => {
    const onUpload = vi.fn();
    const { container, getByRole } = render(<UploadDropzone onUpload={onUpload} />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const bigData = new Uint8Array(11 * 1024 * 1024);
    const file = new File([bigData], "big.pdf", { type: "application/pdf" });

    fireEvent.change(input, { target: { files: [file] } });

    expect(getByRole("alert")).toHaveTextContent(/file must be 10mb or less/i);
    expect(onUpload).not.toHaveBeenCalled();
  });

  it("handles drag and drop", async () => {
    const onUpload = vi.fn().mockResolvedValue(undefined);
    const { getByTestId } = render(<UploadDropzone onUpload={onUpload} />);
    const dropzone = getByTestId("dropzone");
    const file = new File(["data"], "test.pdf", { type: "application/pdf" });

    fireEvent.dragOver(dropzone, { dataTransfer: { files: [file] } });
    fireEvent.drop(dropzone, { dataTransfer: { files: [file] } });

    await waitFor(() => expect(onUpload).toHaveBeenCalledWith(file));
  });
});
