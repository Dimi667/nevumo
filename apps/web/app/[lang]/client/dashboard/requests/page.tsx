import RequestsClient from './RequestsClient';

export default async function ClientRequestsPage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  return <RequestsClient lang={lang} />;
}
