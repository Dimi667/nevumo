import OverviewClient from './OverviewClient';

export default async function ClientOverviewPage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  return <OverviewClient lang={lang} />;
}
