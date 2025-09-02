import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import ExportDialog from './ExportDialog';
import { vi } from 'vitest';
import { mockReports } from '../lib/mockReports';

const push = vi.fn();
vi.mock('next/navigation', () => ({
  useRouter: () => ({ push }),
}));

beforeEach(() => {
  mockReports.length = 0;
});

describe('ExportDialog', () => {
  it('saves report metadata and navigates to reports on confirm', () => {
    const onClose = vi.fn();
    const { getByText } = render(<ExportDialog isOpen onClose={onClose} />);
    fireEvent.click(getByText('Confirm'));
    expect(mockReports).toHaveLength(1);
    expect(push).toHaveBeenCalledWith('/reports');
    expect(onClose).toHaveBeenCalled();
  });

  it('closes on Escape key', () => {
    const onClose = vi.fn();
    render(<ExportDialog isOpen onClose={onClose} />);
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(onClose).toHaveBeenCalled();
  });
});
