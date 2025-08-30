import { describe, it, expect } from "vitest";
import { splitIntoWaves } from "../lib/chunk.js";

const rows = Array.from({ length: 100 }, (_, i) => ({ title: `T${i+1}` }));

describe("CSV chunking into waves", () => {
  it("splits 100 rows into 5 roughly equal waves", () => {
    const waves = splitIntoWaves(rows, 5);
    expect(waves.length).toBe(5);
    const sizes = waves.map(w => w.length);
    // Sizes should be non-zero and within ±1 of each other
    expect(Math.min(...sizes)).toBeGreaterThan(0);
    expect(Math.max(...sizes) - Math.min(...sizes)).toBeLessThanOrEqual(1);
    expect(sizes.reduce((a,b)=>a+b,0)).toBe(100);
  });
});
