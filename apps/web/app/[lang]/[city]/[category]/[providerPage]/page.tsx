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

const PROVIDER_PAGE_REGEX = /^(.*)-(\d+)$/;

const parseProviderPage = (providerPage: string): { slugPart: string; id: number } | null => {
  const match = providerPage.match(PROVIDER_PAGE_REGEX);
  if (!match) return null;
  const id = Number(match[2]);
  if (!Number.isFinite(id) || id <= 0) return null;
  const slugPart = match[1];
  if (!slugPart) return null;
  return { slugPart, id };
};

export async function generateMetadata(props: { params: Promise<ProviderRouteParams> }) {
  const params = await props.params;
  const { lang, category, providerPage } = params;
  const parsed = parseProviderPage(providerPage);
  if (!parsed) return { title: 'Nevumo' };

  try {
    const [provider, categories] = await Promise.all([
      getProviderBySlug(parsed.slugPart),
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
  const parsed = parseProviderPage(providerPage);
  if (!parsed) return notFound();

  try {
    const [provider, transRes] = await Promise.all([
      getProviderBySlug(parsed.slugPart),
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
