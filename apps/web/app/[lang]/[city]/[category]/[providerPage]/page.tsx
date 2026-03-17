import LeadForm from '../../../../../../../components/LeadForm';
import { notFound } from 'next/navigation';

import { slugify } from '../../../../../lib/slugify';

type ProviderRouteParams = {
  lang: string;
  city: string;
  category: string;
  providerPage: string;
};

type ProviderPageParseResult = {
  slugPart: string;
  id: number;
};

const PROVIDER_PAGE_REGEX = /^(.*)-(\d+)$/;

const parseProviderPage = (providerPage: string): ProviderPageParseResult | null => {
  const match = providerPage.match(PROVIDER_PAGE_REGEX);
  if (!match) return null;
  const id = Number(match[2]);
  if (!Number.isFinite(id) || id <= 0) return null;
  const slugPart = match[1];
  if (!slugPart) return null;
  return { slugPart, id };
};

const normalizeCity = (value?: string) =>
  slugify((value ?? 'general').trim());

const normalizeCategory = (value?: string) =>
  slugify((value ?? 'general').trim());

const canonicalCategorySlug = (categoryKey?: string) =>
  slugify((categoryKey ?? '').replace(/^provider_category_/, ''));

const slugForProvider = (provider: {
  name: string;
  slug?: string | null;
}) => slugify(provider.slug || provider.name);

const routeMatchesProvider = (
  provider: {
    name: string;
    slug?: string | null;
    city?: string | null;
    category?: string;
    category_key: string;
  },
  params: {
    city: string;
    category: string;
    slugPart: string;
  }
) => {
  if (!provider) return false;

  const expectedCity = normalizeCity(provider.city ?? undefined);
  const expectedCategories = [
    normalizeCategory(provider.category || provider.category_key),
    canonicalCategorySlug(provider.category_key),
  ].filter(Boolean);
  const expectedSlug = slugForProvider(provider);

  return (
    params.city === expectedCity &&
    expectedCategories.includes(params.category) &&
    params.slugPart === expectedSlug
  );
};

const fetchProvider = async (id: number, lang: string) => {
  const res = await fetch(
    `http://127.0.0.1:8000/provider-info/${id}?lang=${encodeURIComponent(lang)}`,
    { cache: 'no-store' }
  );

  if (!res.ok) {
    throw new Error('Provider not found');
  }

  return res.json();
};

export async function generateMetadata(props: {
  params: Promise<ProviderRouteParams>;
}) {
  const params = await props.params;
  const { lang, city, category, providerPage } = params;
  const parsed = parseProviderPage(providerPage);
  if (!parsed) return { title: 'Nevumo' };

  try {
    const provider = await fetchProvider(parsed.id, lang);
    if (!routeMatchesProvider(provider, { city, category, slugPart: parsed.slugPart })) {
      return { title: 'Nevumo' };
    }

    return { title: `${provider.name} | ${provider.category} | Nevumo` };
  } catch {
    return { title: 'Nevumo' };
  }
}

export default async function Page(props: {
  params: Promise<ProviderRouteParams>;
}) {
  const params = await props.params;
  const { lang, city, category, providerPage } = params;
  const parsed = parseProviderPage(providerPage);
  if (!parsed) return notFound();

  try {
    const [providerRes, transRes] = await Promise.all([
      fetch(
        `http://127.0.0.1:8000/provider-info/${parsed.id}?lang=${encodeURIComponent(lang)}`,
        { cache: 'no-store' }
      ),
      fetch(`http://127.0.0.1:8000/translations/${lang}`, { cache: 'no-store' }),
    ]);

    if (!providerRes.ok) return notFound();

    const provider = await providerRes.json();
    if (
      !routeMatchesProvider(provider, {
        city,
        category,
        slugPart: parsed.slugPart,
      })
    ) {
      return notFound();
    }

    const translations = await transRes.json();

    return (
      <main>
        <LeadForm
          key={lang}
          initialProvider={provider}
          initialT={translations}
          currentLang={lang}
        />
      </main>
    );

  } catch {
    return <div>Грешка при зареждане.</div>;
  }
}
