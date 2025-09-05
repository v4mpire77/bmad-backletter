import './globals.css';
import LayoutWrapper from '@/components/layout-wrapper';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <title>Blackletter Systems – The AI legal assistant built for UK compliance</title>
        <meta
          name="description"
          content="Cut contract review time by 60% and never miss a GDPR obligation. Blackletter flags Article 28(3) clause gaps with explainable findings — snippet, rule ID, and rationale."
        />
        <meta
          property="og:title"
          content="Blackletter Systems – The AI legal assistant built for UK compliance"
        />
        <meta
          property="og:description"
          content="Cut contract review time by 60% and never miss a GDPR obligation. Blackletter flags Article 28(3) clause gaps with explainable findings — snippet, rule ID, and rationale."
        />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://blackletter.systems" />
        <meta property="og:site_name" content="Blackletter Systems" />
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body className="min-h-screen">
        <LayoutWrapper>{children}</LayoutWrapper>
      </body>
    </html>
  );
}
