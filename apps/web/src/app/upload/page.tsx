'use client';

import UploadContracts from '@/components/UploadContracts';

export default function UploadPage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="text-2xl font-semibold tracking-tight">Upload contracts</h1>
      <p className="mt-2 text-sm text-muted-foreground">
        PDF or DOCX • max 10MB each • GDPR-first processing
      </p>
      <div className="mt-6">
        <UploadContracts />
      </div>
    </main>
  );
}
