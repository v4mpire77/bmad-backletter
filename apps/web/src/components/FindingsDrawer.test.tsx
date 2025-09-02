import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import FindingsDrawer from './FindingsDrawer';
import { vi } from 'vitest';

import type { Finding } from '@shared/types';

describe('FindingsDrawer', () => {
  const finding: Finding = {
    detector_id: 'det-1',
    rule_id: 'Rule 1',
    verdict: 'pass',
    snippet: 'Some evidence',
    page: 1,
    start: 0,
    end: 0,
    rationale: '',
    reviewed: false,
  };

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

