import Link from 'next/link';
import Image from 'next/image';
import type { Metadata } from 'next';
import { getCategories, getCityBySlug, API_BASE } from '@/lib/api';
import CityPageHero from '@/components/city/CityPageHero';
import { generateHreflangAlternates } from '@/lib/seo';
import { fetchTranslations, t } from '@/lib/ui-translations';

interface PageProps {
  params: Promise<{ lang: string; city: string }>;
}

// Category icon mapping (reused from homepage patterns)
const categoryIcons: Record<string, React.ReactNode> = {
  cleaning: (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ff5a1f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>
      <path d="M20 3v4M22 5h-4M4 17v2M5 18H3"/>
    </svg>
  ),
  plumbing: (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ff5a1f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
    </svg>
  ),
  massage: (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ff5a1f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
      <path d="M12 5 9.04 7.96a2.17 2.17 0 0 0 0 3.08c.82.82 2.13.85 3 .07l2.07-1.9a2.82 2.82 0 0 1 3.79 0l2.96 2.66"/>
      <path d="m18 15-2-2"/>
      <path d="m15 18-2-2"/>
    </svg>
  ),
};

// Fallback categories for development/testing
const fallbackCategories = [
  { id: 1, slug: 'cleaning', name: 'Cleaning' },
  { id: 2, slug: 'plumbing', name: 'Plumbing' },
  { id: 3, slug: 'massage', name: 'Massage' },
];

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { lang, city } = await params;
  const cityT = await fetchTranslations(lang, 'city');
  const cityData = await getCityBySlug(city, lang);
  const cityName = cityData?.city || city.charAt(0).toUpperCase() + city.slice(1);

  const title = t(cityT, 'seo_title', `${cityName} — Local Services | Nevumo`).replace('{city}', cityName);
  const description = t(cityT, 'seo_description', `Find trusted local services in ${cityName}. Free requests, no obligation. Cleaning, plumbing, massage and more.`).replace('{city}', cityName);

  return {
    title,
    description,
    alternates: {
      languages: generateHreflangAlternates(`/${city}`),
    },
    openGraph: {
      title,
      description,
    },
  };
}

export default async function CityPage({ params }: PageProps) {
  const { lang, city } = await params;
  const cityT = await fetchTranslations(lang, 'city');
  const categoryT = await fetchTranslations(lang, 'category');
  const categories = await getCategories(lang);
  const cityData = await getCityBySlug(city, lang);
  const cityName = cityData?.city || city.charAt(0).toUpperCase() + city.slice(1);

  // Fetch city stats
  let cityStats = { provider_count: 0, request_count: 0, average_rating: 0 };
  try {
    const statsRes = await fetch(`${API_BASE}/api/v1/cities/${city}/stats`, {
      next: { revalidate: 3600 }
    });
    if (statsRes.ok) {
      const statsJson = await statsRes.json();
      cityStats = statsJson;
    }
  } catch (error) {
    console.error('Failed to fetch city stats:', error);
  }

  // Use API categories or fallback for development
  const displayCategories = categories.length > 0 ? categories : fallbackCategories;

  return (
    <div className="min-h-screen bg-white">
      {/* NAVBAR */}
      <nav className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto">
        <Link href={`/${lang}`} className="inline-flex items-center">
          <Image src="/Nevumo_logo.svg" alt="Nevumo" width={120} height={36} priority />
        </Link>
        <Link href={`/${lang}/auth?mode=register&role=provider`} className="text-sm text-gray-600 transition-colors hover:text-orange-600">
          {t(cityT, 'nav_link', 'Become a specialist')}
        </Link>
      </nav>

      {/* HERO SECTION */}
      <CityPageHero
        translations={cityT}
        cityName={cityName}
        providerCount={cityStats.provider_count}
        requestCount={cityStats.request_count}
        averageRating={cityStats.average_rating === 0 ? null : cityStats.average_rating}
        lang={lang}
        citySlug={city}
        categories={displayCategories}
        categoryTranslations={categoryT}
        countryCode={cityData?.country_code}
      />

      {/* CATEGORY GRID */}
      <section className="py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold text-center mb-12 text-gray-900">
            {t(cityT, 'categories_title', 'Popular services in {city}').replace('{city}', cityName)}
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {displayCategories.map((category) => (
              <Link
                key={category.id}
                href={`/${lang}/${city}/${category.slug}`}
                className="nevumo-card text-center hover:shadow-lg transition-shadow"
              >
                <div className="text-orange-500 mb-3">
                  {categoryIcons[category.slug] || categoryIcons.cleaning}
                </div>
                <h3 className="text-xl font-semibold mb-2 text-gray-900">{category.name}</h3>
                <p className="text-gray-600 mb-4">
                  {t(cityT, `cat_${category.slug}_leads`, 'Available now')}
                </p>
                <span className="inline-block text-orange-600 font-semibold text-sm">
                  {t(cityT, 'cat_cta', 'View providers')} →
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>


      {/* HOW IT WORKS */}
      <section className="py-16 px-6 bg-gray-100">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">
            {t(cityT, 'how_title', 'How it works')}
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">
                {t(cityT, 'how_step_1', 'Describe your request')}
              </h3>
              <p className="text-gray-600">
                {t(cityT, 'how_step_1_sub', 'Takes 2 minutes')}
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">
                {t(cityT, 'how_step_2', 'Get offers from specialists')}
              </h3>
              <p className="text-gray-600">
                {t(cityT, 'how_step_2_sub', 'Usually within 30 minutes')}
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">
                {t(cityT, 'how_step_3', 'Choose and connect directly')}
              </h3>
              <p className="text-gray-600">
                {t(cityT, 'how_step_3_sub', 'No commission, no middlemen')}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* SEO CONTENT BLOCK */}
      <section className="py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold mb-6 text-gray-900">
            {t(cityT, 'seo_title', `Services in ${cityName}`).replace('{city}', cityName)}
          </h2>
          <div className="prose prose-gray max-w-none">
            <p className="text-gray-700 leading-relaxed">
              {t(cityT, 'seo_description', `Looking for reliable services in ${cityName}? Nevumo connects you with verified local specialists. From home cleaning to plumbing repairs and professional massage therapy, find the right provider for your needs.`).replace('{city}', cityName)}
            </p>
            <p className="text-gray-700 leading-relaxed mt-4">
              {t(cityT, 'seo_p2', 'All specialists on our platform are reviewed by real customers. Send a free request, compare offers, and choose the best match for your project. No hidden fees, no obligations.')}
            </p>
            <p className="text-gray-700 leading-relaxed mt-4">
              {t(cityT, 'seo_p3', 'Whether you need a one-time service or ongoing support, our network of professionals in {city} is ready to help. Get started with a simple request and receive responses within hours.').replace('{city}', cityName)}
            </p>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="py-12 px-6 bg-gray-50 border-t border-gray-200">
        <div className="max-w-4xl mx-auto text-center">
          <p className="mb-4 text-gray-700">
            {t(cityT, 'footer_title', 'Nevumo — Connecting you with local specialists')}
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm">
            {displayCategories.slice(0, 3).map((cat) => (
              <Link
                key={cat.id}
                href={`/${lang}/${city}/${cat.slug}`}
                className="text-gray-600 hover:text-orange-600 transition"
              >
                {cat.name} {t(cityT, 'footer_in', 'in')} {cityName}
              </Link>
            ))}
          </div>
        </div>
      </footer>
    </div>
  );
}
