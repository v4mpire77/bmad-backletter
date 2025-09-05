import React from 'react';
import { render, screen } from '@testing-library/react';
import DiffView from './DiffView';

describe('DiffView accessibility', () => {
  it('shows icons and aria labels for insertions and deletions', () => {
    render(<DiffView oldText="a b" newText="a c" />);
    const insertion = screen.getByLabelText(/^Insertion:/);
    const deletion = screen.getByLabelText(/^Deletion:/);
    expect(insertion.querySelector('svg')).not.toBeNull();
    expect(deletion.querySelector('svg')).not.toBeNull();
  });

  it('announces diff region updates via aria-live', () => {
    render(<DiffView oldText="foo" newText="bar" />);
    const region = screen.getByRole('region', { name: /diff results/i });
    expect(region).toHaveAttribute('aria-live', 'polite');
  });
});
