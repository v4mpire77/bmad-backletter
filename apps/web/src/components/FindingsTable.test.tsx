import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import FindingsTable from './FindingsTable';

describe('FindingsTable', () => {
  const findings = [
    { id: '1', rule: 'Rule A', evidence: 'Evidence 1', verdict: 'pass' },
    { id: '2', rule: 'Rule B', evidence: 'Evidence 2', verdict: 'fail' },
  ];

  it('filters by rule or verdict', async () => {
    render(<FindingsTable findings={findings} />);
    const input = screen.getByPlaceholderText(/filter/i);
    await userEvent.type(input, 'Rule B');
    expect(screen.getAllByRole('row')).toHaveLength(2);
    expect(screen.getByText('Rule B')).toBeInTheDocument();

    await userEvent.clear(input);
    await userEvent.type(input, 'pass');
    expect(screen.getAllByRole('row')).toHaveLength(2);
    expect(screen.getByText('pass')).toBeInTheDocument();
  });

  it('toggles sort order for rule column', async () => {
    render(<FindingsTable findings={findings} />);
    const ruleHeader = screen.getByRole('button', { name: /rule/i });
    // default is ascending by rule, so first row is Rule A
    let firstCell = screen.getAllByRole('row')[1].querySelectorAll('td')[0];
    expect(firstCell).toHaveTextContent('Rule A');

    await userEvent.click(ruleHeader);
    firstCell = screen.getAllByRole('row')[1].querySelectorAll('td')[0];
    expect(firstCell).toHaveTextContent('Rule B');
  });

  it('sorts by verdict when header clicked', async () => {
    render(<FindingsTable findings={findings} />);
    const verdictHeader = screen.getByRole('button', { name: /verdict/i });
    await userEvent.click(verdictHeader);
    const firstVerdict = screen.getAllByRole('row')[1].querySelectorAll('td')[1];
    expect(firstVerdict).toHaveTextContent('fail');
  });
});
