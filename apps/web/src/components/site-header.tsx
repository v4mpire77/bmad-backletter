'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const tabs = [
  { href: '/upload', label: 'Upload' },
  { href: '/analyses', label: 'Analyses' },
];

export default function SiteHeader() {
  const pathname = usePathname();
  return (
    <header className="sticky top-0 z-50 border-b bg-background/80 backdrop-blur">
      <nav className="mx-auto flex max-w-6xl items-center gap-6 px-4 py-3">
        <Link href="/upload" className="font-semibold">Blackletter</Link>
        <div className="flex gap-4">
          {tabs.map(t => (
            <Link
              key={t.href}
              href={t.href}
              className={`text-sm ${pathname?.startsWith(t.href) ? 'font-semibold underline' : 'text-muted-foreground'}`}
            >
              {t.label}
            </Link>
          ))}
        </div>
      </nav>
    </header>
  );
}
