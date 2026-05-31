'use client';

import dynamic from 'next/dynamic';
import Link from 'next/link';
import { useEffect } from 'react';
import LeadForm from './LeadForm';
import { setCtx } from '@/lib/ctx';

// Dynamically import the sticky button to avoid SSR issues
const StickyLeadFormButton = dynamic(() => import('./StickyLeadFormButton'), {
  ssr: false
});

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

interface CategoryPageClientProps {
  translations: Record<string, string>;
  categorySlug: string;
  citySlug: string;
  city: string;
  category: string;
  lang: string;
  cityName: string;
  services?: Array<{ id: string; title: string }>;
  cityCountryCode: string;
  stickyButtonLabel: string;
  providers: EnrichedProvider[];
  visibleProviders: EnrichedProvider[];
  hiddenProviders: EnrichedProvider[];
  hiddenCount: number;
  providerCardTexts: ProviderCardTexts;
  widgetT: Record<string, string>;
  categoryT: Record<string, string>;
  cityT: Record<string, string>;
  grammaticalCase: 'nominative' | 'locative' | 'genitive';
  cityData?: { locative_form?: string; genitive_form?: string };
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

function getBadge(
  verificationLevel: number,
  cityName: string,
  t: Record<string, string>
): { label: string; className: string } {
  if (verificationLevel === 2) {
    return {
      label: '★ ' + (t['badge_top_specialist'] ?? 'Top specialist') + ' – ' + cityName,
      className: 'bg-orange-100 text-orange-700',
    };
  }
  if (verificationLevel === 1) {
    return {
      label: '✓ ' + (t['badge_verified'] ?? 'Verified specialist'),
      className: 'bg-green-100 text-green-700',
    };
  }
  return {
    label: '⚡ ' + (t['badge_new_provider'] ?? 'New to Nevumo'),
    className: 'bg-blue-50 text-blue-400',
  };
}

function isWithin90Days(dateStr: string | null): boolean {
  if (!dateStr) return false;
  const date = new Date(dateStr);
  const now = new Date();
  const diffDays = (now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24);
  return diffDays <= 90;
}

function getLocalizedCityText(
  str: string,
  lang: string,
  cityName: string,
  cityT: Record<string, string>,
  grammaticalCase: 'nominative' | 'locative' | 'genitive',
  cityData?: { locative_form?: string; genitive_form?: string }
): string {
  // Simplified version - in real implementation this would use the full helper
  return str.replace(/{city}/g, cityName);
}

function ProviderCard({
  provider,
  href,
  texts,
  cityName,
  widgetT,
}: {
  provider: EnrichedProvider;
  href: string;
  texts: ProviderCardTexts;
  cityName: string;
  widgetT: Record<string, string>;
}) {
  const hasLeads = provider.leadsReceived > 0;
  const hasJobs = provider.jobsCompleted > 0;
  const hasRating = provider.rating > 0;
  const hasRecentLead =
    isWithin90Days(provider.latestLeadPreviewCreatedAt) &&
    provider.latestLeadPreviewClientName !== null;

  const badge = getBadge(provider.verificationLevel, cityName, widgetT);

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
                {provider.services.slice(0, 4).map((service) => (
                  <div key={service.id}>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-700 font-medium min-w-0 truncate">{service.title}</span>
                      <span className="font-medium text-gray-900 shrink-0">
                        {formatPrice(service.basePrice, service.priceType, service.currency, texts.onRequest)}
                      </span>
                    </div>
                    {service.description && (
                      <p className="text-xs text-gray-500 line-clamp-1 mt-0.5">{service.description}</p>
                    )}
                  </div>
                ))}
                {!hasAnyDescription && (
                  <p className="text-xs text-gray-500 line-clamp-1">{texts.defaultDescription}</p>
                )}
                {provider.services.length > 4 && (
                  <div className="text-xs text-orange-600 font-medium">
                    {texts.moreServices.replace('{n}', String(provider.services.length - 4))}
                  </div>
                )}
              </div>
            );
          })()}

          <div className="mt-4 flex flex-wrap gap-2 text-xs font-medium text-gray-600 max-w-full">
            <span className={`rounded-full px-3 py-1.5 ${badge.className}`}>
              {badge.label}
            </span>
            {hasRating && hasJobs && (
              <span className="rounded-full bg-amber-50 px-3 py-1.5 text-amber-700">
                ⭐ {provider.rating.toFixed(1)} • {provider.reviewCount} {texts.reviews}
              </span>
            )}
            {hasJobs && (
              <span className="rounded-full bg-gray-50 px-3 py-1.5">
                ✅ {provider.jobsCompleted} {texts.jobsCompleted}
              </span>
            )}
            {hasRecentLead && (
              <span className="rounded-full bg-gray-50 px-3 py-1.5 truncate">
                ⚡ {provider.latestLeadPreviewClientName} {texts.recentlyRequested}
              </span>
            )}
            <span className="rounded-full bg-gray-50 px-3 py-1.5">
              ✓ {texts.directContact}
            </span>
          </div>

          <Link
            href={href}
            className="mt-5 inline-flex w-full items-center justify-center rounded-xl bg-orange-500 px-4 py-3 text-sm font-semibold text-white transition hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-offset-2"
          >
            {texts.sendRequest} {provider.businessName}
          </Link>
        </div>
      </div>
    </article>
  );
}

export default function CategoryPageClient({
  translations,
  categorySlug,
  citySlug,
  city,
  category,
  lang,
  cityName,
  services,
  cityCountryCode,
  stickyButtonLabel,
  providers,
  visibleProviders,
  hiddenProviders,
  hiddenCount,
  providerCardTexts,
  widgetT,
  categoryT,
  cityT,
  grammaticalCase,
  cityData
}: CategoryPageClientProps) {
  useEffect(() => {
    setCtx({ city, category });
  }, [city, category]);

  return (
    <>
      {/* Providers List - Client-side rendering to avoid hydration mismatch */}
      <section className="space-y-4">
        {providers.length === 0 ? (
          <div className="rounded-xl border border-gray-100 bg-white px-6 py-12 text-center shadow-sm">
            <div className="border-l-4 border-orange-400 pl-4 py-2 mb-4 text-left inline-block">
              <p className="font-semibold text-gray-800 text-sm">
                {getLocalizedCityText((categoryT['no_providers_title'] || 'Be the first to request this service in your area'), lang, cityName, cityT, grammaticalCase, cityData)}
              </p>
              <p className="text-sm text-gray-500 mt-0.5">
                {getLocalizedCityText((categoryT['no_providers_subtitle'] || 'Providers joining Nevumo will see your request and contact you'), lang, cityName, cityT, grammaticalCase, cityData)}
              </p>
            </div>
          </div>
        ) : (
          <>
            {visibleProviders.map((provider) => {
              const providerHref = `/${lang}/${city}/${category}/${provider.slug}`;
              return <ProviderCard key={provider.id} provider={provider} href={providerHref} texts={providerCardTexts} cityName={cityName} widgetT={widgetT} />;
            })}
            {hiddenCount > 0 && (
              <details className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
                <summary className="cursor-pointer list-none text-center text-sm font-semibold text-orange-600">
                  {categoryT['show_more'] || 'Show more'}
                </summary>
                <div className="mt-4 space-y-4">
                  {hiddenProviders.map((provider) => {
                    const providerHref = `/${lang}/${city}/${category}/${provider.slug}`;
                    return <ProviderCard key={provider.id} provider={provider} href={providerHref} texts={providerCardTexts} cityName={cityName} widgetT={widgetT} />;
                  })}
                </div>
              </details>
            )}
          </>
        )}
      </section>

      {/* Mobile Lead Form - hidden on desktop */}
      <div id="lead-form-anchor" className="lg:hidden">
        <div className="rounded-xl border border-orange-100 bg-white p-6 shadow-lg mb-8">
          <LeadForm
            translations={translations}
            categorySlug={categorySlug}
            citySlug={citySlug}
            lang={lang}
            cityName={cityName}
            services={services}
            countryCode={cityCountryCode}
            title={translations['form_btn']}
          />
        </div>
      </div>

      {/* Sticky Mobile CTA Button */}
      <StickyLeadFormButton label={stickyButtonLabel} />
    </>
  );
}
