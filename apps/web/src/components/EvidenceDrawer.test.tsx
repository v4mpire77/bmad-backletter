import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
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
});

