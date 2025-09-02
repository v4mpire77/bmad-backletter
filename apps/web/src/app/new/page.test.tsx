/// <reference types="vitest" />
import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';
import UploadPage from './page';

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: vi.fn() }),
}));

const originalFetch = global.fetch;
const originalWebSocket = global.WebSocket;

afterEach(() => {
  vi.restoreAllMocks();
  global.fetch = originalFetch;
  global.WebSocket = originalWebSocket as any;
});

describe('UploadPage file input accessibility', () => {
  it('focuses input and triggers click via label', async () => {
    const user = userEvent.setup();
    const clickSpy = vi
      .spyOn(HTMLInputElement.prototype, 'click')
      .mockImplementation(() => {});

    render(<UploadPage />);
    const label = screen.getByRole('button', {
      name: /drag and drop area or click to select a file/i,
    });
    const input = screen.getByTestId('file-input');

    await user.tab();
    expect(label).toHaveFocus();
    await user.tab();
    expect(input).toHaveFocus();

    await user.click(label);
    expect(input).toHaveFocus();
    expect(clickSpy).toHaveBeenCalledTimes(0);

    label.focus();
    await user.keyboard('{Enter}');
    expect(clickSpy).toHaveBeenCalledTimes(1);

    clickSpy.mockRestore();
  });
});

it('resets to idle on escape key press during upload', async () => {
  const fetchMock = vi
    .fn()
    .mockResolvedValueOnce({ ok: true, json: async () => ({ analysis_id: '1' }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({}) });
  global.fetch = fetchMock as any;

  class MockWebSocket {
    static instances: MockWebSocket[] = [];
    onmessage: ((ev: any) => void) | null = null;
    onerror: ((ev: any) => void) | null = null;
    close = vi.fn();
    constructor(url: string) {
      MockWebSocket.instances.push(this);
    }
  }
  (global as any).WebSocket = MockWebSocket as any;

  const { getByRole, container } = render(<UploadPage />);
  const input = container.querySelector('input[type="file"]') as HTMLInputElement;
  const file = new File(['content'], 'test.txt', { type: 'text/plain' });

  await act(async () => {
    fireEvent.change(input, { target: { files: [file] } });
  });

  const progressBeforeReset = container.querySelector('.bg-blue-600');
  expect(progressBeforeReset).not.toBeNull();

  act(() => {
    fireEvent.keyDown(window, { key: 'Escape' });
  });

  const dropzoneAfterReset = getByRole('button', {
    name: /drag and drop area or click to select a file/i,
  });
  expect(dropzoneAfterReset).not.toBeNull();
  expect(container.querySelector('.bg-blue-600')).toBeNull();
});

it('updates progress based on websocket messages', async () => {
  const fetchMock = vi
    .fn()
    .mockResolvedValueOnce({ ok: true, json: async () => ({ analysis_id: 'analysis-1' }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({}) });
  global.fetch = fetchMock as any;

  class MockWebSocket {
    static instances: MockWebSocket[] = [];
    onmessage: ((ev: any) => void) | null = null;
    onerror: ((ev: any) => void) | null = null;
    close = vi.fn();
    constructor(url: string) {
      MockWebSocket.instances.push(this);
    }
  }
  (global as any).WebSocket = MockWebSocket as any;

  const { container, getByRole } = render(<UploadPage />);
  const input = container.querySelector('input[type="file"]') as HTMLInputElement;
  const file = new File(['content'], 'test.txt', { type: 'text/plain' });

  await act(async () => {
    fireEvent.change(input, { target: { files: [file] } });
  });

  const wsInstance = MockWebSocket.instances[0];

  act(() => {
    wsInstance.onmessage?.({
      data: JSON.stringify({ step: 'extracting', progress: 25 }),
    });
  });
  expect(container.querySelector('.bg-blue-600')?.getAttribute('style')).toContain('width: 25%');

  act(() => {
    wsInstance.onmessage?.({
      data: JSON.stringify({ step: 'done', progress: 100 }),
    });
  });

  expect(getByRole('button', { name: /view findings/i })).not.toBeNull();
});

