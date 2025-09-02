'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
  { href: '/upload', label: 'Upload' },
  { href: '/analyses', label: 'Analyses' },
];

export default function Header() {
  const pathname = usePathname();
  return (
    <header role="banner" className="sticky top-0 z-50 border-b bg-background/80 backdrop-blur">
      <nav aria-label="Main" className="mx-auto flex max-w-6xl items-center gap-6 px-4 py-3">
        <Link href="/" className="font-semibold">
          Blackletter
        </Link>
        <div className="flex gap-4">
          {navItems.map(item => (
            <Link
              key={item.href}
              href={item.href}
              aria-current={pathname?.startsWith(item.href) ? 'page' : undefined}
              className={`text-sm ${pathname?.startsWith(item.href) ? 'font-semibold underline' : 'text-muted-foreground'}`}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </nav>
    </header>
  );
}

