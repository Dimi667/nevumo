import type { Metadata } from "next";
import localFont from "next/font/local";
import { cookies, headers } from "next/headers";

import {
  DEFAULT_LANGUAGE,
  LANGUAGE_COOKIE_NAME,
  LANGUAGE_HEADER_NAME,
  normalizeLanguage,
} from "../lib/locales";
import GoogleAnalytics from "@/components/GoogleAnalytics";
import CookieConsentBanner from "@/components/ui/CookieConsentBanner";
import { FaviconManager } from "@/components/FaviconManager";

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
    default: 'Nevumo - Local Services & Reviews',
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
  manifest: '/manifest.json',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'Nevumo',
  },
  icons: {
    apple: [
      { url: '/apple-touch-icon.png' },
      { url: '/apple-touch-icon-76x76.png', sizes: '76x76' },
      { url: '/apple-touch-icon-120x120.png', sizes: '120x120' },
      { url: '/apple-touch-icon-152x152.png', sizes: '152x152' },
      { url: '/apple-touch-icon.png', sizes: '180x180' },
    ],
    icon: [
      { url: '/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
    ],
  },
};

export function generateViewport() {
  return {
    width: 'device-width',
    initialScale: 1,
    viewportFit: 'cover',
    themeColor: '#f97316',
  };
}

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
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    region: ['EEA', 'GB'],
    wait_for_update: 500
  });
`,
          }}
        />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen bg-[#f9f9f9]`}
      >
        <FaviconManager />
        <GoogleAnalytics />
        {children}
        <CookieConsentBanner lang={lang} />
      </body>
    </html>
  );
}