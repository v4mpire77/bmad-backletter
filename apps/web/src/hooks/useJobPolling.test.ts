import { renderHook, act } from '@testing-library/react';
import { vi, expect, it, afterEach } from 'vitest';
import { useJobPolling } from './useJobPolling';

const originalFetch = global.fetch;

afterEach(() => {
  global.fetch = originalFetch;
  vi.clearAllMocks();
  vi.useRealTimers();
});

it('flags stale job after thresholds and retry resets counters', async () => {
  vi.useFakeTimers();
  process.env.NEXT_PUBLIC_POLL_MAX_ATTEMPTS = '1';
  process.env.NEXT_PUBLIC_POLL_STALE_MS = '1000';
  (global.fetch as any) = vi.fn(() =>
    Promise.resolve({ ok: true, json: () => Promise.resolve({ status: 'running' }) })
  );
  const { result } = renderHook(() =>
    useJobPolling({ jobId: 'job1', onDone: vi.fn() })
  );

  await act(async () => {
    vi.advanceTimersByTime(1100);
  });

  expect(result.current.isStale).toBe(true);
  act(() => {
    result.current.retry();
  });
  expect(result.current.isStale).toBe(false);
  expect(result.current.attempts).toBe(0);
});
