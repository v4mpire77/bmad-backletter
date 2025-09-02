import './globals.css';
import Link from 'next/link';
import type { ReactNode } from 'react';

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <head>
        <title>My App</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body>
        <nav className="bg-gray-100 p-4 flex space-x-4">
          <Link href="/upload" className="text-blue-600 hover:underline">
            Home
          </Link>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  );
}
