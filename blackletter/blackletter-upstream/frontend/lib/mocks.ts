import { Finding } from '@/lib/types';

// This is a simple seeded random number generator for deterministic mocks
// Using a fixed seed for consistent results
const SEED = 12345;
let randomState = SEED;

function seededRandom() {
  randomState = (randomState * 1664525 + 1013904223) % Math.pow(2, 32);
  return randomState / Math.pow(2, 32);
}

// Generate a seeded random integer between min and max (inclusive)
function seededRandomInt(min: number, max: number): number {
  return Math.floor(seededRandom() * (max - min + 1)) + min;
}

// Generate a seeded random item from an array
function seededRandomItem<T>(array: T[]): T {
  const index = seededRandomInt(0, array.length - 1);
  return array[index];
}

// Verdict options
const verdicts = ['pass', 'weak', 'missing', 'needs_review'];

// Detector names
const detectors = [
  'Data Processing Agreement',
  'Subprocessor Clauses',
  'Data Subject Rights',
  'Data Breach Notification',
  'Data Retention Periods',
  'Third Country Transfers',
  'Security Measures',
  'Right to Erasure'
];

// Sample rationale texts
const rationales = [
  'The clause clearly defines the roles and responsibilities of each party.',
  'The language is ambiguous and could be interpreted in multiple ways.',
  'This section is missing entirely from the contract.',
  'The clause needs review to ensure compliance with GDPR requirements.',
  'The terms are standard and meet the necessary requirements.',
  'There are potential risks associated with this clause that need to be addressed.'
];

// Generate mock findings data
export const mockFindingsData: Finding[] = Array.from({ length: 8 }, (_, i) => {
  const detector = detectors[i];
  const verdict = seededRandomItem(verdicts);
  
  // Generate mock anchors for evidence highlighting
  const anchors = Array.from({ length: seededRandomInt(1, 3) }, (_, j) => ({
    text: `Anchor ${j + 1}`,
    page: seededRandomInt(1, 10),
    offset: seededRandomInt(0, 1000)
  }));

  return {
    id: `finding-${i + 1}`,
    detector,
    verdict,
    rationale: seededRandomItem(rationales),
    evidence: `This is mock evidence text for the ${detector} detector. It contains several sentences of sample text to demonstrate the evidence display. The relevant parts will be highlighted based on the anchors. This helps the user quickly identify the key information related to the finding. Additional text is included to make the evidence more realistic and substantial.`,
    anchors,
    reviewed: false
  };
});