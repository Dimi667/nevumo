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
  title: "Nevumo",
  description: "Намери или предложи професионални услуги",
  viewport: 'width=device-width, initial-scale=1, maximum-scale=1',
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