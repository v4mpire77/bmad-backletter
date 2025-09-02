export function apiUrl(path: string): string {
  const base = (process.env.NEXT_PUBLIC_API_BASE || '').replace(/\/$/, '');
  return `${base}${path}`;
}
