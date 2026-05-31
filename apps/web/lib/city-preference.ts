import { setCtx, getCtx, clearCityCtx } from './ctx';

export const saveCityPreference = (citySlug: string) => {
  setCtx({ city: citySlug });
};

export const getCityPreference = (): string | null => {
  const ctx = getCtx();
  return ctx.city || null;
};

export const clearCityPreference = () => {
  clearCityCtx();
};
