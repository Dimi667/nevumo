import LeadForm from '@/components/LeadForm';
import { notFound } from 'next/navigation';
import { getProviderBySlug, getCategories } from '@/lib/api';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

type ProviderRouteParams = {
  lang: string;
  city: string;
  category: string;
  providerPage: string;
};

export async function generateMetadata(props: { params: Promise<ProviderRouteParams> }) {
  const params = await props.params;
  const { lang, category, providerPage } = params;

  try {
    const [provider, categories] = await Promise.all([
      getProviderBySlug(providerPage),
      getCategories(lang),
    ]);
    if (!provider) return { title: 'Nevumo' };

    const categoryName = categories.find((c) => c.slug === category)?.name ?? category;
    return { title: `${provider.business_name} | ${categoryName} | Nevumo` };
  } catch {
    return { title: 'Nevumo' };
  }
}

export default async function Page(props: { params: Promise<ProviderRouteParams> }) {
  const params = await props.params;
  const { lang, city, category, providerPage } = params;

  try {
    const [provider, transRes] = await Promise.all([
      getProviderBySlug(providerPage),
      fetch(`${API_BASE}/translations/${lang}`, { cache: 'no-store' }),
    ]);

    if (!provider) return notFound();

    const translations: Record<string, string> = transRes.ok ? await transRes.json() : {};

    return (
      <main>
        <LeadForm
          key={lang}
          initialProvider={provider}
          initialT={translations}
          currentLang={lang}
          categorySlug={category}
          citySlug={city}
        />
      </main>
    );
  } catch {
    return <div>Error loading provider.</div>;
  }
}
