import micromatch from 'micromatch';

// Simple helper to check if any of the given paths match provided glob patterns.
export function matchPaths(paths = [], patterns = []) {
  return micromatch.some(paths, patterns);
}
