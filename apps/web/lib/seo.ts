import type { ProviderDetail, ProviderListItem } from '@/lib/api';
import { SUPPORTED_LANGUAGES } from '@/lib/locales';
import { getCurrency } from '@/lib/currency';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://nevumo.com';

/**
 * Generates hreflang alternate URLs for all supported languages.
 * @param path - The path after the language prefix, e.g. "/sofia/massage" or "/"
 */
export function generateHreflangAlternates(path: string): Record<string, string> {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return Object.fromEntries(
    SUPPORTED_LANGUAGES.map((lang) => [
      lang,
      `${SITE_URL}/${lang}${normalizedPath === '/' ? '' : normalizedPath}`,
    ]),
  );
}

/**
 * Generates JSON-LD LocalBusiness schema for a provider detail page.
 */
export function generateLocalBusinessJsonLd(
  provider: ProviderDetail,
  category: string,
  city: string,
  countryCode?: string,
): Record<string, unknown> {
  const currency = getCurrency(countryCode);
  return {
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    name: provider.business_name,
    description: provider.description ?? undefined,
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: provider.rating,
      bestRating: 5,
    },
    address: {
      '@type': 'PostalAddress',
      addressLocality: city,
    },
    makesOffer: provider.services.map((s) => ({
      '@type': 'Offer',
      itemOffered: {
        '@type': 'Service',
        name: s.title,
        description: s.description ?? undefined,
      },
      price: s.base_price ?? undefined,
      priceCurrency: currency,
    })),
  };
}

/**
 * Generates JSON-LD ItemList schema for a category listing page.
 */
export function generateServiceListJsonLd(
  providers: ProviderListItem[],
  category: string,
  city: string,
): Record<string, unknown> {
  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: `${category} in ${city}`,
    numberOfItems: providers.length,
    itemListElement: providers.map((p, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      item: {
        '@type': 'LocalBusiness',
        name: p.business_name,
        aggregateRating: {
          '@type': 'AggregateRating',
          ratingValue: p.rating,
          bestRating: 5,
        },
      },
    })),
  };
}

/**
 * Generates JSON-LD Organization schema.
 */
export function generateOrganizationJsonLd(): Record<string, unknown> {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Nevumo',
    url: SITE_URL,
    logo: `${SITE_URL}/logo.png`,
    sameAs: [
      'https://x.com/nevumo',
    ],
  };
}

/**
 * Generates JSON-LD WebSite schema.
 */
export function generateWebSiteJsonLd(lang: string): Record<string, unknown> {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'Nevumo',
    url: `${SITE_URL}/${lang}`,
    potentialAction: {
      '@type': 'SearchAction',
      target: {
        '@type': 'EntryPoint',
        urlTemplate: `${SITE_URL}/${lang}/search?q={search_term_string}`,
      },
      'query-input': 'required name=search_term_string',
    },
  };
}
