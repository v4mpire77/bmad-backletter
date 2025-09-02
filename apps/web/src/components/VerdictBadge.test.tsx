import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import VerdictBadge from './VerdictBadge';

describe('VerdictBadge', () => {
  it('adds an aria-label for accessibility', () => {
    const { getByText } = render(<VerdictBadge verdict="pass" />);
    const badge = getByText(/pass/i);
    expect(badge).toHaveAttribute('aria-label', 'Pass');
  });
});
