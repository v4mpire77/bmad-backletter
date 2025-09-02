import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import ExportDialog from './ExportDialog';
import { vi } from 'vitest';

describe('ExportDialog', () => {
  it('calls onConfirm when confirmed', () => {
    const onClose = vi.fn();
    const onConfirm = vi.fn();
    const { getByText } = render(
      <ExportDialog isOpen onClose={onClose} onConfirm={onConfirm} />
    );
    fireEvent.click(getByText('Confirm'));
    expect(onConfirm).toHaveBeenCalled();
  });

  it('closes on Escape key', () => {
    const onClose = vi.fn();
    const onConfirm = vi.fn();
    render(<ExportDialog isOpen onClose={onClose} onConfirm={onConfirm} />);
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(onClose).toHaveBeenCalled();
  });
});
