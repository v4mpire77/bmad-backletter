"use client";

import { landing } from "@/content/landing";

export default function LandingPage() {
  return (
    <div className="text-gray-900 dark:text-gray-100">
      <header className="border-b border-black/10 dark:border-white/10 bg-white/70 dark:bg-zinc-950/70 backdrop-blur">
        <div className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between">
          <a href="/landing" className="font-semibold tracking-wide" aria-label="Blackletter Systems home">
            Blackletter Systems
          </a>
          <nav aria-label="Primary">
            <a className="px-3 py-1 text-sm hover:underline" href="#how">How it works</a>
            <a className="px-3 py-1 text-sm hover:underline" href="#faq">FAQ</a>
          </nav>
        </div>
      </header>

      <main>
        {/* Hero */}
        <section className="mx-auto max-w-6xl px-4 py-14 text-center" aria-labelledby="hero-heading">
          <p className="inline-block rounded-full border px-3 py-1 text-xs text-sky-700 dark:text-sky-300 border-sky-300/50 mb-2">
            {landing.tagline}
          </p>
          <h1 id="hero-heading" className="text-3xl sm:text-5xl font-semibold mb-3">
            {landing.hero.h1}
          </h1>
          <p className="mx-auto max-w-3xl text-gray-600 dark:text-gray-300">
            {landing.hero.sub}
          </p>
          <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
            {landing.hero.ctas.map((c) => (
              <a
                key={c.href}
                href={c.href}
                className={
                  c.variant === "primary"
                    ? "rounded bg-black text-white px-4 py-2 text-sm focus:ring-2 focus:ring-offset-2 focus:ring-black"
                    : "rounded border px-4 py-2 text-sm"
                }
                aria-label={c.label}
              >
                {c.label}
              </a>
            ))}
          </div>
          <p className="mt-3 text-xs text-gray-500" aria-label="privacy note">
            {landing.hero.micro}
          </p>
        </section>

        {/* Value Props */}
        <section className="mx-auto max-w-6xl px-4 py-8" aria-labelledby="value-props-heading">
          <h2 id="value-props-heading" className="text-xl font-semibold mb-4">
            Why Blackletter
          </h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {landing.valueProps.map((v, i) => (
              <article key={i} className="rounded-lg border p-4 bg-white dark:bg-zinc-900 border-black/10 dark:border-white/10">
                <h3 className="font-medium mb-1">{v.title}</h3>
                <p className="text-sm text-gray-600 dark:text-gray-300">{v.body}</p>
              </article>
            ))}
          </div>
        </section>

        {/* How It Works */}
        <section id="how" className="mx-auto max-w-6xl px-4 py-8" aria-labelledby="how-heading">
          <h2 id="how-heading" className="text-xl font-semibold mb-4">
            How it works
          </h2>
          <ol className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 list-decimal list-inside">
            {landing.howItWorks.map((h, i) => (
              <li key={i} className="rounded-lg border p-4 bg-white dark:bg-zinc-900 border-black/10 dark:border-white/10">
                <h3 className="font-medium mb-1">{h.step}</h3>
                <p className="text-sm text-gray-600 dark:text-gray-300">{h.body}</p>
              </li>
            ))}
          </ol>
        </section>

        {/* Compliance Focus */}
        <section className="mx-auto max-w-6xl px-4 py-8" aria-labelledby="compliance-heading">
          <h2 id="compliance-heading" className="text-xl font-semibold mb-4">
            {landing.compliance.title}
          </h2>
          <div className="flex flex-wrap gap-2 mb-4">
            {landing.compliance.items.map((it) => (
              <span key={it} className="rounded-full border px-3 py-1 text-xs border-black/10 dark:border-white/10">
                {it}
              </span>
            ))}
          </div>
          <div className="flex flex-wrap gap-3 text-sm text-gray-700 dark:text-gray-300">
            {landing.compliance.targets.map((t) => (
              <span key={t} className="inline-flex items-center gap-2">
                <span className="inline-block h-2 w-2 rounded-full bg-emerald-500" aria-hidden /> {t}
              </span>
            ))}
          </div>
        </section>

        {/* Pilot & CTA band */}
        <section className="mx-auto max-w-6xl px-4 py-8" aria-labelledby="pilot-heading">
          <h2 id="pilot-heading" className="text-xl font-semibold mb-2">Pilot outcomes / pricing</h2>
          <p className="text-sm text-gray-600 dark:text-gray-300">{landing.pilot.pricing}</p>
          <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">{landing.pilot.outcome}</p>
          <a href={landing.pilot.cta.href} className="rounded bg-black text-white px-4 py-2 text-sm" aria-label={landing.pilot.cta.label}>
            {landing.pilot.cta.label}
          </a>
        </section>

        {/* FAQ */}
        <section id="faq" className="mx-auto max-w-6xl px-4 py-8" aria-labelledby="faq-heading">
          <h2 id="faq-heading" className="text-xl font-semibold mb-4">FAQ</h2>
          <div className="space-y-3">
            {landing.faq.map((f, i) => (
              <details key={i} className="rounded-lg border p-4 bg-white dark:bg-zinc-900 border-black/10 dark:border-white/10">
                <summary className="cursor-pointer font-medium">{f.q}</summary>
                <p className="mt-2 text-sm text-gray-600 dark:text-gray-300">{f.a}</p>
              </details>
            ))}
          </div>
        </section>
      </main>

      <footer className="mt-8 border-t border-black/10 dark:border-white/10">
        <div className="mx-auto max-w-6xl px-4 py-6 text-xs text-gray-500">
          {landing.footerNote}
        </div>
      </footer>
    </div>
  );
}

