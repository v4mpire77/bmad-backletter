import { renderHook } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { useEvidenceHighlighting } from './useEvidenceHighlighting';
import * as anchors from './anchors';
import type { Anchor } from './types';

describe('useEvidenceHighlighting', () => {
  it('memoizes highlight results', () => {
    const spy = vi.spyOn(anchors, 'highlightAnchors');
    const anchorList: Anchor[] = [];
    const { rerender } = renderHook(({ text }) => useEvidenceHighlighting(text, anchorList), {
      initialProps: { text: 'hello world' },
    });
    rerender({ text: 'hello world' });
    expect(spy).toHaveBeenCalledTimes(1);
    rerender({ text: 'changed' });
    expect(spy).toHaveBeenCalledTimes(2);
  });
});

