import Link from 'next/link';
import Image from 'next/image';
import { SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE } from '@/lib/locales';
import { fetchTranslations, t } from '@/lib/ui-translations';
import { generateHreflangAlternates, getBaseIcons } from '@/lib/seo';
import { ReactNode } from 'react';

interface PageProps {
  params: Promise<{ lang: string }>;
  searchParams: Promise<{ modal?: string }>;
}

export async function generateStaticParams() {
  return SUPPORTED_LANGUAGES.map((lang) => ({ lang }));
}

export async function generateMetadata({ params }: PageProps) {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : DEFAULT_LANGUAGE;
  const dict = await fetchTranslations(normalizedLang, 'provider_terms');

  const title = t(dict, 'page_title', 'Terms & Conditions for Service Providers');
  const description = t(dict, 'meta_description', 'Terms and conditions for service providers on the Nevumo platform.');

  return {
    title,
    description,
    alternates: {
      canonical: `/${normalizedLang}/terms-provider`,
      languages: generateHreflangAlternates('/terms-provider'),
    },
    openGraph: {
      title,
      description,
      url: `${process.env.NEXT_PUBLIC_SITE_URL}/${normalizedLang}/terms-provider`,
      siteName: 'Nevumo',
      locale: normalizedLang,
      type: 'website',
    },
    ...getBaseIcons(),
  };
}

function renderBodyText(text: string, lang: string): ReactNode[] {
  const paragraphs = text.split('\n\n').filter(p => p.trim());
  
  return paragraphs.map((paragraph, index) => {
    const hasPLMarker = paragraph.startsWith('[PL]');
    let content = paragraph;
    let plStyled = false;

    if (hasPLMarker) {
      content = paragraph.replace(/^\[PL\]\s*/, '').trim();
      if (lang === 'pl') {
        plStyled = true;
      }
    }

    if (plStyled) {
      return (
        <div key={index} className="border-l-4 border-blue-500 pl-3 mb-3">
          <span className="text-xs text-blue-600 font-medium block mb-1">🇵🇱 Польска specyfika</span>
          <p className="text-gray-700 leading-relaxed">{content}</p>
        </div>
      );
    }

    return <p key={index} className="text-gray-700 leading-relaxed mb-3">{content}</p>;
  });
}

export default async function TermsProviderPage({ params, searchParams }: PageProps) {
  const { lang } = await params;
  const { modal } = await searchParams;
  const isModal = modal === 'true';
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : DEFAULT_LANGUAGE;
  const dict = await fetchTranslations(normalizedLang, 'provider_terms');

  return (
    <div className="min-h-screen bg-white">
      <main>
        <article className="max-w-3xl mx-auto px-4 py-12">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{t(dict, 'page_title', 'Terms & Conditions for Service Providers')}</h1>
          <p className="text-sm text-muted-foreground mb-8">
            {t(dict, 'effective_date', 'Effective date: 1 June 2026')} |{' '}
            {t(dict, 'version', 'Version: 1.0')}
          </p>

          {t(dict, 'operator_info') && (
            <div className="bg-gray-50 border border-gray-200 rounded-md p-4 text-sm text-gray-700 mb-6">
              {t(dict, 'operator_info')}
            </div>
          )}

          {normalizedLang === 'pl' && t(dict, 'pl_notice') && (
            <div className="bg-blue-50 border border-blue-200 rounded-md p-4 text-blue-900 text-sm my-6">
              {t(dict, 'pl_notice')}
            </div>
          )}

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art1_title', '1. General Provisions')}</h2>
            <div>{renderBodyText(t(dict, 'art1_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art2_title', '2. Definitions')}</h2>
            <div>{renderBodyText(t(dict, 'art2_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art3_title', '3. Registration and Account')}</h2>
            <div>{renderBodyText(t(dict, 'art3_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art4_title', '4. Provider Profile and Service Listings')}</h2>
            <div>{renderBodyText(t(dict, 'art4_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art5_title', '5. Ranking and Visibility')}</h2>
            <div>{renderBodyText(t(dict, 'art5_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art6_title', '6. Commission, Payments, and Pricing')}</h2>
            <div>{renderBodyText(t(dict, 'art6_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art7_title', '7. Provider Obligations')}</h2>
            <div>{renderBodyText(t(dict, 'art7_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art8_title', '8. Account Suspension, Restriction, and Termination')}</h2>
            <div>{renderBodyText(t(dict, 'art8_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art9_title', '9. KYC and Trader Declaration')}</h2>
            <div>{renderBodyText(t(dict, 'art9_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art10_title', '10. Amendments to These Terms')}</h2>
            <div>{renderBodyText(t(dict, 'art10_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art11_title', '11. Access to Your Data')}</h2>
            <div>{renderBodyText(t(dict, 'art11_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art12_title', '12. Internal Complaint-Handling System')}</h2>
            <div>{renderBodyText(t(dict, 'art12_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art13_title', '13. Mediation')}</h2>
            <div>{renderBodyText(t(dict, 'art13_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art14_title', '14. Limitation of Liability')}</h2>
            <div>{renderBodyText(t(dict, 'art14_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art15_title', '15. Intellectual Property')}</h2>
            <div>{renderBodyText(t(dict, 'art15_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art16_title', '16. Data Protection')}</h2>
            <div>{renderBodyText(t(dict, 'art16_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art17_title', '17. Applicable Law and Jurisdiction')}</h2>
            <div>{renderBodyText(t(dict, 'art17_body', ''), normalizedLang)}</div>
          </section>

          <section className="mb-8">
            <h2 className="font-semibold text-xl mt-8 mb-3">{t(dict, 'art18_title', '18. Final Provisions')}</h2>
            <div>{renderBodyText(t(dict, 'art18_body', ''), normalizedLang)}</div>
          </section>
        </article>
      </main>
    </div>
  );
}
