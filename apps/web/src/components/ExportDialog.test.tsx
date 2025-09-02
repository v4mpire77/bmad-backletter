import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import ExportDialog from './ExportDialog';

describe('ExportDialog', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('posts selected options and downloads file', async () => {
    const onClose = vi.fn();
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ url: '/report.pdf' }),
    });
    vi.stubGlobal('fetch', fetchMock);

    const clickSpy = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {});

    const { getByLabelText, getByText } = render(
      <ExportDialog isOpen onClose={onClose} analysisId="a1" />
    );

    fireEvent.click(getByLabelText('Include logo'));
    fireEvent.click(getByLabelText('Include metadata'));
    fireEvent.change(getByLabelText('Date format'), {
      target: { value: 'dd/mm/yyyy' },
    });

    fireEvent.click(getByText('Confirm'));

    await waitFor(() => expect(fetchMock).toHaveBeenCalled());

    expect(fetchMock).toHaveBeenCalledWith('/api/reports/a1', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        include_logo: false,
        include_meta: false,
        date_format: 'dd/mm/yyyy',
      }),
    });
    expect(clickSpy).toHaveBeenCalled();
    expect(onClose).toHaveBeenCalled();
  });

  it('closes on Escape key', () => {
    const onClose = vi.fn();
    render(<ExportDialog isOpen onClose={onClose} analysisId="a1" />);
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(onClose).toHaveBeenCalled();
  });
});
