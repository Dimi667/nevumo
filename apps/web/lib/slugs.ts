import { getCategories, getActiveCities } from './api';

export async function getValidCitySlugs(): Promise<string[]> {
  const cities = await getActiveCities('en');
  return cities.map((c) => c.slug);
}

export async function getValidCategorySlugs(): Promise<string[]> {
  const categories = await getCategories('en');
  return categories.map((c) => c.slug);
}

export async function validateCitySlug(slug: string): Promise<string> {
  const valid = await getValidCitySlugs();
  if (!valid.includes(slug)) {
    const msg = `Invalid city slug: "${slug}". Valid slugs: ${valid.join(', ')}`;
    if (process.env.NODE_ENV === 'development') throw new Error(msg);
    console.warn('[slugs]', msg);
  }
  return slug;
}

export async function validateCategorySlug(slug: string): Promise<string> {
  const valid = await getValidCategorySlugs();
  if (!valid.includes(slug)) {
    const msg = `Invalid category slug: "${slug}". Valid slugs: ${valid.join(', ')}`;
    if (process.env.NODE_ENV === 'development') throw new Error(msg);
    console.warn('[slugs]', msg);
  }
  return slug;
}
