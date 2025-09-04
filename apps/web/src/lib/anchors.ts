import DOMPurify from 'isomorphic-dompurify';
import type { Anchor } from './types';

// Wraps anchor matches in <mark data-anchorkey="..."> and returns sanitized HTML
export function highlightAnchors(evidence: string, anchors: Anchor[]): string {
  if (!evidence) return '';
  if (!anchors || anchors.length === 0) {
    return DOMPurify.sanitize(evidence);
  }

  const sorted = [...anchors]
    .filter((a) => a.text && typeof a.offset === 'number')
    .sort((a, b) => a.offset - b.offset);

  let result = '';
  let lastIndex = 0;
  sorted.forEach((anchor, i) => {
    const start = anchor.offset;
    const end = start + anchor.text.length;
    if (start < lastIndex || start >= evidence.length) return; // skip overlaps/out of bounds
    result += evidence.slice(lastIndex, start);
    const segment = evidence.slice(start, end);
    result += `<mark data-anchorkey="a${i}" tabindex="0">${segment}</mark>`;
    lastIndex = end;
  });
  result += evidence.slice(lastIndex);

  return DOMPurify.sanitize(result, { ADD_ATTR: ['data-anchorkey', 'tabindex'] });
}

