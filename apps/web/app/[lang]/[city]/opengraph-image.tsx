import { fetchTranslations, t } from '@/lib/ui-translations';
import { BaseOGImage } from '@/lib/og/base-og-image';
import { getCityBySlug } from '@/lib/api';
import { getLocalizedCityText } from '@/lib/cityHelpers';

interface OGImageProps {
  params: Promise<{ lang: string; city: string }>;
}

export const runtime = 'nodejs';

export default async function OGImage({ params }: OGImageProps) {
  const { lang, city: citySlug } = await params;
  
  // Fetch translations
  const homepageT = await fetchTranslations(lang, 'homepage');
  const cityT = await fetchTranslations(lang, 'city');
  
  // Get city data
  const cityData = await getCityBySlug(citySlug, lang);
  const cityName = cityData?.city || citySlug;

  // Slavic languages that use grammatical cases (locative/genitive)
  const slavicLanguagesWithDeclension = ['bg', 'cs', 'sk', 'ru', 'uk', 'sr', 'hr', 'mk', 'sl', 'pl'];
  const grammaticalCase = slavicLanguagesWithDeclension.includes(lang) ? 'locative' : 'nominative';
  
  // Get translated OG content with city localization
  const title = getLocalizedCityText(
    t(homepageT, 'city_meta_title', 'Services in {city}'),
    lang,
    cityName,
    cityT,
    grammaticalCase
  );
  const description = getLocalizedCityText(
    t(homepageT, 'city_meta_description', 'Find local services in {city}'),
    lang,
    cityName,
    cityT,
    grammaticalCase
  );
  const ctaText = t(homepageT, 'og_cta', 'Start for free');
  
  // Use BaseOGImage component
  return await BaseOGImage({
    title,
    description,
    ctaText,
  });
}
