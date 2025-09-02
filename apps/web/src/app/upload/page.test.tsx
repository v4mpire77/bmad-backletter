import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';
import UploadPage from './page';

const pushMock = vi.fn();
const originalFetch = global.fetch;

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: pushMock }),
}));

afterEach(() => {
  pushMock.mockReset();
  global.fetch = originalFetch;
  vi.restoreAllMocks();
});

describe('UploadPage', () => {
  it('uploads a valid file and navigates', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ job_id: 'j1', analysis_id: 'a1', status: 'queued' }),
    });
    global.fetch = fetchMock as any;

    const { container, getByText } = render(<UploadPage />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const file = new File(['data'], 'test.pdf', { type: 'application/pdf' });

    await waitFor(() => {
      fireEvent.change(input, { target: { files: [file] } });
    });

    await waitFor(() => expect(pushMock).toHaveBeenCalledWith('/analyses/a1'));
    expect(getByText(/queued/i)).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledWith(
      '/v1/docs/upload',
      expect.objectContaining({ method: 'POST' })
    );
  });

  it('shows error for unsupported file type', () => {
    const fetchMock = vi.fn();
    global.fetch = fetchMock as any;
    const { container, getByRole } = render(<UploadPage />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const file = new File(['data'], 'test.txt', { type: 'text/plain' });

    fireEvent.change(input, { target: { files: [file] } });

    expect(getByRole('alert')).toHaveTextContent(/only pdf or docx files are allowed/i);
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('shows error for files over 10MB', () => {
    const fetchMock = vi.fn();
    global.fetch = fetchMock as any;
    const { container, getByRole } = render(<UploadPage />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const bigData = new Uint8Array(11 * 1024 * 1024);
    const file = new File([bigData], 'big.pdf', { type: 'application/pdf' });

    fireEvent.change(input, { target: { files: [file] } });

    expect(getByRole('alert')).toHaveTextContent(/file must be 10mb or less/i);
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('displays server error message', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      json: async () => ({ detail: 'Nope' }),
    });
    global.fetch = fetchMock as any;

    const { container, getByRole } = render(<UploadPage />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const file = new File(['data'], 'bad.pdf', { type: 'application/pdf' });

    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() =>
      expect(getByRole('alert')).toHaveTextContent(/nope/i)
    );
  });

  it('retries upload after network failure', async () => {
    const first = vi.fn().mockRejectedValue(new Error('network'));
    const second = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ job_id: 'j2', analysis_id: 'a2', status: 'queued' }),
    });
    const fetchMock = vi.fn()
      .mockImplementationOnce(first)
      .mockImplementationOnce(second);
    global.fetch = fetchMock as any;

    const { container, getByRole, getByText } = render(<UploadPage />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const file = new File(['data'], 'test.pdf', { type: 'application/pdf' });

    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => expect(getByRole('alert')).toBeInTheDocument());
    fireEvent.click(getByText(/retry/i));

    await waitFor(() => expect(pushMock).toHaveBeenCalledWith('/analyses/a2'));
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });
});
