import { redirect } from 'next/navigation';

export default async function ClientDashboardPage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  redirect(`/${lang}/client/dashboard/overview`);
}
