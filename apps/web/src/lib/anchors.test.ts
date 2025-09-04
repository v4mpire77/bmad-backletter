import { describe, expect, it } from 'vitest';
import { highlightAnchors } from './anchors';
import type { Anchor } from './types';

const sample = 'The quick brown fox jumps over the lazy dog';

describe('highlightAnchors', () => {
  it('highlights a single anchor', () => {
    const anchors: Anchor[] = [{ text: 'quick', page: 1, offset: 4 }];
    const html = highlightAnchors(sample, anchors);
    expect(html).toContain('<mark');
    expect(html).toContain('quick');
    expect(html).toContain('style="background-color:#fef08a;color:#000"');
  });

  it('highlights multiple anchors', () => {
    const anchors: Anchor[] = [
      { text: 'quick', page: 1, offset: 4 },
      { text: 'lazy', page: 1, offset: 35 },
    ];
    const html = highlightAnchors(sample, anchors);
    expect(html.match(/<mark/g)?.length).toBe(2);
  });

  it('skips overlapping anchors', () => {
    const anchors: Anchor[] = [
      { text: 'brown fox', page: 1, offset: 10 },
      { text: 'fox jumps', page: 1, offset: 16 },
    ];
    const html = highlightAnchors(sample, anchors);
    expect(html.match(/<mark/g)?.length).toBe(1);
  });

  it('returns sanitized html when no matches', () => {
    const html = highlightAnchors(sample, []);
    expect(html).toBe(sample);
  });
});

