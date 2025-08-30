export function splitIntoWaves(rows = [], waves = 5) {
  if (!Array.isArray(rows) || rows.length === 0 || waves <= 0) {
    return [];
  }

  const total = rows.length;
  const baseSize = Math.floor(total / waves);
  const remainder = total % waves;

  const result = [];
  let cursor = 0;
  for (let i = 0; i < waves; i++) {
    const sizeForWave = baseSize + (i < remainder ? 1 : 0);
    const nextCursor = cursor + sizeForWave;
    const chunk = rows.slice(cursor, nextCursor);
    if (chunk.length > 0) {
      result.push(chunk);
    }
    cursor = nextCursor;
  }

  return result;
}
