import Link from 'next/link';
import Image from 'next/image';
import { SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE } from '@/lib/locales';
import { fetchTranslations, t } from '@/lib/ui-translations';
import { generateHreflangAlternates } from '@/lib/seo';

interface PageProps {
  params: Promise<{ lang: string }>;
}

export async function generateStaticParams() {
  return SUPPORTED_LANGUAGES.map((lang) => ({ lang }));
}

export async function generateMetadata({ params }: PageProps) {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : DEFAULT_LANGUAGE;
  const dict = await fetchTranslations(normalizedLang, 'contact_dsa');

  const title = t(dict, 'page_title', 'DSA Contact Point');
  const description = t(dict, 'meta_description', 'Contact point for authorities and users under the Digital Services Act (DSA).');

  return {
    title,
    description,
    alternates: {
      canonical: `/${normalizedLang}/contact-dsa`,
      languages: generateHreflangAlternates('/contact-dsa'),
    },
    openGraph: {
      title,
      description,
      url: `${process.env.NEXT_PUBLIC_SITE_URL}/${normalizedLang}/contact-dsa`,
      siteName: 'Nevumo',
      locale: normalizedLang,
      type: 'website',
    },
  };
}

export default async function ContactDSAPage({ params }: PageProps) {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : DEFAULT_LANGUAGE;
  const dict = await fetchTranslations(normalizedLang, 'contact_dsa');

  return (
    <div className="min-h-screen bg-white">
      {/* NAVBAR */}
      <nav className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto border-b border-gray-100">
        <Link href={`/${normalizedLang}`} className="inline-flex items-center">
          <Image src="/Nevumo_logo.svg" alt="Nevumo" width={120} height={36} priority />
        </Link>
        <Link href={`/${normalizedLang}`} className="text-sm text-gray-600 transition-colors hover:text-orange-600">
          {t(dict, 'back_to_home', 'Back to home')}
        </Link>
      </nav>

      <main>
        <article className="max-w-3xl mx-auto px-4 py-12">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">{t(dict, 'page_title', 'DSA Contact Point')}</h1>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 's1_title')}</h2>
            <p className="text-gray-700 leading-relaxed">
              {t(dict, 's1_body')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 's2_title')}</h2>
            <p className="text-gray-700 leading-relaxed mb-4">
              {t(dict, 's2_body')}
            </p>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-gray-700">{t(dict, 's2_email_privacy')}</span>
                <a href="mailto:privacy@nevumo.com" className="text-orange-600 hover:underline">privacy@nevumo.com</a>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-gray-700">{t(dict, 's2_email_legal')}</span>
                <a href="mailto:legal@nevumo.com" className="text-orange-600 hover:underline">legal@nevumo.com</a>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 's3_title')}</h2>
            <p className="text-gray-700 leading-relaxed mb-4">
              {t(dict, 's3_body')}
            </p>
            <h3 className="text-lg font-semibold mb-2">{t(dict, 's3_what_to_include_title')}</h3>
            <ol className="list-decimal pl-6 space-y-2 text-gray-700">
              {t(dict, 's3_what_to_include_body').split('\n').map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ol>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 's4_title')}</h2>
            <ul className="list-disc pl-6 space-y-2 text-gray-700">
              {t(dict, 's4_body').split('\n').map((item, index) => {
                const cleanItem = item.replace(/^•\s*/, '').trim();
                return cleanItem ? <li key={index}>{cleanItem}</li> : null;
              })}
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 's5_title')}</h2>
            <p className="text-gray-700 leading-relaxed">
              {t(dict, 's5_body')}
            </p>
          </section>
        </article>
      </main>
    </div>
  );
}
