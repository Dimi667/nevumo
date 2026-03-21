import Link from 'next/link';
import { getProviders, getCategories, getCities } from '@/lib/api';

interface PageProps {
  params: Promise<{ lang: string; city: string; category: string }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { lang, city, category } = await params;

  const [categories, cities] = await Promise.all([
    getCategories(lang),
    getCities('BG'),
  ]);

  const categoryName =
    categories.find((c) => c.slug === category)?.name ?? category;
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

  const categoryName =
    categories.find((c) => c.slug === category)?.name ?? category;
  const cityName = cities.find((c) => c.slug === city)?.name ?? city;

  return (
    <main
      style={{
        maxWidth: '900px',
        margin: '0 auto',
        padding: '2rem',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      }}
    >
      <h1 style={{ fontSize: '1.75rem', fontWeight: '700', color: '#333', marginBottom: '0.5rem' }}>
        {categoryName} in {cityName}
      </h1>

      <p style={{ color: '#666', marginBottom: '2rem' }}>
        {providers.length} provider{providers.length !== 1 ? 's' : ''} found
      </p>

      {providers.length === 0 ? (
        <div
          style={{
            textAlign: 'center',
            padding: '3rem',
            color: '#888',
            background: '#f9f9f9',
            borderRadius: '12px',
          }}
        >
          <p style={{ fontSize: '1.1rem' }}>No providers found in this category yet.</p>
          <p style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>Check back soon!</p>
        </div>
      ) : (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
            gap: '1rem',
          }}
        >
          {providers.map((provider) => (
            <a
              key={provider.id}
              href={`/${lang}/${city}/${category}/${provider.slug}-${provider.id}`}
              style={{
                display: 'block',
                padding: '1.25rem',
                background: '#ffffff',
                borderRadius: '12px',
                border: '1px solid #eee',
                boxShadow: '0 2px 8px rgba(0,0,0,0.05)',
                textDecoration: 'none',
                color: 'inherit',
                transition: 'box-shadow 0.2s',
              }}
            >
              <h2
                style={{
                  fontSize: '1.05rem',
                  fontWeight: '700',
                  color: '#333',
                  margin: '0 0 0.5rem 0',
                }}
              >
                {provider.business_name}
              </h2>

              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  fontSize: '0.9rem',
                  color: '#555',
                }}
              >
                <span>⭐ {provider.rating.toFixed(1)}</span>
                {provider.verified && (
                  <span
                    style={{
                      background: '#e8f5e9',
                      color: '#27ae60',
                      fontSize: '0.75rem',
                      fontWeight: '600',
                      padding: '2px 8px',
                      borderRadius: '999px',
                    }}
                  >
                    ✓ Verified
                  </span>
                )}
              </div>
            </a>
          ))}
        </div>
      )}
    </main>
  );
}
