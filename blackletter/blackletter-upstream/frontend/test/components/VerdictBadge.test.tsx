import { render, screen } from '@testing-library/react';
import VerdictBadge from '@/components/VerdictBadge';

describe('VerdictBadge', () => {
  it('renders pass verdict with subtle variant', () => {
    render(<VerdictBadge verdict="pass" />);
    const badge = screen.getByText('pass');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-green-100');
  });

  it('supports solid variant', () => {
    render(<VerdictBadge verdict="pass" variant="solid" />);
    const badge = screen.getByText('pass');
    expect(badge).toHaveClass('bg-green-700');
  });

  it('has correct ARIA label', () => {
    render(<VerdictBadge verdict="pass" />);
    const badge = screen.getByText('pass');
    expect(badge).toHaveAttribute('aria-label', 'Pass');
  });
});
