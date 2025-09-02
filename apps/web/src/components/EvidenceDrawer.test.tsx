import React from 'react';
import { render, fireEvent, screen, act } from '@testing-library/react';
import EvidenceDrawer from './EvidenceDrawer';
import { vi } from 'vitest';

describe('EvidenceDrawer', () => {
  it('closes on Escape key', () => {
    const onClose = vi.fn();
    render(
      <EvidenceDrawer isOpen onClose={onClose} finding={null}>
        <p>content</p>
      </EvidenceDrawer>
    );
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(onClose).toHaveBeenCalled();
  });

  it('copies snippet text and shows toast', async () => {
    vi.useFakeTimers();
    const writeText = vi.fn();
    Object.assign(navigator, { clipboard: { writeText } });
    render(
      <EvidenceDrawer isOpen onClose={vi.fn()} finding={null}>
        <p>snippet text</p>
      </EvidenceDrawer>
    );
    await act(async () => {
      fireEvent.click(screen.getByText('Copy'));
    });
    expect(writeText).toHaveBeenCalledWith('snippet text');
    expect(screen.getByText('Copied to clipboard')).toBeTruthy();
    await act(async () => {
      vi.runAllTimers();
    });
    expect(screen.queryByText('Copied to clipboard')).toBeNull();
    vi.useRealTimers();
  });
});
