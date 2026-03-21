import type { Metadata } from "next";
import localFont from "next/font/local";
import { cookies, headers } from "next/headers";

import {
  DEFAULT_LANGUAGE,
  LANGUAGE_COOKIE_NAME,
  LANGUAGE_HEADER_NAME,
  normalizeLanguage,
} from "../lib/locales";

// Глобалните стилове с Tailwind
import "./globals.css";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
});

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'https://nevumo.com'),
  title: {
    default: 'Nevumo',
    template: '%s | Nevumo',
  },
  description: 'Find and book local services. Compare providers, read reviews, and request quotes.',
  openGraph: {
    type: 'website',
    siteName: 'Nevumo',
    locale: 'en',
    images: [{ url: '/og-default.png', width: 1200, height: 630, alt: 'Nevumo' }],
  },
  twitter: {
    card: 'summary_large_image',
    site: '@nevumo',
  },
  robots: {
    index: true,
    follow: true,
  },
  alternates: {
    canonical: '/',
  },
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const headerStore = await headers();
  const cookieStore = await cookies();
  const lang =
    normalizeLanguage(headerStore.get(LANGUAGE_HEADER_NAME)) ??
    normalizeLanguage(cookieStore.get(LANGUAGE_COOKIE_NAME)?.value) ??
    DEFAULT_LANGUAGE;

  return (
    <html lang={lang}>
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen bg-[#f9f9f9]`}>
        {children}
      </body>
    </html>
  );
}