import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import FindingsDrawer from './FindingsDrawer';
import { vi } from 'vitest';

describe('FindingsDrawer', () => {
  const finding = { rule: 'Rule 1', evidence: 'Some evidence', verdict: 'pass' };

  it('renders when open', () => {
    const { getByText } = render(
      <FindingsDrawer open onClose={() => {}} finding={finding} />
    );
    expect(getByText(/Finding Details/)).toBeTruthy();
  });

  it('does not render when closed', () => {
    const { queryByText } = render(
      <FindingsDrawer open={false} onClose={() => {}} finding={finding} />
    );
    expect(queryByText(/Finding Details/)).toBeNull();
  });

  it('calls onClose on Escape key', () => {
    const onClose = vi.fn();
    render(<FindingsDrawer open onClose={onClose} finding={finding} />);
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(onClose).toHaveBeenCalled();
  });
});

