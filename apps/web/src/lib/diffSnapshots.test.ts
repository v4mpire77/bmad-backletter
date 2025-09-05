import { describe, it, expect } from 'vitest';

function simpleDiff(oldStr: string, newStr: string, options: { ignoreWhitespace?: boolean } = {}) {
  const oldLines = oldStr.split('\n');
  const newLines = newStr.split('\n');
  const maxLen = Math.max(oldLines.length, newLines.length);
  const result: string[] = [];
  for (let i = 0; i < maxLen; i++) {
    const a = oldLines[i] ?? '';
    const b = newLines[i] ?? '';
    const aComp = options.ignoreWhitespace ? a.trim() : a;
    const bComp = options.ignoreWhitespace ? b.trim() : b;
    if (aComp === bComp) {
      result.push(`  ${b}`);
    } else {
      if (a) result.push(`- ${a}`);
      if (b) result.push(`+ ${b}`);
    }
  }
  return result.join('\n');
}

describe('diff snapshots', () => {
  it('captures small diff', () => {
    const before = 'alpha\nbeta\ngamma';
    const after = 'alpha\nbeta changed\ngamma';
    const diff = simpleDiff(before, after);
    expect(diff).toMatchSnapshot();
  });

  it('captures large diff', () => {
    const before = Array.from({ length: 20 }, (_, i) => `line ${i}`).join('\n');
    const after = Array.from({ length: 20 }, (_, i) =>
      i === 10 ? `line ${i} modified` : `line ${i}`
    ).join('\n');
    const diff = simpleDiff(before, after);
    expect(diff).toMatchSnapshot();
  });
});

describe('comment thread snapshots', () => {
  it('captures unresolved and resolved threads', () => {
    const unresolved = {
      id: 1,
      resolved: false,
      comments: ['Needs changes', 'Please update'],
    };
    const resolved = {
      ...unresolved,
      resolved: true,
      resolution: 'Fixed in latest commit',
    };
    expect({ unresolved, resolved }).toMatchSnapshot();
  });
});

describe('whitespace options', () => {
  it('captures diffs with and without whitespace ignored', () => {
    const before = 'a\nb\nc';
    const after = 'a\nb  \n c';
    const diffDefault = simpleDiff(before, after);
    const diffIgnored = simpleDiff(before, after, { ignoreWhitespace: true });
    expect({ diffDefault, diffIgnored }).toMatchSnapshot();
  });
});
