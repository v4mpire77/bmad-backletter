'use client';

import { Shield } from 'lucide-react';

export default function GdprBadge() {
  return (
    <div className="inline-flex items-center gap-1 rounded-md border px-2 py-1 text-xs text-muted-foreground">
      <Shield className="h-3 w-3" aria-hidden="true" />
      <span>GDPR compliant · encrypted uploads</span>
    </div>
  );
}
