import React from "react";
import { render, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { vi } from "vitest";
import UploadPage from "./page";

const pushMock = vi.fn();
const originalFetch = global.fetch;

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: pushMock }),
}));

afterEach(() => {
  pushMock.mockReset();
  global.fetch = originalFetch;
  vi.restoreAllMocks();
});

describe("UploadPage", () => {
  it("uploads a valid file and navigates", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ analysis_id: "a1" }),
    });
    global.fetch = fetchMock as any;

    const { container, getByText } = render(<UploadPage />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const file = new File(["data"], "test.pdf", { type: "application/pdf" });

    await waitFor(() => {
      fireEvent.change(input, { target: { files: [file] } });
    });

    await waitFor(() => expect(pushMock).toHaveBeenCalledWith("/analyses/a1"));
    expect(getByText(/queued/i)).toBeInTheDocument();
  });
});
