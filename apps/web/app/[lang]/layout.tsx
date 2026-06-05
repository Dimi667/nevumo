import LayoutShell from './LayoutShell';
import PWAUrlTracker from '@/components/PWAUrlTracker';

interface LangLayoutProps {
  children: React.ReactNode;
  params: Promise<{ lang: string }>;
}

export default async function LangLayout({ children, params }: LangLayoutProps) {
  const { lang } = await params;
  return (
    <LayoutShell lang={lang}>
      <PWAUrlTracker />
      {children}
    </LayoutShell>
  );
}
