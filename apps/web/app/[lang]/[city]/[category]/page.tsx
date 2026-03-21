import Link from 'next/link';
import { getProviders, getCategories, getCities } from '@/lib/api';
import { generateHreflangAlternates, generateServiceListJsonLd } from '@/lib/seo';
import { JsonLd } from '@/components/JsonLd';

interface PageProps {
  params: Promise<{ lang: string; city: string; category: string }>;
}

function capitalize(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function getInitials(name: string): string {
  return name.charAt(0).toUpperCase();
}

export async function generateMetadata({ params }: PageProps) {
  const { lang, city, category } = await params;

  const [categories, cities] = await Promise.all([
    getCategories(lang),
    getCities('BG'),
  ]);

  const categoryName = categories.find((c) => c.slug === category)?.name ?? category;
  const cityName = cities.find((c) => c.slug === city)?.name ?? city;

  const description = `Find the best ${categoryName} providers in ${cityName}. Compare ratings, read reviews, and book services on Nevumo.`;
  return {
    title: `${categoryName} in ${cityName}`,
    description,
    alternates: {
      languages: generateHreflangAlternates(`/${city}/${category}`),
    },
    openGraph: {
      title: `${categoryName} in ${cityName} | Nevumo`,
      description,
    },
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
    <>
      <JsonLd data={generateServiceListJsonLd(providers, categoryName, cityName)} />
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-2xl mx-auto">

        <h1 className="text-2xl font-bold text-gray-900 mb-1">
          {capitalize(categoryName)} in {capitalize(cityName)}
        </h1>
        <p className="text-sm text-gray-400 mb-6">
          {providers.length} provider{providers.length !== 1 ? 's' : ''} found
        </p>

        {providers.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-2xl border border-gray-100 shadow-sm">
            <p className="text-gray-600 font-medium">No providers found in this category yet.</p>
            <p className="text-gray-400 text-sm mt-1">Check back soon!</p>
          </div>
        ) : (
          <div className="space-y-3">
            {providers.map((provider) => (
              <Link
                key={provider.id}
                href={`/${lang}/${city}/${category}/${provider.slug}`}
                className="flex items-center gap-4 bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md hover:border-gray-200 transition-all p-4"
              >
                {/* Initials avatar */}
                <div className="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center flex-shrink-0">
                  <span className="text-orange-600 font-bold text-base">
                    {getInitials(provider.business_name)}
                  </span>
                </div>

                {/* Info */}
                <div className="flex-1 min-w-0">
                  <p className="font-bold text-gray-900 truncate">{provider.business_name}</p>
                  <div className="flex items-center gap-2 mt-0.5 flex-wrap">
                    <span className="text-amber-500 font-semibold text-sm">
                      ⭐ {provider.rating.toFixed(1)}
                    </span>
                    {provider.verified && (
                      <span className="inline-flex items-center gap-0.5 text-xs font-semibold text-green-700 bg-green-50 px-2 py-0.5 rounded-full">
                        ✓ Verified
                      </span>
                    )}
                  </div>
                </div>

                {/* View arrow */}
                <span className="text-gray-400 font-semibold text-sm flex-shrink-0">View →</span>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
    </>
  );
}
