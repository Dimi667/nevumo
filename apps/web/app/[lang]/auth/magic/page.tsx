import MagicLinkClient from './MagicLinkClient';

interface MagicLinkPageProps {
  params: { lang: string };
  searchParams: { token?: string };
}

export default function MagicLinkPage({ params, searchParams }: MagicLinkPageProps) {
  const { lang } = params;
  const token = searchParams.token || '';

  return <MagicLinkClient lang={lang} token={token} />;
}
