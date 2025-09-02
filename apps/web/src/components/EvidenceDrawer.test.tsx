import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import EvidenceDrawer from './EvidenceDrawer';
import { vi } from 'vitest';

describe('EvidenceDrawer', () => {
  it('closes on Escape key', () => {
    const onClose = vi.fn();
    render(
      <EvidenceDrawer isOpen onClose={onClose}>
        <p>content</p>
      </EvidenceDrawer>
    );
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(onClose).toHaveBeenCalled();
  });
});
