import { describe, it, expect } from 'vitest';
import { validateFile, MAX_BYTES } from './validation';

describe('validateFile', () => {
  it('accepts pdf within size limit', () => {
    const file = new File(['data'], 'doc.pdf', { type: 'application/pdf' });
    expect(validateFile(file)).toEqual({ ok: true });
  });

  it('rejects unsupported type', () => {
    const file = new File(['data'], 'doc.txt', { type: 'text/plain' });
    expect(validateFile(file)).toEqual({ ok: false, reason: 'Only PDF or DOCX are accepted.' });
  });

  it('rejects files over limit', () => {
    const bigData = new Uint8Array(MAX_BYTES + 1);
    const file = new File([bigData], 'big.pdf', { type: 'application/pdf' });
    expect(validateFile(file)).toEqual({ ok: false, reason: 'File exceeds 10MB limit.' });
  });
});
