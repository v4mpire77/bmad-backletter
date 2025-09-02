// Function to highlight anchor terms in evidence text
// This is a simple implementation for demo purposes

interface Anchor {
  text: string;
  page: number;
  offset: number;
}

export function highlightAnchors(evidence: string, anchors: Anchor[]): string {
  if (!anchors || anchors.length === 0) {
    return evidence;
  }

  // Sort anchors by offset in descending order to replace from the end
  // This prevents offset changes from affecting subsequent replacements
  const sortedAnchors = [...anchors].sort((a, b) => b.offset - a.offset);
  
  let highlightedEvidence = evidence;
  
  // Apply highlighting to each anchor
  sortedAnchors.forEach(anchor => {
    const { text, offset } = anchor;
    
    // Check if the anchor text exists at the specified offset
    // This is a simplification - in a real implementation, you'd want more robust matching
    if (offset + text.length <= highlightedEvidence.length) {
      const before = highlightedEvidence.substring(0, offset);
      const anchorText = highlightedEvidence.substring(offset, offset + text.length);
      const after = highlightedEvidence.substring(offset + text.length);
      
      // Only highlight if the text matches exactly
      if (anchorText === text) {
        highlightedEvidence = `${before}<mark class="bg-yellow-200">${anchorText}</mark>${after}`;
      }
    }
  });
  
  return highlightedEvidence;
}