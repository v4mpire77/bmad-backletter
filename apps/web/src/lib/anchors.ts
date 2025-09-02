export type HighlightOpts = { tag?: string; className?: string };

// Deterministic highlighter — wraps matched anchors in a tag
export function highlightAnchors(text: string, anchors: string[], opts: HighlightOpts = {}): string {
  if (!text) return '';
  const tag = opts.tag ?? 'mark';
  const cls = opts.className ? ` class="${opts.className}"` : '';
  const escaped = anchors.filter(Boolean).map((a) => a.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  if (!escaped.length) return text;
  const re = new RegExp(`(${escaped.join('|')})`, 'gi');
  return text.replace(re, (m) => `<${tag}${cls}>${m}</${tag}>`);
}