import MagicLinkClient from './MagicLinkClient';

interface MagicLinkPageProps {
  params: Promise<{ lang: string }>;
  searchParams: Promise<{ token?: string }>;
}

export default async function MagicLinkPage({ params, searchParams }: MagicLinkPageProps) {
  const { lang } = await params;
  const { token } = await searchParams;

  return <MagicLinkClient lang={lang} token={token || ''} />;
}
