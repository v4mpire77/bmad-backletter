import React from "react";
import { render } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import UploadStatusPanel from "./UploadStatusPanel";
import { JobPollingResult } from "@/lib/useJobPolling";

describe("UploadStatusPanel", () => {
  const renderWithStatus = (status: JobPollingResult["status"], progress?: number) =>
    render(<UploadStatusPanel result={{ status, progress }} />);

  it("shows queued state", () => {
    const { getByText } = renderWithStatus("queued");
    expect(getByText(/status: queued/i)).toBeInTheDocument();
  });

  it("shows progress when processing", () => {
    const { container } = renderWithStatus("processing", 40);
    const bar = container.querySelector("div.bg-blue-500");
    expect(bar).toHaveStyle({ width: "40%" });
  });

  it("renders done without progress bar", () => {
    const { queryByRole } = renderWithStatus("done");
    expect(queryByRole("progressbar")).not.toBeInTheDocument();
  });
});
