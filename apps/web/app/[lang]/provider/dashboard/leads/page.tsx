import LeadsClient from './LeadsClient';

export default async function LeadsPage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  return <LeadsClient />;
}
