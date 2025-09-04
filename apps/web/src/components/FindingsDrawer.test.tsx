import React from 'react';
import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axe from 'axe-core';
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

  it('has semantic structure and no a11y violations', async () => {
    render(<FindingsDrawer open onClose={() => {}} finding={finding} />);
    expect(
      screen.getByRole('heading', { level: 2, name: /Finding Details/ })
    ).toBeInTheDocument();
    const results = await axe.run(screen.getByTestId('findings-drawer'), {
      rules: { 'color-contrast': { enabled: false } },
    });
    expect(results.violations.length).toBeLessThanOrEqual(0);
  });

  it('traps focus within the drawer', async () => {
    render(<FindingsDrawer open onClose={() => {}} finding={finding} />);
    const drawer = screen.getByTestId('findings-drawer');
    const closeButton = screen.getByTestId('close-button');
    await waitFor(() => expect(drawer).toHaveFocus());
    await userEvent.tab();
    expect(closeButton).toHaveFocus();
    await userEvent.tab();
    expect(closeButton).toHaveFocus();
    await userEvent.tab({ shift: true });
    expect(closeButton).toHaveFocus();
  });
});

