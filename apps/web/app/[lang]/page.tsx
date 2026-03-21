import { getCategories, getCities } from '@/lib/api';
import { SUPPORTED_LANGUAGES } from '@/lib/locales';

interface PageProps {
  params: Promise<{ lang: string }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { lang } = await params;
  return {
    title: `Nevumo — Find local service providers`,
    description: `Browse service categories and find trusted providers near you.`,
    alternates: {
      languages: Object.fromEntries(
        SUPPORTED_LANGUAGES.map((l) => [l, `/${l}`]),
      ),
    },
  };
}

export default async function LangLanding({ params }: PageProps) {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : 'en';

  const [categories, cities] = await Promise.all([
    getCategories(normalizedLang),
    getCities('BG'),
  ]);

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
        Nevumo
      </h1>
      <p style={{ color: '#666', marginBottom: '2rem' }}>
        Find trusted service providers near you.
      </p>

      {cities.length > 0 && categories.length > 0 ? (
        <div>
          {cities.map((city) => (
            <section key={city.slug} style={{ marginBottom: '2rem' }}>
              <h2 style={{ fontSize: '1.2rem', fontWeight: '600', color: '#444', marginBottom: '0.75rem' }}>
                {city.name}
              </h2>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {categories.map((cat) => (
                  <a
                    key={cat.slug}
                    href={`/${normalizedLang}/${city.slug}/${cat.slug}`}
                    style={{
                      padding: '0.5rem 1rem',
                      background: '#ffffff',
                      border: '1px solid #ddd',
                      borderRadius: '8px',
                      textDecoration: 'none',
                      color: '#333',
                      fontSize: '0.9rem',
                      fontWeight: '500',
                    }}
                  >
                    {cat.name}
                  </a>
                ))}
              </div>
            </section>
          ))}
        </div>
      ) : (
        <p style={{ color: '#888' }}>No categories available yet.</p>
      )}
    </main>
  );
}
