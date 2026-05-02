import Link from 'next/link';
import Image from 'next/image';
import type { Metadata } from 'next';
import { getProviderBySlug, getProviders, getPriceRange, PriceRangeData, getCityBySlug, ServiceOut } from '@/lib/api';
import { generateHreflangAlternates, generateOrganizationJsonLd, generateWebSiteJsonLd, generateLocalBusinessJsonLd } from '@/lib/seo';
import { fetchTranslations } from '@/lib/ui-translations';
import { JsonLd } from '@/components/JsonLd';
import LeadForm from '@/components/category/LeadForm';
import CategoryPageClient from '@/components/category/CategoryPageClient';
import type { ProviderDetail } from '@/lib/api';

interface PageProps {
  params: Promise<{ lang: string; city: string; category: string }>;
}

type CategoryKey = 'cleaning' | 'massage' | 'plumbing';
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

interface ProviderService {
  id: string;
  title: string;
  priceType: string | null;
  basePrice: number | null;
  currency: string;
  description: string | null;
}

interface EnrichedProvider {
  id: string;
  slug: string;
  businessName: string;
  rating: number;
  profileImageUrl: string | null;
  description: string | null;
  jobsCompleted: number;
  leadsReceived: number;
  reviewCount: number;
  latestLeadPreviewCreatedAt: string | null;
  latestLeadPreviewClientName: string | null;
  services: ProviderService[];
}

interface ProviderCardTexts {
  defaultDescription: string;
  jobsCompleted: string;
  lastRequest: string;
  directContact: string;
  sendRequest: string;
  verifiedSpecialist: string;
  freeNoObligation: string;
  peopleSought: string;
  recentlyRequested: string;
  reviews: string;
  onRequest: string;
  moreServices: string;
}

function getApiSlug(category: string): ApiCategorySlug {
  return category as ApiCategorySlug;
}

function getCategoryTranslationKey(category: string): CategoryKey {
  return category as CategoryKey;
}

function isWithin90Days(dateStr: string | null): boolean {
  if (!dateStr) return false;
  const date = new Date(dateStr);
  const now = new Date();
  const diffDays = (now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24);
  return diffDays <= 90;
}

function getInitials(name: string): string {
  return name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part.charAt(0).toUpperCase())
    .join('');
}

function formatPrice(
  basePrice: number | null,
  priceType: string | null,
  currency: string,
  onRequestLabel: string
): string {
  if (!basePrice || priceType === 'request') return onRequestLabel;
  const price = `${basePrice} ${currency}`;
  if (priceType === 'hourly') return `${price}/ч`;
  if (priceType === 'per_sqm') return `${price}/м²`;
  return price;
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
  const hasLeads = provider.leadsReceived > 0;
  const hasJobs = provider.jobsCompleted > 0;
  const hasRating = provider.rating > 0;
  const hasRecentLead =
    isWithin90Days(provider.latestLeadPreviewCreatedAt) &&
    provider.latestLeadPreviewClientName !== null;

  const providerState: 1 | 2 | 3 | 4 =
    hasRating && hasJobs ? 4
    : hasJobs ? 3
    : hasLeads ? 2
    : 1;

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

          {provider.services.length > 0 && (() => {
            const hasAnyDescription = provider.services.some(s => s.description);
            return (
              <div className="mt-3 space-y-2">
                {provider.services.slice(0, 2).map((service) => (
                  <div key={service.id}>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-700 font-medium">{service.title}</span>
                      <span className="font-medium text-gray-900">
                        {formatPrice(service.basePrice, service.priceType, service.currency, texts.onRequest)}
                      </span>
                    </div>
                    {service.description && (
                      <p className="text-xs text-gray-500 line-clamp-1 mt-0.5">{service.description}</p>
                    )}
                  </div>
                ))}
                {!hasAnyDescription && (
                  <p className="text-xs text-gray-500">{texts.defaultDescription}</p>
                )}
                {provider.services.length > 2 && (
                  <div className="text-xs text-orange-600 font-medium">
                    {texts.moreServices.replace('{n}', String(provider.services.length - 2))}
                  </div>
                )}
              </div>
            );
          })()}

          {providerState === 1 && (
            <div className="mt-4 flex flex-wrap gap-2 text-xs font-medium text-gray-600">
              <span className="rounded-full bg-orange-50 px-3 py-1.5 text-orange-700">
                ✓ {texts.verifiedSpecialist} • {texts.freeNoObligation}
              </span>
              <span className="rounded-full bg-gray-50 px-3 py-1.5">
                ✓ {texts.directContact}
              </span>
            </div>
          )}

          {providerState === 2 && (
            <div className="mt-4 flex flex-wrap gap-2 text-xs font-medium text-gray-600">
              <span className="rounded-full bg-gray-50 px-3 py-1.5">
                ⚡ {provider.leadsReceived} {texts.peopleSought}
              </span>
              <span className="rounded-full bg-gray-50 px-3 py-1.5">
                ✓ {texts.directContact}
              </span>
            </div>
          )}

          {providerState === 3 && (
            <div className="mt-4 flex flex-wrap gap-2 text-xs font-medium text-gray-600">
              <span className="rounded-full bg-gray-50 px-3 py-1.5">
                ✅ {provider.jobsCompleted} {texts.jobsCompleted}
              </span>
              {hasRecentLead && (
                <span className="rounded-full bg-gray-50 px-3 py-1.5">
                  ⚡ {provider.latestLeadPreviewClientName} {texts.recentlyRequested}
                </span>
              )}
              <span className="rounded-full bg-gray-50 px-3 py-1.5">
                ✓ {texts.directContact}
              </span>
            </div>
          )}

          {providerState === 4 && (
            <div className="mt-4 flex flex-wrap gap-2 text-xs font-medium text-gray-600">
              <span className="rounded-full bg-amber-50 px-3 py-1.5 text-amber-700">
                ⭐ {provider.rating.toFixed(1)} • {provider.reviewCount} {texts.reviews}
              </span>
              <span className="rounded-full bg-gray-50 px-3 py-1.5">
                ✅ {provider.jobsCompleted} {texts.jobsCompleted}
              </span>
              {hasRecentLead && (
                <span className="rounded-full bg-gray-50 px-3 py-1.5">
                  ⚡ {provider.latestLeadPreviewClientName} {texts.recentlyRequested}
                </span>
              )}
              <span className="rounded-full bg-gray-50 px-3 py-1.5">
                ✓ {texts.directContact}
              </span>
            </div>
          )}

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

function getCategoryContent(
  category: string,
  cityName: string,
  categoryName: string,
  lang: string = 'en',
  citySlug: string = '',
): CategoryContent {
  const replace = (str: string) =>
    str
      .replace(/{city}/g, cityName)
      .replace(/{category}/g, categoryName)
      .replace(/{category_name}/g, categoryName)
      .replace(/{lang}/g, lang)
      .replace(/{city_slug}/g, citySlug);

  const defaultContent: CategoryContent = {
    apiSlug: category as ApiCategorySlug,
    displayName: category,
    heading: '{category} in {city}',
    subtitle: 'Find trusted {category_name} specialists in {city}. Free request, no obligation.',
    metadataTitle: '{category_name} in {city} | Nevumo',
    metadataDescription: 'Find trusted {category_name} specialists in {city}. Free request, no obligation. Reply in as little as 30 minutes.',
    seoTitle: '{category_name} in {city} — what is worth knowing?',
    seoParagraphs: [
      '{city} offers a wide selection of professional {category_name} specialists. Nevumo helps you find trusted professionals nearby.',
      'Check previous client reviews, specialist experience, and the scope of services offered. A good specialist will adapt the technique to your needs.',
      '',
    ],
    seoQuestions: [`How to choose a ${categoryName} specialist?`, ''],
    relatedLinks: [
      { href: '/{lang}/{city_slug}/cleaning', label: 'Cleaning in {city}' },
      { href: '/{lang}/{city_slug}/massage', label: 'Massage in {city}' },
      { href: '/{lang}/{city_slug}/plumbing', label: 'Plumbing in {city}' },
    ].filter(l => !l.href.includes(category)),
    faq: [
      {
        question: 'How to find a {category_name} specialist in {city}?',
        answer: 'On Nevumo you can send a free request to trusted {category_name} specialists in {city} and receive a response in as little as 30 minutes.',
      },
      {
        question: 'How much does {category_name} cost in {city}?',
        answer: 'The cost of {category_name} in {city} depends on the specific requirements. Send a request to get free quotes.',
      },
      {
        question: 'Is the request free?',
        answer: 'Yes, sending a request through Nevumo is completely free and without obligation.',
      },
    ],
  };

  return {
    ...defaultContent,
    heading: replace(defaultContent.heading),
    subtitle: replace(defaultContent.subtitle),
    metadataTitle: replace(defaultContent.metadataTitle),
    metadataDescription: replace(defaultContent.metadataDescription),
    seoTitle: replace(defaultContent.seoTitle),
    seoParagraphs: defaultContent.seoParagraphs.map(replace) as [string, string, string],
    seoQuestions: defaultContent.seoQuestions.map(replace) as [string, string],
    relatedLinks: defaultContent.relatedLinks.map((link) => ({
      href: replace(link.href),
      label: replace(link.label),
    })),
    faq: defaultContent.faq.map((f) => ({
      question: replace(f.question),
      answer: replace(f.answer),
    })),
  };
}

function formatRelativeTime(dateString: string, lang: string = 'en'): string {
  const diffMs = Date.now() - new Date(dateString).getTime();
  const diffSeconds = Math.round(diffMs / 1000);
  const diffMinutes = Math.round(diffSeconds / 60);
  const diffHours = Math.round(diffMinutes / 60);
  const diffDays = Math.round(diffHours / 24);

  try {
    const rtf = new Intl.RelativeTimeFormat(lang, { numeric: 'always' });
    
    if (diffMinutes < 60) {
      return rtf.format(-Math.max(1, diffMinutes), 'minute');
    }
    
    if (diffHours < 24) {
      return rtf.format(-diffHours, 'hour');
    }
    
    return rtf.format(-diffDays, 'day');
  } catch (e) {
    // Fallback if Intl is not supported or lang is invalid
    if (diffMinutes < 60) return `${diffMinutes}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${diffDays}d ago`;
  }
}

// Helper function to get price text based on price data and translations
function getPriceText(
  priceData: PriceRangeData | null,
  translations: Record<string, string>,
  key_prefix: 'price_text' | 'price_faq' | 'price_meta',
  fallback: string = '',
): string {
  const priceOnRequest = translations['price_on_request'] || 'Price on request';
  // If priceData is null or prices are missing/zero, return priceOnRequest as fallback
  if (priceData === null || !priceData.min || !priceData.max || priceData.min === 0 || priceData.max === 0) {
    return priceOnRequest;
  }

  if (priceData.min === priceData.max) {
    const template = (translations[`${key_prefix}_single`] || fallback);
    return template
      .replace(/{price}/g, String(priceData.min))
      .replace(/{min_price}/g, String(priceData.min))
      .replace(/{max_price}/g, String(priceData.max))
      .replace(/{currency}/g, priceData.currency);
  }

  const template = (translations[`${key_prefix}_range`] || fallback);
  return template
    .replace(/{min}/g, String(priceData.min))
    .replace(/{max}/g, String(priceData.max))
    .replace(/{min_price}/g, String(priceData.min))
    .replace(/{max_price}/g, String(priceData.max))
    .replace(/{currency}/g, priceData.currency);
}

function buildFaqJsonLd(
  faq: Array<{ question: string; answer: string }>,
): Record<string, unknown> {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faq.map((item) => ({
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
  const categoryName = (homepageT[catNameKey] || catKey).replace(/{city}/g, cityName);

  const title = `${categoryName} i ${cityName}`;
  const baseDescription = (categoryT[`subtitle_${catKey}`] || '').replace(/{city}/g, cityName);
  
  // Fetch price range for metadata
  const apiSlug = getApiSlug(category);
  const priceData = await getPriceRange(apiSlug, city);
  const priceMetaText = getPriceText(priceData, categoryT, 'price_meta', '');
  const description = priceMetaText ? `${baseDescription} ${priceMetaText}` : baseDescription;

  const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://nevumo.com';

  return {
    title,
    description,
    alternates: {
      canonical: `${SITE_URL}/${lang}/${city}/${category}`,
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
        leadsReceived: detail?.leads_received ?? 0,
        reviewCount: detail?.review_count ?? 0,
        latestLeadPreviewCreatedAt: detail?.latest_lead_preview?.created_at ?? null,
        latestLeadPreviewClientName: detail?.latest_lead_preview?.client_name ?? null,
        services: (detail?.services ?? [])
          .filter((s: ServiceOut) => s.category_slug === category)
          .map((s: ServiceOut) => ({
            id: s.id,
            title: s.title,
            priceType: s.price_type,
            basePrice: s.base_price,
            currency: s.currency ?? 'PLN',
            description: s.description ?? null,
          })),
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
  const categoryName = (homepageT[catNameKey] || catKey).replace(/{city}/g, cityName);

  const content = getCategoryContent(category, cityName, categoryName, lang, city);

  const heading = (categoryT[`h1_${catKey}`] || `${categoryName} in ${cityName}`).replace(/{city}/g, cityName);
  const subtitle = (categoryT[`subtitle_${catKey}`] || '').replace(/{city}/g, cityName);
  const providerCardTexts: ProviderCardTexts = {
    defaultDescription: (categoryT['provider_desc_fallback'] || 'Проверен специалист в {city}. Изпратете кратко запитване и изчакайте връзка.').replace(/{city}/g, cityName),
    jobsCompleted: (categoryT['provider_jobs_completed'] || 'completed jobs').replace(/{city}/g, cityName),
    lastRequest: (categoryT['provider_last_request'] || 'Last request').replace(/{city}/g, cityName),
    directContact: (categoryT['provider_direct_contact'] || 'Direct contact').replace(/{city}/g, cityName),
    sendRequest: (categoryT['form_btn'] || 'Send request').replace(/{city}/g, cityName),
    verifiedSpecialist: (categoryT['provider_verified_specialist'] || 'Verified specialist').replace(/{city}/g, cityName),
    freeNoObligation: (categoryT['provider_free_no_obligation'] || 'Free • No obligation').replace(/{city}/g, cityName),
    peopleSought: (categoryT['provider_people_sought'] || 'people sought this specialist').replace(/{city}/g, cityName),
    recentlyRequested: (categoryT['provider_recently_requested'] || 'recently made a request').replace(/{city}/g, cityName),
    reviews: (categoryT['provider_reviews'] || 'reviews').replace(/{city}/g, cityName),
    onRequest: (categoryT['provider_on_request'] || categoryT['price_on_request'] || 'Price on request').replace(/{city}/g, cityName),
    moreServices: (categoryT['provider_more_services'] || 'и още {n} услуги').replace(/{city}/g, cityName),
  };

  const relatedLinksByCategory: Record<CategoryKey, Array<{ href: string; label: string }>> = {
    massage: [
      { href: `/${lang}/${city}/cleaning`, label: (categoryT['h1_cleaning'] || `Cleaning in ${cityName}`).replace(/{city}/g, cityName) },
      { href: `/${lang}/${city}/plumbing`, label: (categoryT['h1_plumbing'] || `Plumbing in ${cityName}`).replace(/{city}/g, cityName) },
    ],
    cleaning: [
      { href: `/${lang}/${city}/massage`, label: (categoryT['h1_massage'] || `Massage in ${cityName}`).replace(/{city}/g, cityName) },
      { href: `/${lang}/${city}/plumbing`, label: (categoryT['h1_plumbing'] || `Plumbing in ${cityName}`).replace(/{city}/g, cityName) },
    ],
    plumbing: [
      { href: `/${lang}/${city}/massage`, label: (categoryT['h1_massage'] || `Massage in ${cityName}`).replace(/{city}/g, cityName) },
      { href: `/${lang}/${city}/cleaning`, label: (categoryT['h1_cleaning'] || `Cleaning in ${cityName}`).replace(/{city}/g, cityName) },
    ],
  };
  const relatedLinks = relatedLinksByCategory[(category as CategoryKey)] ?? relatedLinksByCategory.cleaning;

  const { providers, allCount, averageRating } = await getEnrichedProviders(lang, city, apiSlug);
  const priceData = await getPriceRange(apiSlug, city);
  const priceText = getPriceText(priceData, categoryT, 'price_text', '');
  
  const cityCountryCode = cityData?.country_code || 'PL';
  const isAfterEuroAdoption = new Date() >= new Date('2026-01-01');
  const cityCurrency = cityData?.currency || (
    cityCountryCode === 'PL' ? 'PLN' : 
    (cityCountryCode === 'BG' && isAfterEuroAdoption ? '€' : 'BGN')
  );

  // FAQ items generation with dynamic translations and fallback
  const faqItems = [1, 2, 3].map(i => {
    const qKey = `faq_${catKey}_q${i}`;
    const aKey = `faq_${catKey}_a${i}`;
    
    let question = categoryT[qKey]?.replace(/{city}/g, cityName) || '';
    let answer = categoryT[aKey]?.replace(/{city}/g, cityName) || '';

    // Fallback to dynamic content if DB translation is missing
    if (!question || !answer) {
      const fallbackFaq = content.faq[i - 1];
      if (fallbackFaq) {
        question = question || fallbackFaq.question;
        answer = answer || fallbackFaq.answer;
      }
    }

    if (!question) return null;

    const priceOnRequest = categoryT['price_on_request'] || 'Price on request';
    const hasValidPrice = priceData && priceData.min && priceData.max && priceData.min > 0 && priceData.max > 0;

    const replaceFaq = (str: string) => {
      let result = str
        .replace(/{city}/g, cityName)
        .replace(/{category}/g, categoryName)
        .replace(/{category_name}/g, categoryName);

      if (hasValidPrice) {
        result = result
          .replace(/{min_price}/g, String(priceData.min))
          .replace(/{max_price}/g, String(priceData.max))
          .replace(/{price_range}/g, `${priceData.min} - ${priceData.max} ${priceData.currency || cityCurrency}`)
          .replace(/{currency}/g, priceData.currency || cityCurrency);
      } else {
        // When no valid prices, identify and replace the entire price phrase containing placeholders
        // We look for a phrase that contains any of our price placeholders
        const pricePhrasePattern = /[^.!?]*({min_price}|{max_price}|{currency}|{price_range})[^.!?]*[.!?]?/gi;
        result = result.replace(pricePhrasePattern, ` ${priceOnRequest}. `);

        // Categorical cleanup: Ensure NO placeholders remain in the entire text
        result = result
          .replace(/{min_price}/g, '')
          .replace(/{max_price}/g, '')
          .replace(/{currency}/g, '')
          .replace(/{price_range}/g, '');

        // Clean up any double spaces or messy punctuation resulting from the replacement
        result = result.replace(/\s+/g, ' ').replace(/\s+([.!?])/g, '$1').trim();
      }

      return result;
    };

    let finalAnswer = replaceFaq(answer);
    
    // Fallback for price-related questions if answer is still empty
    if (!finalAnswer && priceData !== null) {
      const priceQuestionKeywords = ['kosztu', 'price', 'cost', 'cena', 'ceny'];
      const isPriceQuestion = priceQuestionKeywords.some(keyword =>
        question.toLowerCase().includes(keyword.toLowerCase()),
      );
      if (isPriceQuestion) {
        finalAnswer = getPriceText(priceData, categoryT, 'price_faq', '');
      }
    }

    if (!finalAnswer && providers.length === 0) {
      finalAnswer = categoryT['price_on_request'] || 'Price on request';
    }

    return {
      question: replaceFaq(question),
      answer: finalAnswer,
    };
  }).filter((item): item is { question: string; answer: string } => item !== null && item.question !== '');

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
  
  const visibleProviders = providers.slice(0, 20);
  const hiddenProviders = providers.slice(20);
  const hiddenCount = hiddenProviders.length;
  const trustSpecialistsText = `${allCount > 0 ? allCount : 14} ${(categoryT['trust_specialists'] || 'specialists').replace(/{city}/g, cityName)}`;
  const trustRatingText = `${averageRating.toFixed(1)} ${(categoryT['trust_rating'] || 'rating').replace(/{city}/g, cityName)}`;
  const trustLeadsText = `120 ${(categoryT['trust_requests'] || 'requests this month').replace(/{city}/g, cityName)}`;
  const faqJsonLd = buildFaqJsonLd(faqItems);

  const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://nevumo.com';
  const organizationJsonLd = generateOrganizationJsonLd();
  const websiteJsonLd = generateWebSiteJsonLd(lang);

  // Create a pseudo-provider for the category in this city for LocalBusiness schema
  const categoryPseudoProvider: ProviderDetail = {
    id: `cat-${city}-${category}`,
    business_name: heading,
    description: subtitle,
    slug: `${city}/${category}`,
    profile_image_url: null,
    rating: averageRating || 4.8,
    verified: true,
    services: [
      {
        id: `service-${category}`,
        title: categoryName,
        description: subtitle,
        price_type: 'request',
        base_price: priceData?.min || null,
        category_slug: category,
        currency: priceData?.currency || cityCurrency
      }
    ],
    jobs_completed: allCount * 10,
    review_count: providers.reduce((acc, p) => acc + p.reviewCount, 0),
    leads_received: allCount * 5,
    city_leads: allCount * 5,
    translations: {},
    is_claimed: true
  };

  const localBusinessJsonLd = generateLocalBusinessJsonLd(categoryPseudoProvider, categoryName, cityName, cityCountryCode);

  const breadcrumbJsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
        item: `${SITE_URL}/${lang}`,
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: cityName,
        item: `${SITE_URL}/${lang}/${city}`,
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: categoryName,
        item: `${SITE_URL}/${lang}/${city}/${category}`,
      },
    ],
  };

  return (
    <>
      <JsonLd data={faqJsonLd} />
      <JsonLd data={organizationJsonLd} />
      <JsonLd data={websiteJsonLd} />
      <JsonLd data={localBusinessJsonLd} />
      <JsonLd data={breadcrumbJsonLd} />
      <div className="min-h-screen bg-white text-gray-900">
        <header className="border-b border-orange-100 bg-white/90 backdrop-blur">
          <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8 gap-y-2">
            <Link href={`/${lang}`} className="inline-flex items-center">
              <Image src="/Nevumo_logo.svg" alt="Nevumo" width={120} height={36} priority />
            </Link>
            <Link href={`/${lang}`} className="text-sm font-semibold text-gray-700 transition hover:text-orange-600">
              {categoryT['nav_link']?.replace(/{city}/g, cityName) || 'Become a specialist'}
            </Link>
          </div>
        </header>
        <main className="mx-auto w-full max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          <section className="space-y-4">
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
                {(categoryT['trust_response'] || 'Avg. response: ~30 min').replace(/{city}/g, cityName)}
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
                      {(categoryT['no_providers_title'] || 'Be the first to request this service in your area').replace(/{city}/g, cityName)}
                    </p>
                    <p className="text-sm text-gray-500 mt-0.5">
                      {(categoryT['no_providers_subtitle'] || 'Providers joining Nevumo will see your request and contact you').replace(/{city}/g, cityName)}
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
                        {(categoryT['show_more'] || 'Show more').replace(/{city}/g, cityName)}
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
                stickyButtonLabel={(categoryT['sticky_btn'] || 'Get offers — Free').replace(/{city}/g, cityName)}
              />

              <section className="mt-8 rounded-xl bg-gray-50 p-6 sm:p-8">
                <h2 className="text-2xl font-bold text-gray-900">{categoryT[`seo_${catKey}_h2`]?.replace(/{city}/g, cityName) || ''}</h2>
                <p className="mt-4 text-base leading-7 text-gray-700">{categoryT[`seo_${catKey}_p1`]?.replace(/{city}/g, cityName) || ''}</p>
                <h3 className="mt-6 text-xl font-semibold text-gray-900">{categoryT[`seo_${catKey}_h3_1`]?.replace(/{city}/g, cityName) || ''}</h3>
                <p className="mt-3 text-base leading-7 text-gray-700">{categoryT[`seo_${catKey}_p2`]?.replace(/{city}/g, cityName) || ''}</p>
                <h3 className="mt-6 text-xl font-semibold text-gray-900">{categoryT[`seo_${catKey}_h3_2`]?.replace(/{city}/g, cityName) || ''}</h3>
                <p className="mt-3 text-base leading-7 text-gray-700">{categoryT[`seo_${catKey}_p3`]?.replace(/{city}/g, cityName) || ''}</p>
                {priceText && (
                  <p className="mt-4 text-base leading-7 text-gray-700">{priceText}</p>
                )}

                {faqItems.length > 0 && (
                  <div className="mt-10 border-t border-gray-100 pt-10">
                    <h2 className="text-2xl font-bold text-gray-900 mb-6">
                      {(categoryT['faq_title'] || homepageT['faq_title'] || 'Frequently Asked Questions').replace(/{city}/g, cityName)}
                    </h2>
                    <div className="space-y-6 text-left">
                      {faqItems.map((item, index) => (
                        <div key={index} className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
                          <h3 className="text-lg font-bold text-gray-900 mb-2">{item.question}</h3>
                          <p className="text-gray-700 leading-relaxed">{item.answer}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="mt-6 flex flex-wrap items-center gap-2 text-sm text-gray-700">
                  <span>{(categoryT['also_check'] || 'See also:').replace(/{city}/g, cityName)}</span>
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
                    title={(categoryT['form_btn'] || 'Get offers').replace(/{city}/g, cityName)}
                  />
                </div>
              </div>
            </div>
          </div>

          <section className="mt-12 rounded-xl bg-gray-50 border-t border-gray-200 px-6 py-8 text-center">
            <p className="text-sm text-gray-500">
              {(categoryT['provider_cta_prefix'] || 'Do you offer').replace(/{city}/g, cityName)} {categoryName} {(categoryT['provider_cta_suffix'] || `in ${cityName}?`).replace(/{city}/g, cityName)}
            </p>
            <Link href={`/${lang}`} className="mt-2 inline-block text-sm font-semibold text-orange-500 hover:text-orange-600 underline underline-offset-2">
              {(categoryT['provider_cta_link'] || 'Join for free →').replace(/{city}/g, cityName)}
            </Link>
          </section>
        </main>
      </div>
    </>
  );
}
