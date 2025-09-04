# Evidence Drawer & Highlighting

## Types

- `Anchor`: `{ text: string; page: number; offset: number }`
- `Citation`: `{ page: number; text: string; start?: number; end?: number }`
- `Finding`: `{ id: string; title: string; verdict: 'ok'|'weak'|'missing'; evidence: string; rationale?: string; anchors: Anchor[]; citations?: Citation[] }`

`PageFinding` is a legacy table type; use `toFinding` to adapt old payloads.

## Highlight Strategy

`highlightAnchors(evidence, anchors)` wraps each anchor in `<mark data-anchorkey="a{index}" tabindex="0">`. Overlapping anchors are skipped to keep markup valid. Output is sanitized with `isomorphic-dompurify`.

The `useEvidenceHighlighting` hook memoizes highlight results to avoid unnecessary recomputation.

## Linking Pages

`EvidenceDrawer` accepts an optional `onOpenPage(page, offset)` callback. Wire this to a PDF viewer or page map to jump users to the cited location.

