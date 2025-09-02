import React from 'react';

export default function Home() {
  return (
    <section className="space-y-6">
      <header className="space-y-2">
        <h1 className="text-3xl font-semibold">Blackletter — GDPR Contract Analyzer</h1>
        <p className="text-sm text-neutral-600">
          Upload a PDF/DOCX and get evidence-backed checks for GDPR Art. 28(3).
        </p>
      </header>

      <div className="flex gap-3">
        <a href="/upload" className="rounded-lg px-4 py-2 border bg-white hover:bg-neutral-50">
          Upload a Contract
        </a>
        {/* Placeholder: once History API exists, link it here */}
        <a href="/analyses/demo" className="rounded-lg px-4 py-2 border">
          View a Sample
        </a>
      </div>

      <section className="pt-8">
        <h2 className="text-lg font-medium mb-2">Recent Analyses</h2>
        <div className="rounded-xl border bg-white p-6 text-sm text-neutral-500">
          Coming soon — this will list recent jobs once the history endpoint lands.
        </div>
      </section>
    </section>
  );
}
