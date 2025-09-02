import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import ExportDialog from './ExportDialog';
import { vi } from 'vitest';

const push = vi.fn();
vi.mock('next/navigation', () => ({
  useRouter: () => ({ push }),
}));

describe('ExportDialog', () => {
  it('navigates to reports on confirm', () => {
    const onClose = vi.fn();
    const { getByText } = render(<ExportDialog isOpen onClose={onClose} />);
    fireEvent.click(getByText('Confirm'));
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
