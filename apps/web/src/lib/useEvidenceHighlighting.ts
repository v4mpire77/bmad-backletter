import { useMemo } from 'react';
import type { Anchor } from './types';
import { highlightAnchors } from './anchors';

export function useEvidenceHighlighting(evidence: string, anchors: Anchor[]) {
  return useMemo(() => highlightAnchors(evidence, anchors), [evidence, anchors]);
}

