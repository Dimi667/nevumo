import JobsClient from './JobsClient';

export default async function ClientJobsPage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  return <JobsClient lang={lang} />;
}
