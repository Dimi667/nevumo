import SmartGlobalFooter from '@/components/SmartGlobalFooter';

interface LangLayoutProps {
  children: React.ReactNode;
  params: Promise<{ lang: string }>;
  searchParams: Promise<{ modal?: string }>;
}

export default async function LangLayout({ children, params, searchParams }: LangLayoutProps) {
  const { lang } = await params;
  const { modal } = await searchParams || {};
  return (
    <>
      {children}
      {modal !== 'true' && <SmartGlobalFooter lang={lang} />}
    </>
  );
}
