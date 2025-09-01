import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Blackletter Systems',
  description: 'AI Contract Review System - Old rules. New game.',
}
>>>>>>> 47931f5adb3b90222b8a8032099a98d6ea0d662a

export default function RootLayout({
  children,
}: {
<<<<<<< HEAD
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <div className="min-h-screen bg-background">
          <header className="border-b">
            <div className="container mx-auto px-4 py-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <h1 className="blackletter-brand">Blackletter GDPR Processor</h1>
                  <span className="text-sm text-muted-foreground">
                    Context Engineering Framework v2.0.0
                  </span>
                </div>
                <nav className="flex items-center space-x-4">
                  <a 
                    href="/" 
                    className="text-sm font-medium text-foreground hover:text-primary transition-colors"
                  >
                    Upload
                  </a>
                  <a 
                    href="/dashboard" 
                    className="text-sm font-medium text-foreground hover:text-primary transition-colors"
                  >
                    Dashboard
                  </a>
                </nav>
              </div>
            </div>
          </header>
          <main className="container mx-auto px-4 py-8">
            {children}
          </main>
          <footer className="border-t mt-16">
            <div className="container mx-auto px-4 py-6">
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <div>
                  <p>&copy; 2024 Blackletter Systems. All rights reserved.</p>
                </div>
                <div className="flex items-center space-x-4">
                  <span>GDPR Article 28(3) Compliance</span>
                  <span>Framework Score: 80%+</span>
                </div>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
>>>>>>> 47931f5adb3b90222b8a8032099a98d6ea0d662a
/**
 * Blackletter GDPR Processor - Root Layout
 * Context Engineering Framework v2.0.0 Compliant
 */
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Blackletter GDPR Processor',
  description: 'Context Engineering Framework compliant GDPR Article 28(3) processor obligations checker',
  keywords: ['GDPR', 'Contract Analysis', 'Compliance', 'Article 28(3)', 'Processor Obligations'],
  authors: [{ name: 'Blackletter Systems' }],
  viewport: 'width=device-width, initial-scale=1',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <div className="min-h-screen bg-background">
          <header className="border-b">
            <div className="container mx-auto px-4 py-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <h1 className="blackletter-brand">Blackletter GDPR Processor</h1>
                  <span className="text-sm text-muted-foreground">
                    Context Engineering Framework v2.0.0
                  </span>
                </div>
                <nav className="flex items-center space-x-4">
                  <a 
                    href="/" 
                    className="text-sm font-medium text-foreground hover:text-primary transition-colors"
                  >
                    Upload
                  </a>
                  <a 
                    href="/dashboard" 
                    className="text-sm font-medium text-foreground hover:text-primary transition-colors"
                  >
                    Dashboard
                  </a>
                </nav>
              </div>
            </div>
          </header>
          <main className="container mx-auto px-4 py-8">
            {children}
          </main>
          <footer className="border-t mt-16">
            <div className="container mx-auto px-4 py-6">
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <div>
                  <p>&copy; 2024 Blackletter Systems. All rights reserved.</p>
                </div>
                <div className="flex items-center space-x-4">
                  <span>GDPR Article 28(3) Compliance</span>
                  <span>Framework Score: 80%+</span>
                </div>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
=======
import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Blackletter Systems',
  description: 'AI Contract Review System - Old rules. New game.',
}
>>>>>>> 47931f5adb3b90222b8a8032099a98d6ea0d662a

export default function RootLayout({
  children,
}: {
<<<<<<< HEAD
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <div className="min-h-screen bg-background">
          <header className="border-b">
            <div className="container mx-auto px-4 py-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <h1 className="blackletter-brand">Blackletter GDPR Processor</h1>
                  <span className="text-sm text-muted-foreground">
                    Context Engineering Framework v2.0.0
                  </span>
                </div>
                <nav className="flex items-center space-x-4">
                  <a 
                    href="/" 
                    className="text-sm font-medium text-foreground hover:text-primary transition-colors"
                  >
                    Upload
                  </a>
                  <a 
                    href="/dashboard" 
                    className="text-sm font-medium text-foreground hover:text-primary transition-colors"
                  >
                    Dashboard
                  </a>
                </nav>
              </div>
            </div>
          </header>
          <main className="container mx-auto px-4 py-8">
            {children}
          </main>
          <footer className="border-t mt-16">
            <div className="container mx-auto px-4 py-6">
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <div>
                  <p>&copy; 2024 Blackletter Systems. All rights reserved.</p>
                </div>
                <div className="flex items-center space-x-4">
                  <span>GDPR Article 28(3) Compliance</span>
                  <span>Framework Score: 80%+</span>
                </div>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
=======
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
>>>>>>> 47931f5adb3b90222b8a8032099a98d6ea0d662a
