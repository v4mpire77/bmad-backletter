import './globals.css';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';
import Main from '@/components/layout/Main';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-background text-foreground">
        <Header />
        <div className="flex">
          <Sidebar />
          <Main>{children}</Main>
        </div>
      </body>
    </html>
  );
}

