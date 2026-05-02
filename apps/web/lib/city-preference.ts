const CITY_PREFERENCE_KEY = 'nevumo_city_preference';

export const saveCityPreference = (citySlug: string) => {
  if (typeof window === 'undefined') return;
  localStorage.setItem(CITY_PREFERENCE_KEY, citySlug);
};

export const getCityPreference = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(CITY_PREFERENCE_KEY);
};

export const clearCityPreference = () => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(CITY_PREFERENCE_KEY);
};
