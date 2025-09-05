import { renderHook, act } from "@testing-library/react";
import { vi } from "vitest";
import useJobPolling from "./useJobPolling";

vi.mock("next/navigation", () => ({ useRouter: () => ({ push: vi.fn() }) }));

describe("useJobPolling", () => {
  afterEach(() => {
    vi.clearAllMocks();
    vi.useRealTimers();
  });

  it("backs off after three failures", async () => {
    vi.useFakeTimers();
    const fetchMock = vi.fn().mockRejectedValue(new Error("net"));
    // @ts-ignore
    global.fetch = fetchMock;
    renderHook(() => useJobPolling("job1"));
    expect(fetchMock).toHaveBeenCalledTimes(1);
    await act(async () => {
      await vi.advanceTimersByTimeAsync(2000);
    });
    expect(fetchMock).toHaveBeenCalledTimes(2);
    await act(async () => {
      await vi.advanceTimersByTimeAsync(2000);
    });
    expect(fetchMock).toHaveBeenCalledTimes(3);
    await act(async () => {
      await vi.advanceTimersByTimeAsync(2000);
    });
    expect(fetchMock).toHaveBeenCalledTimes(4);
    await act(async () => {
      await vi.advanceTimersByTimeAsync(4000);
    });
    expect(fetchMock).toHaveBeenCalledTimes(5);
  });

  it("aborts polling when abort is called", async () => {
    vi.useFakeTimers();
    const fetchMock = vi.fn(() => new Promise(() => {}));
    // @ts-ignore
    global.fetch = fetchMock;
    const { result } = renderHook(() => useJobPolling("job2"));
    expect(fetchMock).toHaveBeenCalledTimes(1);
    act(() => {
      result.current.abort();
    });
    await act(async () => {
      await vi.advanceTimersByTimeAsync(10000);
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });
});
