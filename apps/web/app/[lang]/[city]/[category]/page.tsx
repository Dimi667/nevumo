import Link from 'next/link';
import Image from 'next/image';
import type { Metadata } from 'next';
import { getProviderBySlug, getProviders } from '@/lib/api';
import { generateHreflangAlternates } from '@/lib/seo';
import { fetchTranslations, t } from '@/lib/ui-translations';
import { JsonLd } from '@/components/JsonLd';
import LeadForm from '@/components/category/LeadForm';

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

          <a
            href="#lead-form"
            className="mt-5 inline-flex w-full items-center justify-center rounded-xl bg-orange-500 px-4 py-3 text-sm font-semibold text-white transition hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-offset-2"
          >
            {texts.sendRequest}
          </a>
        </div>
      </div>
    </article>
  );
}

const CATEGORY_CONTENT: Record<CategoryKey, CategoryContent> = {
  masaz: {
    apiSlug: 'massage',
    displayName: 'massage',
    heading: 'Massage in Warsaw',
    subtitle:
      'Find trusted massage specialists in Warsaw. Free request, no obligation.',
    metadataTitle: 'Massage in Warsaw | Nevumo',
    metadataDescription:
      'Find trusted massage specialists in Warsaw. Free request, no obligation. Reply in as little as 30 minutes.',
    seoTitle: 'Massage in Warsaw — what is worth knowing?',
    seoParagraphs: [
      'Warsaw offers a wide selection of professional massage specialists. Whether you are looking for relaxing, sports, or therapeutic massage, Nevumo helps you find trusted professionals nearby.',
      'Check previous client reviews, specialist experience, and the scope of services offered. A good massage specialist will adapt the technique to your needs.',
      'Massage prices in Warsaw start from around 100 PLN per hour. The final cost depends on the type of massage, the specialist’s experience, and location.',
    ],
    seoQuestions: ['How to choose a massage specialist?', 'How much does massage cost in Warsaw?'],
    relatedLinks: [
      { href: '/pl/warszawa/sprzatanie', label: 'Cleaning in Warsaw' },
      { href: '/pl/warszawa/hydraulik', label: 'Plumbing in Warsaw' },
    ],
    faq: [
      {
        question: 'How to find a massage specialist in Warsaw?',
        answer:
          'On Nevumo you can send a free request to trusted massage specialists in Warsaw and receive a response in as little as 30 minutes.',
      },
      {
        question: 'How much does massage cost in Warsaw?',
        answer:
          'Massage prices in Warsaw start from around 100 PLN per hour, depending on the type of massage and specialist experience.',
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
    heading: 'Cleaning in Warsaw',
    subtitle:
      'Find trusted cleaning specialists in Warsaw. Free request, no obligation.',
    metadataTitle: 'Cleaning in Warsaw | Nevumo',
    metadataDescription:
      'Find trusted cleaning companies in Warsaw. Free request, no obligation.',
    seoTitle: 'Cleaning in Warsaw — what is worth knowing?',
    seoParagraphs: [
      'Professional cleaning companies in Warsaw offer comprehensive services for homes, apartments, and offices. On Nevumo you can find trusted specialists available across the city.',
      'Pay attention to customer reviews, scope of services, and scheduling flexibility. The best companies often offer recurring service discounts.',
      'Standard apartment cleaning in Warsaw usually costs from 150 to 300 PLN, depending on size and scope of work.',
    ],
    seoQuestions: ['How to choose a cleaning company?', 'How much does cleaning cost in Warsaw?'],
    relatedLinks: [
      { href: '/pl/warszawa/masaz', label: 'Massage in Warsaw' },
      { href: '/pl/warszawa/hydraulik', label: 'Plumbing in Warsaw' },
    ],
    faq: [
      {
        question: 'How to find a cleaning company in Warsaw?',
        answer:
          'On Nevumo you can send a free request to trusted cleaning companies in Warsaw and quickly receive responses from available specialists.',
      },
      {
        question: 'How much does cleaning cost in Warsaw?',
        answer:
          'Standard apartment cleaning in Warsaw usually costs from 150 to 300 PLN, depending on size and scope of services.',
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
    heading: 'Plumbing in Warsaw',
    subtitle:
      'Find a trusted plumber in Warsaw. Free request, no obligation.',
    metadataTitle: 'Plumbing in Warsaw | Nevumo',
    metadataDescription:
      'Find a trusted plumber in Warsaw. Fast response, free request.',
    seoTitle: 'Plumbing in Warsaw — what is worth knowing?',
    seoParagraphs: [
      'Plumbing issues require a fast response. On Nevumo you can find trusted plumbers in Warsaw, including urgent availability. Free request, quick response.',
      'You usually call a plumber for water system failures, leaking taps, blocked drains, or bathroom and kitchen renovation work.',
      'Plumber rates in Warsaw usually start from 100 to 150 PLN per hour. The final price depends on the type of issue and response time.',
    ],
    seoQuestions: ['When should you call a plumber?', 'How much does a plumber cost in Warsaw?'],
    relatedLinks: [
      { href: '/pl/warszawa/masaz', label: 'Massage in Warsaw' },
      { href: '/pl/warszawa/sprzatanie', label: 'Cleaning in Warsaw' },
    ],
    faq: [
      {
        question: 'How to find a plumber in Warsaw?',
        answer:
          'On Nevumo you can send a free request to trusted plumbers in Warsaw and receive a response quickly.',
      },
      {
        question: 'How much does a plumber cost in Warsaw?',
        answer:
          'Plumber rates in Warsaw usually start from 100 to 150 PLN per hour, depending on the type of issue and response time.',
      },
      {
        question: 'Is the request free?',
        answer:
          'Yes, sending a request through Nevumo is completely free and without obligation.',
      },
    ],
  },
};

function getCategoryContent(category: string): CategoryContent {
  return CATEGORY_CONTENT[(category as CategoryKey)] ?? CATEGORY_CONTENT.masaz;
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

function buildFaqJsonLd(content: CategoryContent): Record<string, unknown> {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: content.faq.map((item) => ({
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
  const catKey = getCategoryTranslationKey(category);
  const title = `${t(categoryT, `h1_${catKey}`, 'Services in Warsaw')} | Nevumo`;
  const description = t(categoryT, `subtitle_${catKey}`, '');

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
  const content = getCategoryContent(category);
  const categoryT = await fetchTranslations(lang, 'category');
  const homepageT = await fetchTranslations(lang, 'homepage');
  const apiSlug = getApiSlug(category);
  const catKey = getCategoryTranslationKey(category);
  const heading = t(categoryT, `h1_${catKey}`, 'Services in Warsaw');
  const subtitle = t(categoryT, `subtitle_${catKey}`, '');
  const catNameKey = `cat_${catKey}_name` as const;
  const categoryName = t(homepageT, catNameKey, catKey);
  const providerCardTexts: ProviderCardTexts = {
    defaultDescription: t(categoryT, 'provider_desc_fallback', 'Trusted specialist available in Warsaw. Send a short request and wait for contact.'),
    jobsCompleted: t(categoryT, 'provider_jobs_completed', 'completed jobs'),
    lastRequest: t(categoryT, 'provider_last_request', 'Last request'),
    directContact: t(categoryT, 'provider_direct_contact', 'Direct contact'),
    sendRequest: t(categoryT, 'form_btn', 'Send request'),
  };

  const relatedLinksByCategory: Record<CategoryKey, Array<{ href: string; label: string }>> = {
    masaz: [
      { href: `/${lang}/${city}/sprzatanie`, label: t(categoryT, 'h1_cleaning', 'Cleaning in Warsaw') },
      { href: `/${lang}/${city}/hydraulik`, label: t(categoryT, 'h1_plumbing', 'Plumbing in Warsaw') },
    ],
    sprzatanie: [
      { href: `/${lang}/${city}/masaz`, label: t(categoryT, 'h1_massage', 'Massage in Warsaw') },
      { href: `/${lang}/${city}/hydraulik`, label: t(categoryT, 'h1_plumbing', 'Plumbing in Warsaw') },
    ],
    hydraulik: [
      { href: `/${lang}/${city}/masaz`, label: t(categoryT, 'h1_massage', 'Massage in Warsaw') },
      { href: `/${lang}/${city}/sprzatanie`, label: t(categoryT, 'h1_cleaning', 'Cleaning in Warsaw') },
    ],
  };
  const relatedLinks = relatedLinksByCategory[(category as CategoryKey)] ?? relatedLinksByCategory.sprzatanie;

  const { providers, allCount, averageRating } = await getEnrichedProviders(lang, city, apiSlug);
  const visibleProviders = providers.slice(0, 20);
  const hiddenProviders = providers.slice(20);
  const hiddenCount = hiddenProviders.length;
  const trustSpecialistsText = `${allCount > 0 ? allCount : 14} ${t(categoryT, 'trust_specialists', 'specialists')}`;
  const trustRatingText = `${averageRating.toFixed(1)} ${t(categoryT, 'trust_rating', 'rating')}`;
  const trustLeadsText = `120 ${t(categoryT, 'trust_requests', 'requests this month')}`;
  const faqJsonLd = buildFaqJsonLd(content);

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

        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 lg:py-12">
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

          <section className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_20rem] lg:items-start">
            <div className="space-y-4">
              {providers.length === 0 ? (
                <div className="rounded-xl border border-gray-100 bg-white px-6 py-12 text-center shadow-sm">
                  <p className="text-base font-medium text-gray-700">
                    {t(categoryT, 'empty_state', 'First specialists are joining.')}
                  </p>
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
              <section className="mt-8 rounded-xl bg-gray-50 p-6 sm:p-8">
                <h2 className="text-2xl font-bold text-gray-900">{t(categoryT, `seo_${catKey}_h2`, '')}</h2>
                <p className="mt-4 text-base leading-7 text-gray-700">{t(categoryT, `seo_${catKey}_p1`, '')}</p>
                <h3 className="mt-6 text-xl font-semibold text-gray-900">{t(categoryT, `seo_${catKey}_h3_1`, '')}</h3>
                <p className="mt-3 text-base leading-7 text-gray-700">{t(categoryT, `seo_${catKey}_p2`, '')}</p>
                <h3 className="mt-6 text-xl font-semibold text-gray-900">{t(categoryT, `seo_${catKey}_h3_2`, '')}</h3>
                <p className="mt-3 text-base leading-7 text-gray-700">{t(categoryT, `seo_${catKey}_p3`, '')}</p>
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
            </div>

            <aside className="lg:sticky lg:top-6">
              <div id="lead-form" className="rounded-xl border border-orange-100 bg-white p-6 shadow-lg">
                <LeadForm
                  categorySlug={apiSlug}
                  citySlug={city}
                  title={t(categoryT, 'form_title', 'Send a request')}
                  subtitle={t(categoryT, 'form_subtitle', 'Free • No obligation')}
                  phonePlaceholder={t(categoryT, 'form_phone', 'Your phone number')}
                  descPlaceholder={t(categoryT, 'form_desc', 'Describe what you need (optional)')}
                  buttonText={t(categoryT, 'form_btn', 'Send request')}
                  trustItems={[
                    t(categoryT, 'form_trust_1', 'Free'),
                    t(categoryT, 'form_trust_2', 'No obligation'),
                    t(categoryT, 'form_trust_3', 'Reply within 30 min'),
                  ]}
                />
              </div>
            </aside>
          </section>

          <section className="mt-12 rounded-xl bg-gray-50 border-t border-gray-200 px-6 py-8 text-center">
            <p className="text-sm text-gray-500">
              {t(categoryT, 'provider_cta_prefix', 'Do you offer')} {categoryName} {t(categoryT, 'provider_cta_suffix', 'in Warsaw?')}
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
