import Link from 'next/link';
import Image from 'next/image';
import { SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE } from '@/lib/locales';
import { t, type TranslationDict } from '@/lib/ui-translations';
import { generateHreflangAlternates } from '@/lib/seo';

interface PageProps {
  params: Promise<{ lang: string }>;
  searchParams: Promise<{ modal?: string }>;
}

const API_BASE = typeof window === 'undefined' ? (process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');

// For PDF button, always use browser-accessible URL
const PDF_API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function getTranslations(lang: string): Promise<TranslationDict> {
  try {
    const res = await fetch(
      `${API_BASE}/api/v1/translations/terms?lang=${lang}`,
      { next: { revalidate: 3600 } }
    );
    if (!res.ok) return {};
    return (await res.json()) as TranslationDict;
  } catch (error) {
    console.error('Fetch error:', error);
    return {};
  }
}

export async function generateStaticParams() {
  return SUPPORTED_LANGUAGES.map((lang) => ({ lang }));
}

export async function generateMetadata({ params, searchParams }: PageProps) {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : DEFAULT_LANGUAGE;
  const dict = await getTranslations(normalizedLang);

  const title = t(dict, 'page_title', 'Terms & Conditions — Nevumo');
  const description = t(dict, 'meta_description', 'Terms and conditions for using the Nevumo platform.');

  const { modal } = await searchParams;
  const isModal = modal === 'true';

  return {
    title,
    description,
    robots: isModal ? { index: false, follow: true } : { index: true, follow: true },
    alternates: isModal ? undefined : {
      canonical: `/${normalizedLang}/terms`,
      languages: generateHreflangAlternates('/terms'),
    },
    openGraph: isModal ? undefined : {
      title,
      description,
      url: `${process.env.NEXT_PUBLIC_SITE_URL}/${normalizedLang}/terms`,
      siteName: 'Nevumo',
      locale: normalizedLang,
      type: 'website' as const,
    },
  };
}

export default async function TermsPage({ params, searchParams }: PageProps) {
  const { lang } = await params;
  const { modal } = await searchParams;
  const isModal = modal === 'true';
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : DEFAULT_LANGUAGE;
  const dict = await getTranslations(normalizedLang);

  const renderBody = (text: string, isPl: boolean) => {
    if (!text) return null;
    return text.split('\n\n').map((paragraph, index) => {
      const isPlParagraph = paragraph.includes('[PL]');
      const cleanParagraph = paragraph.replace(/\[PL\]/g, '').trim();

      if (isPlParagraph && isPl) {
        return (
          <div key={index} className="border-l-4 border-blue-500 pl-3 mb-3">
            <span className="text-[10px] font-bold text-blue-600 uppercase block mb-1">PL</span>
            <p className="text-gray-700 leading-relaxed">{cleanParagraph}</p>
          </div>
        );
      }

      return (
        <p key={index} className="text-gray-700 leading-relaxed mb-3">
          {cleanParagraph}
        </p>
      );
    });
  };

  const getWarningText = (lang: string) => {
    if (lang === 'pl') return "Ten formularz dotyczy wyłącznie umowy z Nevumo — operatorem platformy. Nie dotyczy umów z Usługodawcami.";
    if (lang === 'bg') return "Този формуляр се отнася единствено до договора с Nevumo — оператора на платформата. Не се отнася до договори с доставчици на услуги.";
    return "This form applies only to the contract with Nevumo — the platform operator. It does not apply to contracts with service providers.";
  };

  const articles = Array.from({ length: 15 }, (_, i) => i + 1);

  return (
    <div className="min-h-screen bg-white">
      <main className="max-w-3xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{t(dict, 'page_title', 'Terms & Conditions')}</h1>
        <div className="text-sm text-gray-500 mb-8">
          {t(dict, 'effective_date', 'Effective date: 11.05.2026')} | {t(dict, 'version', 'Version: 1.0')}
        </div>

        {normalizedLang === 'pl' && t(dict, 'pl_notice') && (
          <div className="bg-blue-50 border border-blue-200 rounded-md p-4 text-blue-900 text-sm my-6">
            {t(dict, 'pl_notice')}
          </div>
        )}

        {articles.map((num) => (
          <section key={num} className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">
              {t(dict, `art${num}_title`, `Article ${num}`)}
            </h2>
            <div>
              {renderBody(t(dict, `art${num}_body`), normalizedLang === 'pl')}
            </div>
          </section>
        ))}

        <section className="mb-8">
          <h2 className="font-semibold text-xl mt-8 mb-3">
            {t(dict, 'annex1_title', 'Annex 1')}
          </h2>
          
          <div className="bg-amber-50 border border-amber-300 rounded-md p-4 text-amber-900 text-sm mb-4">
            {getWarningText(normalizedLang)}
          </div>

          <div>
            {renderBody(t(dict, 'annex1_body'), normalizedLang === 'pl')}
          </div>

          <div className="mt-6 flex flex-col sm:flex-row gap-4">
            <a
              href={`${PDF_API_BASE}/api/v1/legal/withdrawal-form/${normalizedLang}`}
              download={`withdrawal-form-${normalizedLang}.pdf`}
              className="inline-flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
            >
              <svg className="-ml-1 mr-2 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              {t(dict, 'download_pdf', 'Download PDF')}
            </a>
            <Link
              href={`/${normalizedLang}/withdrawal`}
              className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-orange-600 hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
            >
              {t(dict, 'online_form', 'Online form')}
            </Link>
          </div>
        </section>
      </main>
    </div>
  );
}
