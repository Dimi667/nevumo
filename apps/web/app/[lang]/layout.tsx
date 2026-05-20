import { headers } from 'next/headers';
import SmartGlobalFooter from '@/components/SmartGlobalFooter';
import GlobalHeader from '@/components/GlobalHeader';

interface LangLayoutProps {
  children: React.ReactNode;
  params: Promise<{ lang: string }>;
  searchParams: Promise<{ modal?: string; embed?: string }>;
}

export default async function LangLayout({ children, params, searchParams }: LangLayoutProps) {
  const { lang } = await params;
  const { modal, embed } = await searchParams || {};
  const headersList = await headers();
  const pathname = headersList.get('x-pathname') || '';
  const isDashboard = pathname.includes('/client/dashboard/') || pathname.includes('/provider/dashboard/');

  return (
    <>
      {!isDashboard && modal !== 'true' && embed !== '1' && <GlobalHeader lang={lang} />}
      {children}
      {!isDashboard && modal !== 'true' && <SmartGlobalFooter lang={lang} />}
    </>
  );
}
