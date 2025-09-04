import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';
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

  it('cycles focus through segments and actions and closes on esc', async () => {
    const finding: Finding = {
      ...baseFinding,
      anchors: [
        { text: 'The', page: 1, offset: 0 },
        { text: 'Processor', page: 1, offset: 4 },
      ],
      citations: baseFinding.citations,
    };
    const onClose = vi.fn();
    const { container } = render(
      <EvidenceDrawer
        isOpen
        onClose={onClose}
        finding={finding}
        onOpenPage={() => {}}
      />
    );
    const segments = document.querySelectorAll('[data-anchorkey]');
    expect(segments.length).toBe(2);
    await waitFor(() => expect(document.activeElement).toBe(segments[0]));

    await userEvent.tab();
    expect(document.activeElement).toBe(segments[1]);

    await userEvent.tab();
    const citationLink = screen.getByTestId('citation-link');
    expect(document.activeElement).toBe(citationLink);

    await userEvent.tab();
    const closeButton = screen.getByTestId('close-button');
    expect(document.activeElement).toBe(closeButton);

    await userEvent.tab();
    expect(document.activeElement).toBe(segments[0]);

    await userEvent.tab({ shift: true });
    expect(document.activeElement).toBe(closeButton);

    await userEvent.keyboard('{Escape}');
    expect(onClose).toHaveBeenCalled();
  });
});

