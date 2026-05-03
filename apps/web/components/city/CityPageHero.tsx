import CityHeroChips from '@/components/city/CityHeroChips';
import { getLocalizedCityText } from '@/lib/cityHelpers';

interface CityPageHeroProps {
  translations: Record<string, string>;
  cityName: string;
  providerCount: number;
  requestCount: number;
  averageRating: number | null;
  lang: string;
  citySlug: string;
  categories: { id: number; slug: string; name: string }[];
  categoryTranslations: Record<string, string>;
  countryCode?: string;
}

export default function CityPageHero({
  translations,
  cityName,
  providerCount,
  requestCount,
  averageRating,
  lang,
  citySlug,
  categories,
  categoryTranslations,
  countryCode,
}: CityPageHeroProps) {
  let title = '';
  let subtitle = '';
  let trust = '';

  // Determine state logic
  if (providerCount === 0) {
    // State 0
    title = getLocalizedCityText(translations['hero_title'] || 'Find services in {city}', lang, cityName, translations);
    subtitle = translations['hero_subtitle_0'] || '';
    trust = translations['hero_trust_0'] || '';
  } else if (providerCount >= 1 && providerCount <= 5 && requestCount === 0) {
    // State 1
    title = getLocalizedCityText(translations['hero_title'] || 'Find services in {city}', lang, cityName, translations);
    subtitle = translations['hero_subtitle_few'] || '';
    trust = translations['hero_trust_few'] || '';
  } else if (providerCount > 0 && requestCount > 0 && (averageRating === null || averageRating === 0)) {
    // State 2
    title = getLocalizedCityText(translations['hero_title'] || 'Find services in {city}', lang, cityName, translations);
    subtitle = translations['hero_subtitle_active'] || '';
    trust = (translations['hero_trust_requests'] || '').replace('{count}', String(requestCount));
  } else if (providerCount > 0 && requestCount > 0 && averageRating !== null && averageRating > 0) {
    // State 3
    title = getLocalizedCityText(translations['hero_title'] || 'Find services in {city}', lang, cityName, translations);
    subtitle = translations['hero_subtitle_active'] || '';
    trust = (translations['hero_trust_full'] || '')
      .replace('{rating}', averageRating.toFixed(1))
      .replace('{count}', String(requestCount));
  }

  return (
    <section className="min-h-[420px] md:min-h-[500px] flex items-center text-center bg-gradient-to-br from-orange-400 to-orange-700 py-20 px-4">
      <div className="max-w-4xl mx-auto w-full">
        <h1 className="text-4xl md:text-6xl font-bold text-white mb-4 leading-tight">
          {title}
        </h1>
        <p className="text-white/90 text-xl md:text-2xl mb-8 max-w-2xl mx-auto font-medium drop-shadow">
          {subtitle}
        </p>

        <CityHeroChips
          categories={categories}
          categoryTranslations={categoryTranslations}
          citySlug={citySlug}
          lang={lang}
          countryCode={countryCode}
        />

        <p className="text-sm text-white mt-6">{trust}</p>
        <p className="text-sm text-white mt-1">{translations["hero_cta_sub"]}</p>
      </div>
    </section>
  );
}
