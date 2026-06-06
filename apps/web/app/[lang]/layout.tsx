import LayoutShell from './LayoutShell';
import PWAUrlTracker from '@/components/PWAUrlTracker';
import AutoIntentTracker from '@/components/AutoIntentTracker';

interface LangLayoutProps {
  children: React.ReactNode;
  params: Promise<{ lang: string }>;
}

export default async function LangLayout({ children, params }: LangLayoutProps) {
  const { lang } = await params;
  return (
    <LayoutShell lang={lang}>
      <PWAUrlTracker />
      <AutoIntentTracker />
      {children}
    </LayoutShell>
  );
}
