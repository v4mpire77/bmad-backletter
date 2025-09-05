import { describe, it, expect } from 'vitest';
import { diffLines, anchorComment, isBinaryFile, renderDiff } from './diffUtils';

describe('diff utilities', () => {
  it('maps added and removed lines correctly', () => {
    const oldText = 'a\nb\nc';
    const newText = 'a\nx\nb\nc';
    const changes = diffLines(oldText, newText);
    const mapping = Object.fromEntries(changes.filter(c => c.oldLine !== null).map(c => [c.oldLine!, c.newLine]));
    expect(mapping[1]).toBe(1);
    expect(mapping[2]).toBe(3); // line shifted due to addition
    expect(mapping[3]).toBe(4);
  });

  it('anchors comments to new line numbers after shifts', () => {
    const oldText = 'a\nb\nc';
    const newText = 'a\nx\nb\nc';
    const changes = diffLines(oldText, newText);
    const newLine = anchorComment(2, changes);
    expect(newLine).toBe(3);
  });

  it('handles binary and empty files', () => {
    expect(isBinaryFile(new Uint8Array([0, 1, 2]))).toBe(true);
    expect(isBinaryFile('')).toBe(false);
    const changes = diffLines('', '');
    expect(changes).toEqual([]);
  });

  it('toggles between side-by-side and inline views', () => {
    const inline = renderDiff('a', 'a', 'inline');
    const side = renderDiff('a', 'a', 'side-by-side');
    expect(inline.mode).toBe('inline');
    expect(side.mode).toBe('side-by-side');
  });
});
