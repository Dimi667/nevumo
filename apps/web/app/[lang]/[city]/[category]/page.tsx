import Link from 'next/link';
import { getProviders, getCategories, getCities } from '@/lib/api';

interface PageProps {
  params: Promise<{ lang: string; city: string; category: string }>;
}

function capitalize(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

export async function generateMetadata({ params }: PageProps) {
  const { lang, city, category } = await params;

  const [categories, cities] = await Promise.all([
    getCategories(lang),
    getCities('BG'),
  ]);

  const categoryName = categories.find((c) => c.slug === category)?.name ?? category;
  const cityName = cities.find((c) => c.slug === city)?.name ?? city;

  return {
    title: `${categoryName} in ${cityName} | Nevumo`,
    description: `Find the best ${categoryName} providers in ${cityName}. Compare ratings, read reviews, and book services on Nevumo.`,
  };
}

export default async function CategoryPage({ params }: PageProps) {
  const { lang, city, category } = await params;

  const [providers, categories, cities] = await Promise.all([
    getProviders(category, city, lang),
    getCategories(lang),
    getCities('BG'),
  ]);

  const categoryName = categories.find((c) => c.slug === category)?.name ?? category;
  const cityName = cities.find((c) => c.slug === city)?.name ?? city;

  return (
    <main className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">
          {capitalize(categoryName)} in {capitalize(cityName)}
        </h1>

        <p className="text-gray-500 mb-6 text-sm">
          {providers.length} provider{providers.length !== 1 ? 's' : ''} found
        </p>

        {providers.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-2xl border border-gray-100 shadow-sm">
            <p className="text-gray-600 text-lg font-medium">No providers found in this category yet.</p>
            <p className="text-gray-400 text-sm mt-1">Check back soon!</p>
          </div>
        ) : (
          <div className="grid gap-3 sm:grid-cols-2">
            {providers.map((provider) => (
              <Link
                key={provider.id}
                href={`/${lang}/${city}/${category}/${provider.slug}`}
                className="flex items-center justify-between bg-white rounded-2xl border border-gray-100 shadow-sm p-5 hover:shadow-md hover:border-gray-200 transition-all no-underline"
              >
                <div className="min-w-0">
                  <h2 className="text-base font-bold text-gray-900 mb-1 truncate">
                    {provider.business_name}
                  </h2>
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-amber-500 font-semibold text-sm">
                      ★ {provider.rating.toFixed(1)}
                    </span>
                    {provider.verified && (
                      <span className="inline-flex items-center gap-1 text-xs font-semibold text-green-700 bg-green-50 px-2 py-0.5 rounded-full">
                        ✓ Verified
                      </span>
                    )}
                  </div>
                </div>
                <span className="text-gray-400 font-semibold ml-4 flex-shrink-0">View →</span>
              </Link>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
