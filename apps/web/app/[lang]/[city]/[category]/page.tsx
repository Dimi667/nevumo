import Link from 'next/link';
import Image from 'next/image';
import type { Metadata } from 'next';
import { getProviderBySlug, getProviders, getPriceRange, PriceRangeData, getCityBySlug, ServiceOut, getCategories } from '@/lib/api';
import { generateHreflangAlternates, generateOrganizationJsonLd, generateWebSiteJsonLd, generateLocalBusinessJsonLd } from '@/lib/seo';
import { fetchTranslations, t } from '@/lib/ui-translations';
import { getLocalizedCityText } from '@/lib/cityHelpers';
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
  category_slug: string | null;
}

interface EnrichedProvider {
  id: string;
  slug: string;
  businessName: string;
  rating: number;
  verificationLevel: number;
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
  const cityT = await fetchTranslations(lang, 'city');
  const cityData = await getCityBySlug(city, lang);
  const cityName = cityData?.city || city.charAt(0).toUpperCase() + city.slice(1);
  // Slavic languages that use grammatical cases (locative/genitive)
  const slavicLanguagesWithDeclension = ['bg', 'cs', 'sk', 'ru', 'uk', 'sr', 'hr', 'mk', 'sl', 'pl'];
  const grammaticalCase = slavicLanguagesWithDeclension.includes(lang) ? 'locative' : 'nominative';
  const catKey = getCategoryTranslationKey(category);
  const catNameKey = `cat_${catKey}_name` as const;
  const categoryName = getLocalizedCityText((homepageT[catNameKey] || catKey), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form });

  const prepBase = categoryT['preposition_base'] || 'in';
  const title = getLocalizedCityText(`${categoryName} ${prepBase} {city}`, lang, cityName, categoryT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form });
  const baseDescription = getLocalizedCityText((categoryT[`subtitle_${catKey}`] || ''), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form });
  
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

  const details = listItems.map((provider) => ({
    id: provider.id,
    slug: provider.slug,
    businessName: provider.business_name,
    rating: provider.rating,
    verificationLevel: provider.verification_level ?? 0,
    profileImageUrl: provider.profile_image_url ?? null,
    description: provider.description ?? null,
    jobsCompleted: provider.jobs_completed ?? 0,
    leadsReceived: provider.leads_received ?? 0,
    reviewCount: provider.review_count ?? 0,
    latestLeadPreviewCreatedAt: provider.latest_lead_preview?.created_at ?? null,
    latestLeadPreviewClientName: provider.latest_lead_preview?.client_name ?? null,
    services: (provider.services ?? [])
      .filter((s: ServiceOut) => s.category_slug === category)
      .map((s: ServiceOut) => ({
        id: s.id,
        title: s.title,
        priceType: s.price_type,
        basePrice: s.base_price,
        currency: s.currency ?? 'PLN',
        description: s.description ?? null,
        category_slug: s.category_slug,
      })),
  })) satisfies EnrichedProvider[];

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
  const cityT = await fetchTranslations(lang, 'city');
  const cookieT = await fetchTranslations(lang, 'cookie_banner');
  const widgetT = await fetchTranslations(lang, 'widget');
  const apiSlug = getApiSlug(category);
  const catKey = getCategoryTranslationKey(category);

  const cityData = await getCityBySlug(city, lang);
  const cityName = cityData?.city || city.charAt(0).toUpperCase() + city.slice(1);
  // Slavic languages that use grammatical cases (locative/genitive)
  const slavicLanguagesWithDeclension = ['bg', 'cs', 'sk', 'ru', 'uk', 'sr', 'hr', 'mk', 'sl', 'pl'];
  const grammaticalCase = slavicLanguagesWithDeclension.includes(lang) ? 'locative' : 'nominative';
  const useDirectCityName = slavicLanguagesWithDeclension.includes(lang);

  const catNameKey = `cat_${catKey}_name` as const;
  const categoryName = getLocalizedCityText((homepageT[catNameKey] || catKey), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form });

  const content = getCategoryContent(category, cityName, categoryName, lang, city);

  const prepBaseCat = categoryT['preposition_base'] || 'in';
  const heading = getLocalizedCityText((categoryT[`h1_${catKey}`] || `${categoryName} ${prepBaseCat} {city}`), lang, cityName, categoryT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form });
  const subtitle = getLocalizedCityText((categoryT[`subtitle_${catKey}`] || ''), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form });
  const providerCardTexts: ProviderCardTexts = {
    defaultDescription: getLocalizedCityText((categoryT['provider_desc_fallback'] || 'Проверен специалист в {city}. Изпратете кратко запитване и изчакайте връзка.'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }),
    jobsCompleted: getLocalizedCityText((categoryT['provider_jobs_completed'] || 'completed jobs'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }),
    lastRequest: getLocalizedCityText((categoryT['provider_last_request'] || 'Last request'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }),
    directContact: getLocalizedCityText((categoryT['provider_direct_contact'] || 'Direct contact'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }),
    sendRequest: getLocalizedCityText((categoryT['send_request_to_provider'] || 'Send request to'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }),
    verifiedSpecialist: getLocalizedCityText((categoryT['provider_verified_specialist'] || 'Verified specialist'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }),
    freeNoObligation: getLocalizedCityText((categoryT['provider_free_no_obligation'] || 'Free • No obligation'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }),
    peopleSought: getLocalizedCityText((categoryT['provider_people_sought'] || 'people sought this specialist'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }),
    recentlyRequested: getLocalizedCityText((categoryT['provider_recently_requested'] || 'recently made a request'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }),
    reviews: getLocalizedCityText((categoryT['provider_reviews'] || 'reviews'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }),
    onRequest: getLocalizedCityText((categoryT['provider_on_request'] || categoryT['price_on_request'] || 'Price on request'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }),
    moreServices: getLocalizedCityText((categoryT['provider_more_services'] || 'и още {n} услуги'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }),
  };

  const allCategories = await getCategories(lang);
  const relatedLinks = allCategories
    .filter((cat) => cat.slug !== category)
    .map((cat) => ({
      href: `/${lang}/${city}/${cat.slug}`,
      label: getLocalizedCityText(
        `${cat.name} ${prepBaseCat} {city}`,
        lang,
        cityName,
        categoryT,
        grammaticalCase,
        { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }
      ),
    }));

  const { providers, allCount, averageRating } = await getEnrichedProviders(lang, city, apiSlug);
  const priceData = await getPriceRange(apiSlug, city);
  const priceText = getPriceText(priceData, categoryT, 'price_text', '');
  
  const cityCountryCode = cityData?.country_code || 'PL';
  const isAfterEuroAdoption = new Date() >= new Date('2026-01-01');
  const cityCurrency = cityData?.currency || (
    cityCountryCode === 'PL' ? 'PLN' : 
    (cityCountryCode === 'BG' && isAfterEuroAdoption ? '€' : 'BGN')
  );

  // Helper function to replace {city} variable
  const replaceCity = (str: string) => {
    return str.replace(/{city}/g, cityName);
  };

  // FAQ items generation with dynamic translations and fallback
  const faqItems = [1, 2, 3].map(i => {
    const qKey = `faq_${catKey}_q${i}`;
    const aKey = `faq_${catKey}_a${i}`;
    
    let question = getLocalizedCityText((categoryT[qKey] || ''), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form });
    let answer = getLocalizedCityText((categoryT[aKey] || ''), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form });

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
      
      // Apply getLocalizedCityText for city placeholders after other replacements
      if (result.includes('{city}')) {
        result = getLocalizedCityText(result, lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form });
      }

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
        .flatMap(provider => 
          (provider.services || [])
            .filter(service => service.category_slug === apiSlug)
            .map(service => service.title)
        )
        .filter(title => title && title.length > 0 && title.length < 50)
    )
  ).map((title, index) => ({
    id: `service-${index}`,
    title
  })).slice(0, 8); // Limit to 8 services
  
  const visibleProviders = providers.slice(0, 20);
  const hiddenProviders = providers.slice(20);
  const hiddenCount = hiddenProviders.length;
  const trustSpecialistsText = `${allCount > 0 ? allCount : 14} ${getLocalizedCityText((categoryT['trust_specialists'] || 'specialists'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form })}`;
  const trustRatingText = `${averageRating.toFixed(1)} ${getLocalizedCityText((categoryT['trust_rating'] || 'rating'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form })}`;
  const trustLeadsText = `120 ${getLocalizedCityText((categoryT['trust_requests'] || 'requests this month'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form })}`;

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
    is_claimed: true,
    reviews: [],
    verification_level: 0,
    gallery: []
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
      <JsonLd data={organizationJsonLd} />
      <JsonLd data={websiteJsonLd} />
      <JsonLd data={localBusinessJsonLd} />
      <JsonLd data={breadcrumbJsonLd} />
      <div className="min-h-screen bg-white text-gray-900">
        <header className="border-b border-orange-100 bg-white/90 backdrop-blur">
          <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8 gap-y-2">
            <Link href={`/${lang}/auth?mode=register&role=provider&city=${city}&category=${category}`} className="text-sm font-semibold text-gray-700 transition hover:text-orange-600">
              <span className="flex flex-col items-end text-right text-sm font-semibold md:flex-row md:items-center md:gap-1">
                <span>{categoryT['nav_cta_line1'] || 'Do you offer'} {categoryName}?</span>
                <span>{categoryT['nav_cta_line2'] || 'Join for free!'} →</span>
              </span>
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
            <div className="mt-5 mb-6 inline-flex flex-wrap items-center gap-x-3 gap-y-2 rounded-full bg-gray-50 px-4 py-3 text-sm text-gray-700 max-w-full w-full">
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
                {getLocalizedCityText((categoryT['trust_response'] || 'Avg. response: ~30 min'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form })}
              </span>
            </div>
          </section>

          <div className="flex flex-col lg:flex-row gap-8">
            <div className="flex-1 min-w-0">
              {/* Mobile Lead Form and Sticky Button */}
              <CategoryPageClient
                translations={categoryT}
                categorySlug={apiSlug}
                citySlug={city}
                city={city}
                category={category}
                lang={lang}
                cityName={cityName}
                services={services}
                cityCountryCode={cityCountryCode}
                stickyButtonLabel={getLocalizedCityText((categoryT['sticky_btn'] || 'Get offers — Free'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form })}
                providers={providers}
                visibleProviders={visibleProviders}
                hiddenProviders={hiddenProviders}
                hiddenCount={hiddenCount}
                providerCardTexts={providerCardTexts}
                widgetT={widgetT}
                categoryT={categoryT}
                cityT={cityT}
                grammaticalCase={grammaticalCase}
                cityData={cityData ? {
  locative_form: cityData.locative_form ?? undefined,
  genitive_form: cityData.genitive_form ?? undefined,
} : undefined}
              />

              <section className="mt-8 rounded-xl bg-gray-50 p-6 sm:p-8">
                <h2 className="text-2xl font-bold text-gray-900">{replaceCity(getLocalizedCityText((categoryT[`seo_${catKey}_h2`] || ''), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }))}</h2>
                <p className="mt-4 text-base leading-7 text-gray-700">{replaceCity(useDirectCityName ? (categoryT[`seo_${catKey}_p1`] || '').replace('{city}', cityName) : getLocalizedCityText((categoryT[`seo_${catKey}_p1`] || ''), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }))}</p>
                <h3 className="mt-6 text-xl font-semibold text-gray-900">{replaceCity(getLocalizedCityText((categoryT[`seo_${catKey}_h3_1`] || ''), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }))}</h3>
                <p className="mt-3 text-base leading-7 text-gray-700">{replaceCity(getLocalizedCityText((categoryT[`seo_${catKey}_p2`] || ''), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }))}</p>
                <h3 className="mt-6 text-xl font-semibold text-gray-900">{replaceCity(getLocalizedCityText((categoryT[`seo_${catKey}_h3_2`] || ''), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }))}</h3>
                <p className="mt-3 text-base leading-7 text-gray-700">{replaceCity(getLocalizedCityText((categoryT[`seo_${catKey}_p3`] || ''), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form }))}</p>
                {priceText && (
                  <p className="mt-4 text-base leading-7 text-gray-700">{priceText}</p>
                )}

                <div className="mt-6 flex flex-wrap items-center gap-2 text-sm text-gray-700">
                  <span>{getLocalizedCityText((categoryT['also_check'] || 'See also:'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form })}</span>
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

            <div className="hidden lg:block w-full lg:w-80 xl:w-96 shrink-0">
              <div className="sticky top-6 max-h-[calc(100vh-48px)] flex flex-col overflow-hidden">
                <div id="lead-form" className="rounded-xl border border-orange-100 bg-white shadow-lg flex flex-col min-h-0 overflow-hidden">
                  <LeadForm
                    translations={categoryT}
                    categorySlug={apiSlug}
                    citySlug={city}
                    lang={lang}
                    cityName={cityName}
                    services={services}
                    countryCode={cityCountryCode}
                    title={getLocalizedCityText((categoryT['form_btn'] || 'Get offers'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form })}
                  />
                </div>
              </div>
            </div>
          </div>

          <section className="mt-12 rounded-xl bg-gray-50 border-t border-gray-200 px-6 py-8 text-center">
            <p className="text-sm text-gray-500">
              {getLocalizedCityText((categoryT['provider_cta_prefix'] || 'Do you offer'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form })} {categoryName} {getLocalizedCityText((categoryT['provider_cta_suffix'] || `${prepBaseCat} {city}?`), lang, cityName, categoryT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form })}
            </p>
            <Link href={`/${lang}/auth?mode=register&role=provider&city=${city}&category=${category}`} className="mt-2 inline-block text-sm font-semibold text-orange-500 hover:text-orange-600 underline underline-offset-2">
              {getLocalizedCityText((categoryT['provider_cta_link'] || 'Join for free →'), lang, cityName, cityT, grammaticalCase, { locative_form: cityData?.locative_form, genitive_form: cityData?.genitive_form })}
            </Link>
          </section>
        </main>
      </div>
    </>
  );
}
