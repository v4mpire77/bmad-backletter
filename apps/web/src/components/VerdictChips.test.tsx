import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import VerdictChips from './VerdictChips';

describe('VerdictChips', () => {
  it('adds an aria-label for accessibility', () => {
    const { getByText } = render(<VerdictChips verdict="pass" />);
    const chip = getByText(/pass/i);
    expect(chip).toHaveAttribute('aria-label', 'Pass');
  });
});
