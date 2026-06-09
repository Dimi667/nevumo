import { generateHreflangAlternates } from '@/lib/seo';
import { SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE } from '@/lib/locales';
import WithdrawalClient from './WithdrawalClient';

type PageProps = {
  params: Promise<{ lang: string }>;
  searchParams: Promise<{ modal?: string }>;
};

export async function generateMetadata({ params, searchParams }: PageProps) {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : DEFAULT_LANGUAGE;
  const isModal = (await searchParams)?.modal === 'true';

  return {
    robots: isModal ? { index: false, follow: true } : { index: true, follow: true },
    alternates: isModal ? undefined : {
      canonical: `/${normalizedLang}/withdrawal`,
      languages: generateHreflangAlternates('/withdrawal'),
    },
  };
}

export default function WithdrawalPage(props: PageProps) {
  return <WithdrawalClient {...props} />;
}
