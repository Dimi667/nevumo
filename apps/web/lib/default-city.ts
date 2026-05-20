import { getCityPreference } from './city-preference';
import { getCityBySlug } from './api';
import { validateCitySlug } from './slugs';

const LANGUAGE_TO_CITY: Record<string, string> = {
  pl: 'warszawa',
  bg: 'sofia',
  sr: 'belgrade',
};

const DEFAULT_CITY = 'warszawa';

export async function resolveDefaultCity(lang: string): Promise<string> {
  // 1. User preference
  const prefCity = getCityPreference();
  if (prefCity) {
    const cityData = await getCityBySlug(prefCity, lang);
    if (cityData) return validateCitySlug(prefCity);
  }
  
  // 2. Language mapping
  const langCity = LANGUAGE_TO_CITY[lang];
  if (langCity) {
    const cityData = await getCityBySlug(langCity, lang);
    if (cityData) return validateCitySlug(langCity);
  }
  
  // 3. Fallback
  return validateCitySlug(DEFAULT_CITY);
}
