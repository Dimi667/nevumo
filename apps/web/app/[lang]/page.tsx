import { SUPPORTED_LANGUAGES } from '@/lib/locales';
import { generateHreflangAlternates } from '@/lib/seo';
import { fetchTranslations, t } from '@/lib/ui-translations';
import Image from 'next/image';
import Link from 'next/link';
import RotatingCategory from '@/components/homepage/RotatingCategory';
import { AuthIntentButton } from './AuthIntentButton';
import CategoryIntentButton from '@/components/homepage/CategoryIntentButton';
import MobileStickyCTA from '@/components/homepage/MobileStickyCTA';

interface PageProps {
  params: Promise<{ lang: string }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { lang } = await params;
  const homepageT = await fetchTranslations(lang, 'homepage');

  return {
    title: t(homepageT, 'meta_title', 'Get clients for your services | Nevumo'),
    description: t(homepageT, 'meta_description', 'Free registration. No commission.'),
    alternates: {
      languages: generateHreflangAlternates('/'),
    },
  };
}

export function generateViewport() {
  return {
    width: 'device-width',
    initialScale: 1,
    viewportFit: 'cover',
    themeColor: '#f97316',
  };
}

export default async function Homepage({ params }: PageProps) {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : 'en';
  const homepageT = await fetchTranslations(lang, 'homepage');
  const rotatingCategories = t(homepageT, 'rotating_categories', 'Massage,Cleaning,Plumbing').split(',');

  return (
    <div className="min-h-screen bg-white">
      {/* NAVBAR */}
      <nav className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto">
        <Image 
          src="/Nevumo_logo.svg" 
          alt="Nevumo" 
          width={120} 
          height={36}
          priority
        />
        <Link
          href={`/${normalizedLang}/warszawa`}
          className="text-sm text-gray-600 transition-colors"
        >
          {t(homepageT, 'nav_link', 'Looking for a service?')}
        </Link>
      </nav>

      {/* HERO SECTION */}
      <section className="py-24 px-4 text-center bg-gradient-to-br from-orange-400 to-orange-700">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-4">
            {t(homepageT, 'hero_prefix', 'Get clients for')}{' '}
            <RotatingCategory categories={rotatingCategories} />
            {' '}{t(homepageT, 'hero_suffix', 'in Warsaw')}
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-white">
            {t(homepageT, 'hero_subtitle', 'Free. No commission. Direct contact.')}
          </p>
          
          <div className="flex flex-wrap justify-center gap-6 mb-8 text-sm md:text-base">
            <span className="flex items-center gap-2 text-white">
              <span className="text-white">✓</span> {t(homepageT, 'trust_1', 'No commission')}
            </span>
            <span className="flex items-center gap-2 text-white">
              <span className="text-white">✓</span> {t(homepageT, 'trust_2', '2 min registration')}
            </span>
            <span className="flex items-center gap-2 text-white">
              <span className="text-white">✓</span> {t(homepageT, 'trust_3', 'Real requests')}
            </span>
          </div>
          
          <div className="text-lg mb-10 text-orange-100">
            {t(homepageT, 'social_proof', '')}
          </div>
          
          <AuthIntentButton
            href={`/${normalizedLang}/auth`}
            intent="provider"
            className="bg-white text-orange-600 font-bold px-8 py-4 rounded-full hover:bg-orange-50 transition"
          >
            {t(homepageT, 'cta_hero', 'Start for free')}
          </AuthIntentButton>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="bg-gray-100 py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">{t(homepageT, 'how_title', 'How it works')}</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">{t(homepageT, 'step1_title', 'Create a profile')}</h3>
              <p className="text-gray-600">{t(homepageT, 'step1_sub', '2 minutes')}</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">{t(homepageT, 'step2_title', 'Receive client requests')}</h3>
              <p className="text-gray-600">{t(homepageT, 'step2_sub', 'immediately after registration')}</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">{t(homepageT, 'step3_title', 'Contact clients directly')}</h3>
              <p className="text-gray-600">{t(homepageT, 'step3_sub', 'no middlemen')}</p>
            </div>
          </div>
        </div>
      </section>

      {/* CATEGORY CARDS */}
      <section className="py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="nevumo-card text-center">
              <div className="text-orange-500 mb-3">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ff5a1f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/><path d="M20 3v4M22 5h-4M4 17v2M5 18H3"/></svg>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">{t(homepageT, 'cat_cleaning_name', 'Cleaning')}</h3>
              <p className="text-gray-600 mb-6">{t(homepageT, 'cat_cleaning_leads', '26 requests this week')}</p>
              <CategoryIntentButton
                href={`/${normalizedLang}/auth?category=cleaning`}
                category="cleaning"
                className="btn-primary w-full text-sm whitespace-nowrap"
              >
                {t(homepageT, 'cat_cta', 'I offer this service')}
              </CategoryIntentButton>
            </div>
            <div className="nevumo-card text-center">
              <div className="text-orange-500 mb-3">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ff5a1f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">{t(homepageT, 'cat_plumbing_name', 'Plumbing')}</h3>
              <p className="text-gray-600 mb-6">{t(homepageT, 'cat_plumbing_leads', '18 requests this week')}</p>
              <CategoryIntentButton
                href={`/${normalizedLang}/auth?category=plumbing`}
                category="plumbing"
                className="btn-primary w-full text-sm whitespace-nowrap"
              >
                {t(homepageT, 'cat_cta', 'I offer this service')}
              </CategoryIntentButton>
            </div>
            <div className="nevumo-card text-center">
              <div className="text-orange-500 mb-3">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ff5a1f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M12 5 9.04 7.96a2.17 2.17 0 0 0 0 3.08c.82.82 2.13.85 3 .07l2.07-1.9a2.82 2.82 0 0 1 3.79 0l2.96 2.66"/><path d="m18 15-2-2"/><path d="m15 18-2-2"/></svg>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">{t(homepageT, 'cat_massage_name', 'Massage')}</h3>
              <p className="text-gray-600 mb-6">{t(homepageT, 'cat_massage_leads', '14 requests this week')}</p>
              <CategoryIntentButton
                href={`/${normalizedLang}/auth?category=massage`}
                category="massage"
                className="btn-primary w-full text-sm whitespace-nowrap"
              >
                {t(homepageT, 'cat_cta', 'I offer this service')}
              </CategoryIntentButton>
            </div>
          </div>
        </div>
      </section>

      {/* LIVE ACTIVITY FEED */}
      <section className="py-16 px-6 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">{t(homepageT, 'activity_title', 'Recent requests')}</h2>
          <div className="space-y-4">
            <div className="nevumo-card flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-red-500">🔴</span>
                <span className="text-gray-900">{t(homepageT, 'activity_1', '')}</span>
              </div>
              <span className="text-gray-500 text-sm">{t(homepageT, 'activity_1_time', '')}</span>
            </div>
            <div className="nevumo-card flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-red-500">🔴</span>
                <span className="text-gray-900">{t(homepageT, 'activity_2', '')}</span>
              </div>
              <span className="text-gray-500 text-sm">{t(homepageT, 'activity_2_time', '')}</span>
            </div>
            <div className="nevumo-card flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-red-500">🔴</span>
                <span className="text-gray-900">{t(homepageT, 'activity_3', '')}</span>
              </div>
              <span className="text-gray-500 text-sm">{t(homepageT, 'activity_3_time', '')}</span>
            </div>
          </div>
        </div>
      </section>

      {/* WHY NEVUMO */}
      <section className="py-16 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-12 text-gray-900">{t(homepageT, 'why_title', '')}</h2>
          <div className="space-y-6 text-left max-w-2xl mx-auto">
            <div className="flex items-start gap-3">
              <span className="text-green-500 text-xl mt-1">✓</span>
              <div>
                <h3 className="font-semibold text-gray-900">{t(homepageT, 'why_1_title', 'Free')}</h3>
                <p className="text-gray-600">{t(homepageT, 'why_1_sub', '')}</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-green-500 text-xl mt-1">✓</span>
              <div>
                <h3 className="font-semibold text-gray-900">{t(homepageT, 'why_2', '')}</h3>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-green-500 text-xl mt-1">✓</span>
              <div>
                <h3 className="font-semibold text-gray-900">{t(homepageT, 'why_3', '')}</h3>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SECOND CTA */}
      <section className="py-20 px-6 bg-gray-100" id="second-cta">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-8 text-gray-900">{t(homepageT, 'cta2_title', '')}</h2>
          <AuthIntentButton
            href={`/${normalizedLang}/auth`}
            intent="provider"
            className="btn-primary text-lg px-8 py-4 inline-block"
          >
            {t(homepageT, 'cta2_btn', '')}
          </AuthIntentButton>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="py-12 px-6 bg-gray-50 border-t border-gray-200">
        <div className="max-w-4xl mx-auto text-center">
          <p className="mb-6 text-gray-700">{t(homepageT, 'footer_title', '')}</p>
          <div className="flex flex-wrap justify-center gap-4 mb-6 text-sm">
            <Link href={`/${normalizedLang}/warszawa/sprzatanie`} className="text-gray-700 transition-colors">
              {t(homepageT, 'footer_link_cleaning', '')}
            </Link>
            <span className="text-gray-500">|</span>
            <Link href={`/${normalizedLang}/warszawa/hydraulik`} className="text-gray-700 transition-colors">
              {t(homepageT, 'footer_link_plumbing', '')}
            </Link>
            <span className="text-gray-500">|</span>
            <Link href={`/${normalizedLang}/warszawa/masaz`} className="text-gray-700 transition-colors">
              {t(homepageT, 'footer_link_massage', '')}
            </Link>
          </div>
          <p className="text-gray-500 text-sm">
            {t(homepageT, 'footer_popular', '')}
          </p>
        </div>
      </footer>

      {/* MOBILE STICKY CTA */}
      <MobileStickyCTA>
        <AuthIntentButton
          href={`/${normalizedLang}/auth`}
          intent="provider"
          className="btn-primary w-full text-center block"
        >
          {t(homepageT, 'cta_hero', 'Start for free')}
        </AuthIntentButton>
      </MobileStickyCTA>
    </div>
  );
}
