import { describe, it, expect } from 'vitest';
import { apiUrl } from './api';

describe('apiUrl', () => {
  it('prefixes path with API base', () => {
    process.env.NEXT_PUBLIC_API_BASE = 'http://localhost:8000';
    expect(apiUrl('/v1/docs/upload')).toBe('http://localhost:8000/v1/docs/upload');
  });

  it('handles trailing slash in base', () => {
    process.env.NEXT_PUBLIC_API_BASE = 'http://localhost:8000/';
    expect(apiUrl('/v1/docs/upload')).toBe('http://localhost:8000/v1/docs/upload');
  });
});
