import type { Metadata } from 'next';
import LayoutShell from './LayoutShell';
import { baseIcons } from '@/lib/base-metadata';

export const metadata: Metadata = {
  icons: baseIcons,
};

interface LangLayoutProps {
  children: React.ReactNode;
  params: Promise<{ lang: string }>;
}

export default async function LangLayout({ children, params }: LangLayoutProps) {
  const { lang } = await params;
  return (
    <LayoutShell lang={lang}>
      {children}
    </LayoutShell>
  );
}
