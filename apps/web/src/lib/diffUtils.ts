export type LineChange = {
  oldLine: number | null;
  newLine: number | null;
  type: 'context' | 'add' | 'remove';
};

// Very small diff implementation used for tests
export function diffLines(oldText: string, newText: string): LineChange[] {
  const oldLines = oldText === '' ? [] : oldText.split('\n');
  const newLines = newText === '' ? [] : newText.split('\n');
  const result: LineChange[] = [];
  let i = 0;
  let j = 0;
  while (i < oldLines.length || j < newLines.length) {
    const oldLine = oldLines[i];
    const newLine = newLines[j];
    if (oldLine === newLine) {
      result.push({ oldLine: i + 1, newLine: j + 1, type: 'context' });
      i++; j++;
      continue;
    }
    if (newLine !== undefined && oldLines[i] === newLines[j + 1]) {
      // line added in new
      result.push({ oldLine: null, newLine: j + 1, type: 'add' });
      j++;
      continue;
    }
    if (oldLine !== undefined && oldLines[i + 1] === newLine) {
      // line removed from old
      result.push({ oldLine: i + 1, newLine: null, type: 'remove' });
      i++;
      continue;
    }
    // fallback: treat as removal then addition
    if (oldLine !== undefined) {
      result.push({ oldLine: i + 1, newLine: null, type: 'remove' });
      i++;
    }
    if (newLine !== undefined) {
      result.push({ oldLine: null, newLine: j + 1, type: 'add' });
      j++;
    }
  }
  return result;
}

export function mapOldToNew(changes: LineChange[]): Record<number, number | null> {
  const map: Record<number, number | null> = {};
  for (const change of changes) {
    if (change.oldLine !== null) {
      map[change.oldLine] = change.newLine ?? null;
    }
  }
  return map;
}

export function anchorComment(oldLine: number, changes: LineChange[]): number | null {
  const map = mapOldToNew(changes);
  return map[oldLine] ?? null;
}

export function isBinaryFile(content: Uint8Array | string): boolean {
  if (typeof content === 'string') {
    return false;
  }
  for (const byte of content) {
    if (byte === 0) return true;
  }
  return false;
}

export function renderDiff(oldText: string, newText: string, mode: 'inline' | 'side-by-side') {
  return { mode, changes: diffLines(oldText, newText) };
}
