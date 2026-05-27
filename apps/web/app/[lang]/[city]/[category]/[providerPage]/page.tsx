import { notFound, redirect } from 'next/navigation';
import { getProviderBySlug, getCategories, resolveSlug, getCityBySlug } from '@/lib/api';
import { fetchTranslations } from '@/lib/ui-translations';
import ProviderWidget from '@/components/ProviderWidget';
import ProviderFullPage from '@/components/provider/ProviderFullPage';
import ClaimProfileBanner from '@/components/ClaimProfileBanner';
import { generateHreflangAlternates, generateLocalBusinessJsonLd } from '@/lib/seo';
import { JsonLd } from '@/components/JsonLd';
import { getCurrency, formatCurrency } from '@/lib/currency';

type ProviderRouteParams = {
  lang: string;
  city: string;
  category: string;
  providerPage: string;
};

function formatPrice(price: number | null, priceType: string, currency: string, translations?: { services_label?: string; price_on_request?: string }): string {
  if (priceType === 'request' || price === null) return translations?.price_on_request || 'Price on request';
  return formatCurrency(price, currency) + (priceType === 'hourly' ? '/h' : '');
}

function getInitials(name: string): string {
  return name.charAt(0).toUpperCase();
}

export async function generateMetadata(props: { 
  params: Promise<ProviderRouteParams>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const { lang, city, category, providerPage } = await props.params;
  const searchParams = await props.searchParams;
  const isEmbed = searchParams.embed === '1';

  try {
    const slugResolution = await resolveSlug(providerPage);
    const slugToUse = slugResolution.found && slugResolution.slug ? slugResolution.slug : providerPage;

    const [provider, categories] = await Promise.all([
      getProviderBySlug(slugToUse, lang, city),
      getCategories(lang),
    ]);

    if (!provider) return { title: 'Nevumo' };

    const categoryName = categories.find((c) => c.slug === category)?.name ?? category;
    const description = provider.description ?? `Book ${provider.business_name} for ${categoryName} services.`;
    const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://nevumo.com';
    const canonicalUrl = `${SITE_URL}/${lang}/${city}/${category}/${slugToUse}`;

    return {
      title: `${provider.business_name} | ${categoryName}`,
      description,
      robots: {
        index: !isEmbed,
        follow: !isEmbed,
      },
      alternates: {
        canonical: canonicalUrl,
        languages: generateHreflangAlternates(`/${city}/${category}/${slugToUse}`),
      },
      openGraph: {
        title: `${provider.business_name} | ${categoryName} | Nevumo`,
        description,
        url: canonicalUrl,
      },
    };
  } catch {
    return { title: 'Nevumo' };
  }
}

export function generateViewport() {
  return {
    width: 'device-width',
    initialScale: 1,
    viewportFit: 'cover',
  };
}

export default async function Page(props: {
  params: Promise<ProviderRouteParams>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const { lang, city, category, providerPage } = await props.params;
  const searchParams = await props.searchParams;
  const isEmbed = searchParams.embed === '1';

  // Check for redirect first
  const slugResolution = await resolveSlug(providerPage);
  if (slugResolution.found && slugResolution.redirected) {
    // Preserve the full query string when redirecting
    const queryString = new URLSearchParams();
    for (const [key, value] of Object.entries(searchParams)) {
      if (value === undefined) continue;
      if (Array.isArray(value)) {
        value.forEach((v) => queryString.append(key, v));
      } else {
        queryString.set(key, value);
      }
    }
    const query = queryString.toString();
    const redirectUrl = `/${lang}/${city}/${category}/${slugResolution.slug}${query ? `?${query}` : ''}`;
    redirect(redirectUrl);
  }

  // Use the resolved slug consistently for provider lookups
  const slugToUse = slugResolution.found && slugResolution.slug ? slugResolution.slug : providerPage;

  const [provider, categories, cityData, providerPageT, categoryT, widgetT, footerT] = await Promise.all([
    getProviderBySlug(slugToUse, lang, city),
    getCategories(lang),
    getCityBySlug(city, lang),
    fetchTranslations(lang, 'provider_page'),
    fetchTranslations(lang, 'category'),
    fetchTranslations(lang, 'widget'),
    fetchTranslations(lang, 'footer'),
  ]);
  const mergedT = { ...categoryT, ...widgetT, ...providerPageT, ...footerT };

  if (!provider) return notFound();

  const categoryName = categories.find((c) => c.slug === category)?.name ?? category;
  const cityName = cityData?.city || city;
  const cityCountryCode = cityData?.country_code ?? 'BG';

  // Embed mode - render widget only
  if (isEmbed) {
    return (
      <>
        <style>{`[data-global-header] { display: none !important; } [data-global-footer] { display: none !important; }`}</style>
        <div className="min-h-screen bg-gray-50 p-4">
          <div className="max-w-md mx-auto">
            <ProviderWidget
              provider={provider}
              categoryName={categoryName}
              categorySlug={category}
              citySlug={city}
              countryCode={cityCountryCode}
              isEmbed={true}
              translations={mergedT}
              lang={lang}
            />
          </div>
        </div>
      </>
    );
  }

  // Full page mode - render ProviderFullPage
  return (
    <>
      <JsonLd data={generateLocalBusinessJsonLd(provider, category, cityName, cityCountryCode)} />
      <ProviderFullPage
        provider={{
          ...provider,
          city_name: cityName,
          category_name: categoryName,
          category_slug: category,
          city_slug: city,
          lang,
        }}
        translations={mergedT}
        lang={lang}
      />
    </>
  );
}
