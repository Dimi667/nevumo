import Link from 'next/link';
import Image from 'next/image';
import { getActiveCities } from '@/lib/api';
import { generateHreflangAlternates } from '@/lib/seo';
import { SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE } from '@/lib/locales';

interface PageProps {
  params: Promise<{ lang: string }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : DEFAULT_LANGUAGE;
  
  return {
    title: 'Choose a city — Nevumo',
    description: 'Find trusted local services in your city. Select your location to browse available specialists.',
    alternates: {
      canonical: `/${normalizedLang}/izberi-grad`,
      languages: generateHreflangAlternates('/izberi-grad'),
    },
    openGraph: {
      title: 'Choose a city — Nevumo',
      description: 'Find trusted local services in your city. Select your location to browse available specialists.',
      url: `${process.env.NEXT_PUBLIC_SITE_URL}/${normalizedLang}/izberi-grad`,
      siteName: 'Nevumo',
      locale: normalizedLang,
      type: 'website',
    },
  };
}

export default async function ChooseCityPage({ params }: PageProps) {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : DEFAULT_LANGUAGE;
  const cities = await getActiveCities(normalizedLang);

  return (
    <div className="min-h-screen bg-white">
      {/* NAVBAR */}
      <nav className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto">
        <Link href={`/${normalizedLang}`} className="inline-flex items-center">
          <Image src="/Nevumo_logo.svg" alt="Nevumo" width={120} height={36} priority />
        </Link>
        <Link href={`/${normalizedLang}/auth?mode=register&role=provider`} className="text-sm text-gray-600 transition-colors hover:text-orange-600">
          Become a specialist
        </Link>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-12">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-8 text-center">
          In which city are you looking for a service?
        </h1>

        {cities.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-xl text-gray-600 font-medium">Очаквай скоро</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {cities.map((city) => (
              <Link
                key={city.id}
                href={`/${normalizedLang}/${city.slug}`}
                className="nevumo-card flex items-center justify-between hover:border-orange-500 hover:shadow-md transition-all group"
              >
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 group-hover:text-orange-600 transition-colors">
                    {city.city}
                  </h3>
                  <p className="text-sm text-gray-500 uppercase tracking-wider">
                    {city.country_code}
                  </p>
                </div>
                <div className="text-orange-500 transform group-hover:translate-x-1 transition-transform">
                  <svg 
                    width="24" 
                    height="24" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    strokeWidth="2" 
                    strokeLinecap="round" 
                    strokeLinejoin="round"
                  >
                    <path d="M9 18l6-6-6-6" />
                  </svg>
                </div>
              </Link>
            ))}
          </div>
        )}
      </main>

      {/* FOOTER */}
      <footer className="py-12 px-6 bg-gray-50 border-t border-gray-200 mt-auto">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-gray-500 text-sm">
            Nevumo — Connecting you with local specialists
          </p>
        </div>
      </footer>
    </div>
  );
}
