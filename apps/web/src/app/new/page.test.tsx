import React from 'react';
import { render, fireEvent, act } from '@testing-library/react';
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

it('opens file dialog when drop zone is clicked', () => {
  const { getByRole, container } = render(<UploadPage />);
  const dropzone = getByRole('button', {
    name: /drag and drop area or click to select a file/i,
  });
  const input = container.querySelector('input[type="file"]') as HTMLInputElement;
  const clickSpy = vi.spyOn(input, 'click');

  fireEvent.click(dropzone);

  expect(clickSpy).toHaveBeenCalled();
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
    onopen: ((ev: any) => void) | null = null;
    onclose: ((ev: any) => void) | null = null;
    readyState = WebSocket.OPEN;
    close = vi.fn();
    send = vi.fn();
    
    constructor(url: string) {
      MockWebSocket.instances.push(this);
      // Simulate WebSocket opening
      setTimeout(() => {
        if (this.onopen) {
          this.onopen({});
        }
      }, 0);
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

