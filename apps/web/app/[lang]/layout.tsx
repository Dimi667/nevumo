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

  return (
    <>
      {modal !== 'true' && embed !== '1' && <GlobalHeader lang={lang} />}
      {children}
      {modal !== 'true' && <SmartGlobalFooter lang={lang} />}
    </>
  );
}
