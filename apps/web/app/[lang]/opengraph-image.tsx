import { fetchTranslations, t } from '@/lib/ui-translations';
import { BaseOGImage } from '@/lib/og/base-og-image';
import { resolveDefaultCity } from '@/lib/default-city';
import { getCityBySlug } from '@/lib/api';
import { getLocalizedCityText } from '@/lib/cityHelpers';

interface OGImageProps {
  params: Promise<{ lang: string }>;
}

export const runtime = 'nodejs';

export default async function OGImage({ params }: OGImageProps) {
  const { lang } = await params;
  
  // Fetch translations for homepage and city
  const homepageT = await fetchTranslations(lang, 'homepage');
  const cityT = await fetchTranslations(lang, 'city');
  
  // Resolve city for dynamic translations
  const citySlug = await resolveDefaultCity(lang);
  const cityData = await getCityBySlug(citySlug, lang);
  const cityName = cityData?.city || 'Warsaw';

  // Slavic languages that use grammatical cases (locative/genitive)
  const slavicLanguagesWithDeclension = ['bg', 'cs', 'sk', 'ru', 'uk', 'sr', 'hr', 'mk', 'sl', 'pl'];
  const grammaticalCase = slavicLanguagesWithDeclension.includes(lang) ? 'locative' : 'nominative';
  
  // Get translated OG content with fallbacks and city localization
  const title = getLocalizedCityText(
    t(homepageT, 'meta_title', 'Get clients for your services'),
    lang,
    cityName,
    cityT,
    grammaticalCase
  );
  const description = getLocalizedCityText(
    t(homepageT, 'meta_description', 'Free registration. No commission.'),
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
