import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Blackletter Systems | Compliance‑First AI for UK GDPR Contract Review",
  description:
    "Cut contract review time by 60% with explainable GDPR checks. Blackletter surfaces Article 28(3) clause gaps with snippet‑level evidence. Built for UK law firms (10–200 fee‑earners).",
  openGraph: {
    title: "Blackletter Systems — UK GDPR Contract Review",
    description:
      "Explainable findings with snippet, rule ID and rationale. Built for UK compliance teams.",
    type: "website",
    url: "https://bmad-backletter.onrender.com",
    images: [
      { url: "/window.svg", width: 1200, height: 630, alt: "Blackletter" },
    ],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
