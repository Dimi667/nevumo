import Link from 'next/link';
import Image from 'next/image';
import type { Metadata } from 'next';
import { getProviderBySlug, getProviders, getPriceRange, PriceRangeData, getCityBySlug } from '@/lib/api';
import { generateHreflangAlternates } from '@/lib/seo';
import { fetchTranslations, t } from '@/lib/ui-translations';
import { JsonLd } from '@/components/JsonLd';
import LeadForm from '@/components/category/LeadForm';
import CategoryPageClient from '@/components/category/CategoryPageClient';

interface PageProps {
  params: Promise<{ lang: string; city: string; category: string }>;
}

type CategoryKey = 'masaz' | 'sprzatanie' | 'hydraulik';
type TranslationCategoryKey = 'cleaning' | 'plumbing' | 'massage';
type ApiCategorySlug = 'massage' | 'cleaning' | 'plumbing';

interface CategoryContent {
  apiSlug: ApiCategorySlug;
  displayName: string;
  heading: string;
  subtitle: string;
  metadataTitle: string;
  metadataDescription: string;
  seoTitle: string;
  seoParagraphs: [string, string, string];
  seoQuestions: [string, string];
  relatedLinks: Array<{ href: string; label: string }>;
  faq: Array<{ question: string; answer: string }>;
}

interface EnrichedProvider {
  id: string;
  slug: string;
  businessName: string;
  rating: number;
  profileImageUrl: string | null;
  description: string | null;
  jobsCompleted: number;
  latestLeadPreviewCreatedAt: string | null;
}

interface ProviderCardTexts {
  defaultDescription: string;
  jobsCompleted: string;
  lastRequest: string;
  directContact: string;
  sendRequest: string;
}

const categorySlugMap: Record<string, string> = {
  masaz: 'massage',
  sprzatanie: 'cleaning',
  hydraulik: 'plumbing',
};

const categoryKeyMap: Record<string, TranslationCategoryKey> = {
  masaz: 'massage',
  sprzatanie: 'cleaning',
  hydraulik: 'plumbing',
};

function getApiSlug(category: string): ApiCategorySlug {
  return (categorySlugMap[category] ?? category) as ApiCategorySlug;
}

function getCategoryTranslationKey(category: string): TranslationCategoryKey {
  return categoryKeyMap[category] ?? 'cleaning';
}

function getInitials(name: string): string {
  return name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part.charAt(0).toUpperCase())
    .join('');
}

function ProviderCard({
  provider,
  href,
  texts,
}: {
  provider: EnrichedProvider;
  href: string;
  texts: ProviderCardTexts;
}) {
  const latestLeadTime = provider.latestLeadPreviewCreatedAt
    ? formatRelativeTime(provider.latestLeadPreviewCreatedAt)
    : null;

  return (
    <article className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
      <div className="flex items-start gap-4">
        <Link href={href} className="shrink-0">
          <div className="flex h-16 w-16 items-center justify-center overflow-hidden rounded-full bg-orange-100 text-lg font-bold text-orange-600">
            {provider.profileImageUrl ? (
              <img
                src={provider.profileImageUrl}
                alt={provider.businessName}
                className="h-full w-full object-cover"
              />
            ) : (
              <span>{getInitials(provider.businessName)}</span>
            )}
          </div>
        </Link>

        <div className="min-w-0 flex-1">
          <Link href={href} className="block">
            <h2 className="text-lg font-bold text-gray-900 transition hover:text-orange-600">
              {provider.businessName}
            </h2>
          </Link>

          {provider.rating > 0 && (
            <div className="mt-1 flex items-center gap-2 text-sm font-medium text-amber-600">
              <span>⭐⭐⭐⭐⭐</span>
              <span>{provider.rating.toFixed(1)}</span>
            </div>
          )}

          <p className="mt-3 line-clamp-2 text-sm leading-6 text-gray-600">
            {provider.description ?? texts.defaultDescription}
          </p>

          <div className="mt-4 flex flex-wrap gap-2 text-xs font-medium text-gray-600">
            {provider.jobsCompleted > 0 && (
              <span className="rounded-full bg-gray-50 px-3 py-1.5">
                ✔ {provider.jobsCompleted} {texts.jobsCompleted}
              </span>
            )}
            {latestLeadTime && (
              <span className="rounded-full bg-gray-50 px-3 py-1.5">
                ✔ {texts.lastRequest}: {latestLeadTime}
              </span>
            )}
            <span className="rounded-full bg-gray-50 px-3 py-1.5">
              ✔ {texts.directContact}
            </span>
          </div>

          <Link
            href={href}
            className="mt-5 inline-flex w-full items-center justify-center rounded-xl bg-orange-500 px-4 py-3 text-sm font-semibold text-white transition hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-offset-2"
          >
            {texts.sendRequest}
          </Link>
        </div>
      </div>
    </article>
  );
}

const CATEGORY_CONTENT: Record<CategoryKey, CategoryContent> = {
  masaz: {
    apiSlug: 'massage',
    displayName: 'massage',
  heading: '{category} in {city}',
    subtitle:
      'Find trusted massage specialists in {city}. Free request, no obligation.',
    metadataTitle: 'Massage in {city} | Nevumo',
    metadataDescription:
      'Find trusted massage specialists in {city}. Free request, no obligation. Reply in as little as 30 minutes.',
    seoTitle: 'Massage in {city} — what is worth knowing?',
    seoParagraphs: [
      '{city} offers a wide selection of professional massage specialists. Whether you are looking for relaxing, sports, or therapeutic massage, Nevumo helps you find trusted professionals nearby.',
      'Check previous client reviews, specialist experience, and the scope of services offered. A good massage specialist will adapt the technique to your needs.',
      '',
    ],
    seoQuestions: ['How to choose a massage specialist?', ''],
    relatedLinks: [
      { href: '/{lang}/{city_slug}/sprzatanie', label: 'Cleaning in {city}' },
      { href: '/{lang}/{city_slug}/hydraulik', label: 'Plumbing in {city}' },
    ],
    faq: [
      {
        question: 'How to find a massage specialist in {city}?',
        answer:
          'On Nevumo you can send a free request to trusted massage specialists in {city} and receive a response in as little as 30 minutes.',
      },
      {
        question: 'How much does massage cost in {city}?',
        answer: '',
      },
      {
        question: 'Is the request free?',
        answer:
          'Yes, sending a request through Nevumo is completely free and without obligation.',
      },
    ],
  },
  sprzatanie: {
    apiSlug: 'cleaning',
    displayName: 'cleaning',
    heading: '{category} in {city}',
    subtitle:
      'Find trusted cleaning specialists in {city}. Free request, no obligation.',
    metadataTitle: 'Cleaning in {city} | Nevumo',
    metadataDescription:
      'Find trusted cleaning companies in {city}. Free request, no obligation.',
    seoTitle: 'Cleaning in {city} — what is worth knowing?',
    seoParagraphs: [
      'Professional cleaning companies in {city} offer comprehensive services for homes, apartments, and offices. On Nevumo you can find trusted specialists available across the city.',
      'Pay attention to customer reviews, scope of services, and scheduling flexibility. The best companies often offer recurring service discounts.',
      '',
    ],
    seoQuestions: ['How to choose a cleaning company?', 'How much does cleaning cost in {city}?'],
    relatedLinks: [
      { href: '/{lang}/{city_slug}/masaz', label: 'Massage in {city}' },
      { href: '/{lang}/{city_slug}/hydraulik', label: 'Plumbing in {city}' },
    ],
    faq: [
      {
        question: 'How to find a cleaning company in {city}?',
        answer:
          'On Nevumo you can send a free request to trusted cleaning companies in {city} and quickly receive responses from available specialists.',
      },
      {
        question: 'How much does cleaning cost in {city}?',
        answer: '',
      },
      {
        question: 'Is the request free?',
        answer:
          'Yes, sending a request through Nevumo is completely free and without obligation.',
      },
    ],
  },
  hydraulik: {
    apiSlug: 'plumbing',
    displayName: 'plumbing',
    heading: '{category} in {city}',
    subtitle:
      'Find a trusted plumber in {city}. Free request, no obligation.',
    metadataTitle: 'Plumbing in {city} | Nevumo',
    metadataDescription:
      'Find a trusted plumber in {city}. Fast response, free request.',
    seoTitle: 'Plumbing in {city} — what is worth knowing?',
    seoParagraphs: [
      'Plumbing issues require a fast response. On Nevumo you can find trusted plumbers in {city}, including urgent availability. Free request, quick response.',
      'You usually call a plumber for water system failures, leaking taps, blocked drains, or bathroom and kitchen renovation work.',
      '',
    ],
    seoQuestions: ['When should you call a plumber?', 'How much does a plumber cost in {city}?'],
    relatedLinks: [
      { href: '/{lang}/{city_slug}/masaz', label: 'Massage in {city}' },
      { href: '/{lang}/{city_slug}/sprzatanie', label: 'Cleaning in {city}' },
    ],
    faq: [
      {
        question: 'How to find a plumber in {city}?',
        answer:
          'On Nevumo you can send a free request to trusted plumbers in {city} and receive a response quickly.',
      },
      {
        question: 'How much does a plumber cost in {city}?',
        answer: '',
      },
      {
        question: 'Is the request free?',
        answer:
          'Yes, sending a request through Nevumo is completely free and without obligation.',
      },
    ],
  },
};

function getCategoryContent(
  category: string,
  cityName: string,
  categoryName: string,
  lang: string = 'en',
  citySlug: string = '',
): CategoryContent {
  const base = CATEGORY_CONTENT[(category as CategoryKey)] ?? CATEGORY_CONTENT.masaz;

  const replace = (str: string) =>
    str
      .replace(/{city}/g, cityName)
      .replace(/{category}/g, categoryName)
      .replace(/{lang}/g, lang)
      .replace(/{city_slug}/g, citySlug);

  return {
    ...base,
    heading: replace(base.heading),
    subtitle: replace(base.subtitle),
    metadataTitle: replace(base.metadataTitle),
    metadataDescription: replace(base.metadataDescription),
    seoTitle: replace(base.seoTitle),
    seoParagraphs: base.seoParagraphs.map(replace) as [string, string, string],
    seoQuestions: base.seoQuestions.map(replace) as [string, string],
    relatedLinks: base.relatedLinks.map((link) => ({
      href: replace(link.href),
      label: replace(link.label),
    })),
    faq: base.faq.map((f) => ({
      question: replace(f.question),
      answer: replace(f.answer),
    })),
  };
}

function formatRelativeTime(dateString: string): string {
  const diffMs = Date.now() - new Date(dateString).getTime();
  const diffMinutes = Math.max(1, Math.round(diffMs / 60000));

  if (diffMinutes < 60) {
    return `${diffMinutes} min temu`;
  }

  const diffHours = Math.round(diffMinutes / 60);
  if (diffHours < 24) {
    return `${diffHours} godz. temu`;
  }

  const diffDays = Math.round(diffHours / 24);
  return `${diffDays} dni temu`;
}

// Helper function to get price text based on price data and translations
function getPriceText(
  priceData: PriceRangeData | null,
  translations: Record<string, string>,
  key_prefix: 'price_text' | 'price_faq' | 'price_meta',
  fallback: string = '',
): string {
  if (priceData === null) {
    return t(translations, `${key_prefix}_none`, fallback);
  }

  if (priceData.min === priceData.max) {
    const template = t(translations, `${key_prefix}_single`, fallback);
    return template
      .replace('{price}', String(priceData.min))
      .replace('{currency}', priceData.currency);
  }

  const template = t(translations, `${key_prefix}_range`, fallback);
  return template
    .replace('{min}', String(priceData.min))
    .replace('{max}', String(priceData.max))
    .replace('{currency}', priceData.currency);
}

function buildFaqJsonLd(
  content: CategoryContent,
  priceData: PriceRangeData | null,
  translations: Record<string, string>,
): Record<string, unknown> {
  // Find the price question and replace its answer with price_faq text
  const priceQuestionKeywords = ['kosztu', 'price', 'cost', 'cena'];
  const updatedFaq = content.faq.map((item) => {
    const isPriceQuestion = priceQuestionKeywords.some(keyword =>
      item.question.toLowerCase().includes(keyword.toLowerCase()),
    );
    if (isPriceQuestion && priceData !== null) {
      const priceFaqText = getPriceText(priceData, translations, 'price_faq', item.answer);
      return {
        ...item,
        answer: priceFaqText,
      };
    }
    return item;
  });

  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: updatedFaq.map((item) => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: item.answer,
      },
    })),
  };
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { lang, city, category } = await params;
  const categoryT = await fetchTranslations(lang, 'category');
  const homepageT = await fetchTranslations(lang, 'homepage');
  const cityData = await getCityBySlug(city, lang);
  const cityName = cityData?.city || city.charAt(0).toUpperCase() + city.slice(1);
  const catKey = getCategoryTranslationKey(category);
  const catNameKey = `cat_${catKey}_name` as const;
  const categoryName = t(homepageT, catNameKey, catKey);

  const title = `${t(categoryT, `h1_${catKey}`, `${categoryName} in ${cityName}`)} | Nevumo`;
  const baseDescription = t(categoryT, `subtitle_${catKey}`, '');
  
  // Fetch price range for metadata
  const apiSlug = getApiSlug(category);
  const priceData = await getPriceRange(apiSlug, city);
  const priceMetaText = getPriceText(priceData, categoryT, 'price_meta', '');
  const description = priceMetaText ? `${baseDescription} ${priceMetaText}` : baseDescription;

  return {
    title,
    description,
    alternates: {
      languages: generateHreflangAlternates(`/${city}/${category}`),
    },
    openGraph: {
      title,
      description,
    },
  };
}

async function getEnrichedProviders(
  lang: string,
  city: string,
  category: string,
): Promise<{ allCount: number; providers: EnrichedProvider[]; averageRating: number }> {
  const listItems = await getProviders(category, city, lang);

  const details = await Promise.all(
    listItems.map(async (provider) => {
      const detail = await getProviderBySlug(provider.slug, lang, city);
      return {
        id: provider.id,
        slug: provider.slug,
        businessName: provider.business_name,
        rating: detail?.rating ?? provider.rating,
        profileImageUrl: detail?.profile_image_url ?? null,
        description: detail?.description ?? null,
        jobsCompleted: detail?.jobs_completed ?? 0,
        latestLeadPreviewCreatedAt: detail?.latest_lead_preview?.created_at ?? null,
      } satisfies EnrichedProvider;
    }),
  );

  const ratedProviders = listItems.filter((provider) => provider.rating > 0);
  const averageRating = ratedProviders.length > 0
    ? ratedProviders.reduce((sum, provider) => sum + provider.rating, 0) / ratedProviders.length
    : 4.8;

  return {
    allCount: listItems.length,
    providers: details,
    averageRating,
  };
}

export default async function CategoryPage({ params }: PageProps) {
  const { lang, city, category } = await params;
  const categoryT = await fetchTranslations(lang, 'category');
  const homepageT = await fetchTranslations(lang, 'homepage');
  const apiSlug = getApiSlug(category);
  const catKey = getCategoryTranslationKey(category);

  const cityData = await getCityBySlug(city, lang);
  const cityName = cityData?.city || city.charAt(0).toUpperCase() + city.slice(1);

  const catNameKey = `cat_${catKey}_name` as const;
  const categoryName = t(homepageT, catNameKey, catKey);

  const content = getCategoryContent(category, cityName, categoryName, lang, city);

  const heading = t(categoryT, `h1_${catKey}`, `${categoryName} in ${cityName}`);
  const subtitle = t(categoryT, `subtitle_${catKey}`, '');
  const providerCardTexts: ProviderCardTexts = {
    defaultDescription: t(categoryT, 'provider_desc_fallback', 'Проверен специалист в {city}. Изпратете кратко запитване и изчакайте връзка.').replace('{city}', cityName),
    jobsCompleted: t(categoryT, 'provider_jobs_completed', 'completed jobs'),
    lastRequest: t(categoryT, 'provider_last_request', 'Last request'),
    directContact: t(categoryT, 'provider_direct_contact', 'Direct contact'),
    sendRequest: t(categoryT, 'form_btn', 'Send request'),
  };

  const relatedLinksByCategory: Record<CategoryKey, Array<{ href: string; label: string }>> = {
    masaz: [
      { href: `/${lang}/${city}/sprzatanie`, label: t(categoryT, 'h1_cleaning', `Cleaning in ${cityName}`) },
      { href: `/${lang}/${city}/hydraulik`, label: t(categoryT, 'h1_plumbing', `Plumbing in ${cityName}`) },
    ],
    sprzatanie: [
      { href: `/${lang}/${city}/masaz`, label: t(categoryT, 'h1_massage', `Massage in ${cityName}`) },
      { href: `/${lang}/${city}/hydraulik`, label: t(categoryT, 'h1_plumbing', `Plumbing in ${cityName}`) },
    ],
    hydraulik: [
      { href: `/${lang}/${city}/masaz`, label: t(categoryT, 'h1_massage', `Massage in ${cityName}`) },
      { href: `/${lang}/${city}/sprzatanie`, label: t(categoryT, 'h1_cleaning', `Cleaning in ${cityName}`) },
    ],
  };
  const relatedLinks = relatedLinksByCategory[(category as CategoryKey)] ?? relatedLinksByCategory.sprzatanie;

  const { providers, allCount, averageRating } = await getEnrichedProviders(lang, city, apiSlug);
  const priceData = await getPriceRange(apiSlug, city);
  const priceText = getPriceText(priceData, categoryT, 'price_text', '');
  
  // Extract unique service titles from providers for chips
  const services = Array.from(
    new Set(
      providers
        .flatMap(provider => {
          // Extract service titles from provider data if available
          // For now, we'll use a basic approach - this might need adjustment based on actual provider data structure
          return provider.description && provider.description.length > 0
            ? [provider.description.split('.')[0]?.trim() || ''] // Use first sentence as service title
            : [];
        })
        .filter(title => title.length > 0 && title.length < 50) // Filter for reasonable length
    )
  ).map((title, index) => ({
    id: `service-${index}`,
    title
  })).slice(0, 8); // Limit to 8 services
  
  const CITY_COUNTRY_MAP: Record<string, string> = {
    'warszawa': 'PL',
    'sofia': 'BG',
    'belgrade': 'RS',
    'prague': 'CZ',
    'athens': 'GR',
  };
  
  const cityCountryCode = CITY_COUNTRY_MAP[city] ?? 'PL';
  const visibleProviders = providers.slice(0, 20);
  const hiddenProviders = providers.slice(20);
  const hiddenCount = hiddenProviders.length;
  const trustSpecialistsText = `${allCount > 0 ? allCount : 14} ${t(categoryT, 'trust_specialists', 'specialists')}`;
  const trustRatingText = `${averageRating.toFixed(1)} ${t(categoryT, 'trust_rating', 'rating')}`;
  const trustLeadsText = `120 ${t(categoryT, 'trust_requests', 'requests this month')}`;
  const faqJsonLd = buildFaqJsonLd(content, priceData, categoryT);

  return (
    <>
      <JsonLd data={faqJsonLd} />
      <div className="min-h-screen bg-white text-gray-900">
        <header className="border-b border-orange-100 bg-white/90 backdrop-blur">
          <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
            <Link href={`/${lang}`} className="inline-flex items-center">
              <Image src="/Nevumo_logo.svg" alt="Nevumo" width={120} height={36} priority />
            </Link>
            <Link href={`/${lang}`} className="text-sm font-semibold text-gray-700 transition hover:text-orange-600">
              {t(categoryT, 'nav_link', 'Become a specialist')}
            </Link>
          </div>
        </header>

        <main className="max-w-6xl mx-auto px-4 py-8">
          <section className="mb-8">
            <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              {heading}
            </h1>
            <p className="mt-3 max-w-3xl text-base text-gray-600 sm:text-lg">
              {subtitle}
            </p>
            <div className="mt-5 inline-flex flex-wrap items-center gap-x-3 gap-y-2 rounded-full bg-gray-50 px-4 py-3 text-sm text-gray-700">
              <span>{trustSpecialistsText}</span>
              <span className="text-gray-400">•</span>
              <span className="flex items-center gap-1">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" className="text-orange-400">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                {trustRatingText}
              </span>
              <span className="text-gray-400">•</span>
              <span>{trustLeadsText}</span>
              <span className="text-gray-400">•</span>
              <span className="flex items-center gap-1">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" className="text-orange-400">
                  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                </svg>
                {t(categoryT, 'trust_response', 'Avg. response: ~30 min')}
              </span>
            </div>
          </section>

          <div className="flex flex-col lg:flex-row gap-8">
            <div className="flex-1 min-w-0">
              <section className="space-y-4">
              {providers.length === 0 ? (
                <div className="rounded-xl border border-gray-100 bg-white px-6 py-12 text-center shadow-sm">
                  <div className="border-l-4 border-orange-400 pl-4 py-2 mb-4 text-left inline-block">
                    <p className="font-semibold text-gray-800 text-sm">
                      {t(categoryT, 'no_providers_title', 'Be the first to request this service in your area')}
                    </p>
                    <p className="text-sm text-gray-500 mt-0.5">
                      {t(categoryT, 'no_providers_subtitle', 'Providers joining Nevumo will see your request and contact you')}
                    </p>
                  </div>
                </div>
              ) : (
                <>
                  {visibleProviders.map((provider) => {
                    const providerHref = `/${lang}/${city}/${category}/${provider.slug}`;
                    return <ProviderCard key={provider.id} provider={provider} href={providerHref} texts={providerCardTexts} />;
                  })}
                  {hiddenCount > 0 && (
                    <details className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
                      <summary className="cursor-pointer list-none text-center text-sm font-semibold text-orange-600">
                        {t(categoryT, 'show_more', 'Show more')}
                      </summary>
                      <div className="mt-4 space-y-4">
                        {hiddenProviders.map((provider) => {
                          const providerHref = `/${lang}/${city}/${category}/${provider.slug}`;
                          return <ProviderCard key={provider.id} provider={provider} href={providerHref} texts={providerCardTexts} />;
                        })}
                      </div>
                    </details>
                  )}
                </>
              )}

              {/* Mobile Lead Form and Sticky Button */}
              <CategoryPageClient
                translations={categoryT}
                categorySlug={apiSlug}
                citySlug={city}
                lang={lang}
                cityName={cityName}
                services={services}
                cityCountryCode={cityCountryCode}
                stickyButtonLabel={t(categoryT, 'sticky_btn', 'Get offers — Free')}
              />

              <section className="mt-8 rounded-xl bg-gray-50 p-6 sm:p-8">
                <h2 className="text-2xl font-bold text-gray-900">{t(categoryT, `seo_${catKey}_h2`, '')}</h2>
                <p className="mt-4 text-base leading-7 text-gray-700">{t(categoryT, `seo_${catKey}_p1`, '')}</p>
                <h3 className="mt-6 text-xl font-semibold text-gray-900">{t(categoryT, `seo_${catKey}_h3_1`, '')}</h3>
                <p className="mt-3 text-base leading-7 text-gray-700">{t(categoryT, `seo_${catKey}_p2`, '')}</p>
                <h3 className="mt-6 text-xl font-semibold text-gray-900">{t(categoryT, `seo_${catKey}_h3_2`, '')}</h3>
                <p className="mt-3 text-base leading-7 text-gray-700">{t(categoryT, `seo_${catKey}_p3`, '')}</p>
                {priceText && (
                  <p className="mt-4 text-base leading-7 text-gray-700">{priceText}</p>
                )}
                <div className="mt-6 flex flex-wrap items-center gap-2 text-sm text-gray-700">
                  <span>{t(categoryT, 'also_check', 'See also:')}</span>
                  {relatedLinks.map((link, index) => (
                    <span key={link.href}>
                      <Link href={link.href} className="font-medium text-orange-600 underline underline-offset-2">
                        {link.label}
                      </Link>
                      {index < relatedLinks.length - 1 ? <span className="ml-2 text-gray-400">•</span> : null}
                    </span>
                  ))}
                </div>
              </section>
              </section>
            </div>

            <div className="hidden lg:block w-full lg:w-80 xl:w-96 shrink-0">
              <div className="sticky top-6">
                <div id="lead-form" className="rounded-xl border border-orange-100 bg-white p-6 shadow-lg">
                  <LeadForm
                    translations={categoryT}
                    categorySlug={apiSlug}
                    citySlug={city}
                    lang={lang}
                    cityName={cityName}
                    services={services}
                    countryCode={cityCountryCode}
                    title={t(categoryT, 'form_btn', 'Get offers')}
                  />
                </div>
              </div>
            </div>
          </div>

          <section className="mt-12 rounded-xl bg-gray-50 border-t border-gray-200 px-6 py-8 text-center">
            <p className="text-sm text-gray-500">
              {t(categoryT, 'provider_cta_prefix', 'Do you offer')} {categoryName} {t(categoryT, 'provider_cta_suffix', `in ${cityName}?`)}
            </p>
            <Link href={`/${lang}`} className="mt-2 inline-block text-sm font-semibold text-orange-500 hover:text-orange-600 underline underline-offset-2">
              {t(categoryT, 'provider_cta_link', 'Join for free →')}
            </Link>
          </section>
        </main>
      </div>
    </>
  );
}
