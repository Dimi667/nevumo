import LayoutShell from './LayoutShell';
import type { Metadata } from "next";

interface LangLayoutProps {
  children: React.ReactNode;
  params: Promise<{ lang: string }>;
}

export const metadata: Metadata = {
  icons: {
    icon: '/icon.svg',
    apple: '/icons/icon-192x192.png',
  },
};

export default async function LangLayout({ children, params }: LangLayoutProps) {
  const { lang } = await params;
  return (
    <LayoutShell lang={lang}>
      {children}
    </LayoutShell>
  );
}
