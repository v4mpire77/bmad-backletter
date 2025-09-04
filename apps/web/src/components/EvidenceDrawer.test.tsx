import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import userEvent from '@testing-library/user-event';
import axe from 'axe-core';
import EvidenceDrawer from './EvidenceDrawer';
import type { Finding } from '@/lib/types';

beforeAll(() => {
  (global as any).ResizeObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
  };
});

const baseFinding: Finding = {
  id: '1',
  title: 'art28_data_categories',
  verdict: 'ok',
  evidence: 'The Processor shall process personal data...',
  rationale: 'Because <strong>evidence</strong> shows compliance.',
  anchors: [{ text: 'personal data', page: 1, offset: 24 }],
  citations: [{ page: 3, text: 'Sample citation', start: 10, end: 20 }],
};

describe('EvidenceDrawer', () => {
  it('renders with anchors', () => {
    const { container } = render(
      <EvidenceDrawer isOpen onClose={() => {}} finding={baseFinding} />
    );
    expect(container).toMatchSnapshot();
  });

  it('renders with citations', () => {
    const finding: Finding = { ...baseFinding, anchors: [], citations: baseFinding.citations };
    const { container } = render(
      <EvidenceDrawer isOpen onClose={() => {}} finding={finding} />
    );
    expect(container).toMatchSnapshot();
  });

  it('renders with empty rationale', () => {
    const finding: Finding = { ...baseFinding, rationale: undefined };
    const { container } = render(
      <EvidenceDrawer isOpen onClose={() => {}} finding={finding} />
    );
    expect(container).toMatchSnapshot();
  });

  it('renders loading state', () => {
    const { container } = render(
      <EvidenceDrawer isOpen onClose={() => {}} finding={null} />
    );
    expect(container).toMatchSnapshot();
  });

  it('has semantic headings and lists with no a11y violations', async () => {
    render(<EvidenceDrawer isOpen onClose={() => {}} finding={baseFinding} onOpenPage={() => {}} />);
    expect(
      screen.getByRole('heading', { level: 3, name: 'Evidence' })
    ).toBeInTheDocument();
    expect(screen.getByRole('list')).toBeInTheDocument();
    const results = await axe.run(document.body);
    expect(results.violations.length).toBeLessThanOrEqual(0);
  });

  it('supports keyboard navigation for citations and close button', async () => {
    render(<EvidenceDrawer isOpen onClose={() => {}} finding={baseFinding} onOpenPage={() => {}} />);
    const citation = screen.getByTestId('citation-link');
    const closeButton = screen.getByTestId('close-button');
    await userEvent.tab();
    expect(citation).toHaveFocus();
    await userEvent.tab();
    expect(closeButton).toHaveFocus();
    await userEvent.tab({ shift: true });
    expect(citation).toHaveFocus();
  });

  it('meets color contrast guidelines for highlights', async () => {
    render(<EvidenceDrawer isOpen onClose={() => {}} finding={baseFinding} onOpenPage={() => {}} />);
    const results = await axe.run(document.body, {
      runOnly: { type: 'rule', values: ['color-contrast'] },
    });
    expect(results.violations.length).toBeLessThanOrEqual(0);
  });
});

