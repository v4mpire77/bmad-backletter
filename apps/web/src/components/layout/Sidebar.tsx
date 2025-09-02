'use client';

import Link from 'next/link';

const navItems = [
  { href: '/upload', label: 'Upload' },
  { href: '/analyses', label: 'Analyses' },
];

export default function Sidebar() {
  return (
    <aside
      className="hidden w-64 shrink-0 border-r bg-background/60 p-4 md:block"
      aria-label="Sidebar"
    >
      <nav className="flex flex-col gap-2" aria-label="Sidebar Navigation">
        {navItems.map(item => (
          <Link key={item.href} href={item.href} className="text-sm text-muted-foreground hover:text-foreground">
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}

