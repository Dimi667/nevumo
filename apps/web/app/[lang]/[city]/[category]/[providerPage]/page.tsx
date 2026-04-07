import { notFound, redirect } from 'next/navigation';
import { getProviderBySlug, getCategories, resolveSlug } from '@/lib/api';
import ProviderWidget from '@/components/ProviderWidget';
import ClaimProfileBanner from '@/components/ClaimProfileBanner';
import { generateHreflangAlternates, generateLocalBusinessJsonLd } from '@/lib/seo';
import { JsonLd } from '@/components/JsonLd';

const CITY_COUNTRY_MAP: Record<string, string> = {
  warszawa: 'PL',
  sofia: 'BG',
  belgrade: 'RS',
  prague: 'CZ',
  athens: 'GR',
};

type ProviderRouteParams = {
  lang: string;
  city: string;
  category: string;
  providerPage: string;
};

function formatPrice(price: number | null, priceType: string, translations?: { services_label?: string; price_on_request?: string }): string {
  if (priceType === 'request' || price === null) return translations?.price_on_request || 'Price on request';
  if (priceType === 'hourly') return `${price} лв./h`;
  return `${price} лв.`;
}

function getInitials(name: string): string {
  return name.charAt(0).toUpperCase();
}

export async function generateMetadata(props: { params: Promise<ProviderRouteParams> }) {
  const { lang, city, category, providerPage } = await props.params;
  try {
    // Resolve slug to get the canonical slug (but don't redirect here - no access to searchParams)
    const slugResolution = await resolveSlug(providerPage);
    
    // Use the resolved slug for provider lookup (if found), otherwise fallback to original
    const slugToUse = slugResolution.found && slugResolution.slug ? slugResolution.slug : providerPage;
    
    const [provider, categories] = await Promise.all([
      getProviderBySlug(slugToUse, lang, city),
      getCategories(lang),
    ]);
    if (!provider) return { title: 'Nevumo' };
    const categoryName = categories.find((c) => c.slug === category)?.name ?? category;
    const description = provider.description ?? `Book ${provider.business_name} for ${categoryName} services.`;
    return {
      title: `${provider.business_name} | ${categoryName}`,
      description,
      alternates: {
        languages: generateHreflangAlternates(`/${city}/${category}/${slugToUse}`),
      },
      openGraph: {
        title: `${provider.business_name} | ${categoryName} | Nevumo`,
        description,
      },
    };
  } catch {
    return { title: 'Nevumo' };
  }
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

  const [provider, categories] = await Promise.all([
    getProviderBySlug(slugToUse, lang, city),
    getCategories(lang),
  ]);

  if (!provider) return notFound();

  const categoryName = categories.find((c) => c.slug === category)?.name ?? category;
  const cityCountryCode = CITY_COUNTRY_MAP[city] ?? 'BG';

  // Embed mode - render widget only
  if (isEmbed) {
    return (
      <div className="min-h-screen bg-gray-50 p-4">
        <div className="max-w-md mx-auto">
          <ProviderWidget
            provider={provider}
            categoryName={categoryName}
            categorySlug={category}
            citySlug={city}
            countryCode={cityCountryCode}
          />
        </div>
      </div>
    );
  }

  // Full page mode (existing logic)
  return (
    <>
      <JsonLd data={generateLocalBusinessJsonLd(provider, category, city)} />
      <div className="min-h-screen bg-gray-50 py-6 px-4">
        <div className="max-w-md mx-auto">
          {/* Claim profile banner for unclaimed providers */}
          {provider.is_claimed === false && lang === 'pl' && (
            <ClaimProfileBanner businessName={provider.business_name} lang={lang} />
          )}

          {/* Card */}
          <div className="bg-white rounded-2xl shadow-lg overflow-hidden pb-24 md:pb-0">

          {/* Logo bar */}
          <div className="px-6 pt-5 pb-2 text-center">
            <span className="text-xl font-extrabold tracking-tight">
              <span className="text-orange-500">N</span>evumo
            </span>
          </div>

          {/* Avatar + name + description */}
          <div className="px-6 pt-3 pb-5 text-center border-b border-gray-100">
            <div className="w-20 h-20 rounded-full bg-orange-100 flex items-center justify-center mx-auto mb-3">
              <span className="text-orange-600 text-3xl font-bold">
                {getInitials(provider.business_name)}
              </span>
            </div>

            <h1 className="text-xl font-bold text-gray-900 mb-1">
              {provider.business_name}
            </h1>

            {provider.description && (
              <p className="text-sm text-gray-500 mb-3">{provider.description}</p>
            )}

            <div className="flex items-center justify-center gap-3 flex-wrap">
              {provider.rating > 0 && (
                <span className="text-amber-500 font-semibold">
                  ⭐ {provider.rating.toFixed(1)} {provider.translations?.rating_label || 'rating'}
                </span>
              )}
              {provider.verified && (
                <span className="inline-flex items-center gap-1 text-sm font-semibold text-green-700 bg-green-50 border border-green-200 px-3 py-1 rounded-full">
                  ✓ {provider.translations?.verified_label || 'Verified professional'}
                </span>
              )}
            </div>
          </div>

          {/* Services */}
          {provider.services.length > 0 && (
            <div className="px-6 py-5 border-b border-gray-100">
              <h2 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">
                {provider.translations?.services_label || 'Services'}
              </h2>
              <ul className="space-y-3">
                {provider.services.map((service) => (
                  <li key={service.id}>
                    <div className="flex justify-between items-start gap-2">
                      <span className="font-semibold text-gray-800 text-sm">
                        {service.title}
                      </span>
                      <span className="text-sm font-bold text-gray-700 whitespace-nowrap flex-shrink-0">
                        {formatPrice(service.base_price, service.price_type, provider.translations)}
                      </span>
                    </div>
                    {service.description && (
                      <p className="text-xs text-gray-400 mt-0.5">{service.description}</p>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Request form */}
          <div className="px-6 py-5">
            <ProviderWidget
              provider={provider}
              categoryName={categoryName}
              categorySlug={category}
              citySlug={city}
              countryCode={cityCountryCode}
            />
          </div>

        </div>
      </div>
    </div>
    </>
  );
}
