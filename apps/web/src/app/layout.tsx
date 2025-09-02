import './globals.css';
import Link from 'next/link';
import type { ReactNode } from 'react';

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav className="bg-gray-100 p-4 flex space-x-4">
          <Link href="/upload" className="text-blue-600 hover:underline">
            Home
          </Link>
          <Link href="/analyses" className="text-blue-600 hover:underline">
            Analyses
          </Link>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  );
}

