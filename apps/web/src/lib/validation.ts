export const ACCEPTED_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  '.pdf',
  '.docx',
];

export const MAX_BYTES = 10 * 1024 * 1024; // 10MB

export function validateFile(file: File): { ok: true } | { ok: false; reason?: string } {
  const ext = file.name.toLowerCase().split('.').pop() ?? '';
  const byMime = ACCEPTED_TYPES.includes(file.type);
  const byExt = ['pdf', 'docx'].includes(ext);
  if (!byMime && !byExt) return { ok: false, reason: 'Only PDF or DOCX are accepted.' };
  if (file.size > MAX_BYTES) return { ok: false, reason: 'File exceeds 10MB limit.' };
  return { ok: true };
}
