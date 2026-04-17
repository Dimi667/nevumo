import SettingsClient from './SettingsClient';

export default async function ClientSettingsPage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  return <SettingsClient lang={lang} />;
}
