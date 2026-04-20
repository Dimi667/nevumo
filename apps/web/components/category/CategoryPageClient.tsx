'use client';

import dynamic from 'next/dynamic';
import LeadForm from './LeadForm';

// Dynamically import the sticky button to avoid SSR issues
const StickyLeadFormButton = dynamic(() => import('./StickyLeadFormButton'), {
  ssr: false
});

interface CategoryPageClientProps {
  translations: Record<string, string>;
  categorySlug: string;
  citySlug: string;
  lang: string;
  cityName: string;
  services?: Array<{ id: string; title: string }>;
  cityCountryCode: string;
  stickyButtonLabel: string;
}

export default function CategoryPageClient({
  translations,
  categorySlug,
  citySlug,
  lang,
  cityName,
  services,
  cityCountryCode,
  stickyButtonLabel
}: CategoryPageClientProps) {
  return (
    <>
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
