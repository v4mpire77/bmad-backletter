import { render, screen } from '@testing-library/react';
import VerdictChips from '@/components/VerdictChips';

describe('VerdictChips', () => {
  it('renders pass verdict correctly', () => {
    render(<VerdictChips verdict="pass" />);
    const chipElement = screen.getByText('pass');
    expect(chipElement).toBeInTheDocument();
    expect(chipElement).toHaveClass('bg-green-100');
  });

  it('renders weak verdict correctly', () => {
    render(<VerdictChips verdict="weak" />);
    const chipElement = screen.getByText('weak');
    expect(chipElement).toBeInTheDocument();
    expect(chipElement).toHaveClass('bg-yellow-100');
  });

  it('renders missing verdict correctly', () => {
    render(<VerdictChips verdict="missing" />);
    const chipElement = screen.getByText('missing');
    expect(chipElement).toBeInTheDocument();
    expect(chipElement).toHaveClass('bg-red-100');
  });

  it('renders needs_review verdict correctly', () => {
    render(<VerdictChips verdict="needs_review" />);
    const chipElement = screen.getByText('needs review');
    expect(chipElement).toBeInTheDocument();
    expect(chipElement).toHaveClass('bg-blue-100');
  });

  it('has correct ARIA label', () => {
    render(<VerdictChips verdict="pass" />);
    const chipElement = screen.getByText('pass');
    expect(chipElement).toHaveAttribute('aria-label', 'Pass');
  });
});