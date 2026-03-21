import type { MetadataRoute } from 'next';
import { getCategories, getCities, getProviders } from '@/lib/api';
import { SUPPORTED_LANGUAGES } from '@/lib/locales';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://nevumo.com';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  try {
    const [categories, cities] = await Promise.all([
      getCategories('en'),
      getCities('BG'),
    ]);

    const entries: MetadataRoute.Sitemap = [];

    // Language landing pages
    for (const lang of SUPPORTED_LANGUAGES) {
      entries.push({
        url: `${SITE_URL}/${lang}`,
        changeFrequency: 'weekly',
        priority: 0.5,
      });
    }

    // Category listing + provider pages
    for (const city of cities) {
      for (const category of categories) {
        // Category listing pages (all languages)
        for (const lang of SUPPORTED_LANGUAGES) {
          entries.push({
            url: `${SITE_URL}/${lang}/${city.slug}/${category.slug}`,
            changeFrequency: 'daily',
            priority: 0.9,
          });
        }

        // Fetch providers for this city+category combo
        let providers: Awaited<ReturnType<typeof getProviders>> = [];
        try {
          providers = await getProviders(category.slug, city.slug, 'en');
        } catch {
          providers = [];
        }

        // Provider pages (all languages)
        for (const provider of providers) {
          for (const lang of SUPPORTED_LANGUAGES) {
            entries.push({
              url: `${SITE_URL}/${lang}/${city.slug}/${category.slug}/${provider.slug}`,
              changeFrequency: 'weekly',
              priority: 0.8,
            });
          }
        }
      }
    }

    return entries;
  } catch {
    return [];
  }
}
