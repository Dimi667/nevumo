import Link from 'next/link';
import Image from 'next/image';
import type { Metadata } from 'next';
import { getProviderBySlug, getProviders } from '@/lib/api';
import { generateHreflangAlternates } from '@/lib/seo';
import { JsonLd } from '@/components/JsonLd';
import LeadForm from '@/components/category/LeadForm';

interface PageProps {
  params: Promise<{ lang: string; city: string; category: string }>;
}

type CategoryKey = 'masaz' | 'sprzatanie' | 'hydraulik';
type ApiCategorySlug = 'massage' | 'cleaning' | 'plumbing';

interface CategoryContent {
  apiSlug: ApiCategorySlug;
  displayName: string;
  heading: string;
  subtitle: string;
  metadataTitle: string;
  metadataDescription: string;
  seoTitle: string;
  seoParagraphs: [string, string, string];
  seoQuestions: [string, string];
  relatedLinks: Array<{ href: string; label: string }>;
  faq: Array<{ question: string; answer: string }>;
}

interface EnrichedProvider {
  id: string;
  slug: string;
  businessName: string;
  rating: number;
  profileImageUrl: string | null;
  description: string | null;
  jobsCompleted: number;
  latestLeadPreviewCreatedAt: string | null;
}

function getInitials(name: string): string {
  return name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part.charAt(0).toUpperCase())
    .join('');
}

function ProviderCard({
  provider,
  href,
}: {
  provider: EnrichedProvider;
  href: string;
}) {
  const latestLeadTime = provider.latestLeadPreviewCreatedAt
    ? formatRelativeTime(provider.latestLeadPreviewCreatedAt)
    : null;

  return (
    <article className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
      <div className="flex items-start gap-4">
        <Link href={href} className="shrink-0">
          <div className="flex h-16 w-16 items-center justify-center overflow-hidden rounded-full bg-orange-100 text-lg font-bold text-orange-600">
            {provider.profileImageUrl ? (
              <img
                src={provider.profileImageUrl}
                alt={provider.businessName}
                className="h-full w-full object-cover"
              />
            ) : (
              <span>{getInitials(provider.businessName)}</span>
            )}
          </div>
        </Link>

        <div className="min-w-0 flex-1">
          <Link href={href} className="block">
            <h2 className="text-lg font-bold text-gray-900 transition hover:text-orange-600">
              {provider.businessName}
            </h2>
          </Link>

          {provider.rating > 0 && (
            <div className="mt-1 flex items-center gap-2 text-sm font-medium text-amber-600">
              <span>⭐⭐⭐⭐⭐</span>
              <span>{provider.rating.toFixed(1)}</span>
            </div>
          )}

          <p className="mt-3 line-clamp-2 text-sm leading-6 text-gray-600">
            {provider.description ?? 'Sprawdzony specjalista dostępny w Warszawie. Wyślij krótkie zapytanie i poczekaj na kontakt.'}
          </p>

          <div className="mt-4 flex flex-wrap gap-2 text-xs font-medium text-gray-600">
            {provider.jobsCompleted > 0 && (
              <span className="rounded-full bg-gray-50 px-3 py-1.5">
                ✔ {provider.jobsCompleted} wykonanych zleceń
              </span>
            )}
            {latestLeadTime && (
              <span className="rounded-full bg-gray-50 px-3 py-1.5">
                ✔ Ostatnie zapytanie: {latestLeadTime}
              </span>
            )}
            <span className="rounded-full bg-gray-50 px-3 py-1.5">
              ✔ Bezpośredni kontakt
            </span>
          </div>

          <a
            href="#lead-form"
            className="mt-5 inline-flex w-full items-center justify-center rounded-xl bg-orange-500 px-4 py-3 text-sm font-semibold text-white transition hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-offset-2"
          >
            Wyślij zapytanie
          </a>
        </div>
      </div>
    </article>
  );
}

const CATEGORY_CONTENT: Record<CategoryKey, CategoryContent> = {
  masaz: {
    apiSlug: 'massage',
    displayName: 'masaż',
    heading: 'Masaż w Warszawie',
    subtitle:
      'Znajdź sprawdzonych masażystów w Warszawie. Bezpłatne zapytanie, bez zobowiązań.',
    metadataTitle: 'Masaż w Warszawie — znajdź specjalistę | Nevumo',
    metadataDescription:
      'Znajdź sprawdzonych masażystów w Warszawie. Bezpłatne zapytanie, bez zobowiązań. Odpowiedź nawet w 30 minut.',
    seoTitle: 'Masaż w Warszawie — co warto wiedzieć?',
    seoParagraphs: [
      'Warszawa oferuje szeroki wybór profesjonalnych masażystów. Niezależnie od tego, czy szukasz masażu relaksacyjnego, sportowego czy terapeutycznego, na Nevumo znajdziesz sprawdzonych specjalistów w swojej okolicy.',
      'Sprawdź opinie poprzednich klientów, doświadczenie specjalisty oraz zakres oferowanych usług. Dobry masażysta dostosuje technikę do Twoich potrzeb.',
      'Ceny masażu w Warszawie zaczynają się od około 100 zł za godzinę. Koszt zależy od rodzaju masażu, doświadczenia specjalisty i lokalizacji.',
    ],
    seoQuestions: ['Jak wybrać masażystę?', 'Ile kosztuje masaż w Warszawie?'],
    relatedLinks: [
      { href: '/pl/warszawa/sprzatanie', label: 'Sprzątanie w Warszawie' },
      { href: '/pl/warszawa/hydraulik', label: 'Hydraulik w Warszawie' },
    ],
    faq: [
      {
        question: 'Jak znaleźć masażystę w Warszawie?',
        answer:
          'Na Nevumo możesz bezpłatnie wysłać zapytanie do sprawdzonych masażystów w Warszawie i otrzymać odpowiedź nawet w 30 minut.',
      },
      {
        question: 'Ile kosztuje masaż w Warszawie?',
        answer:
          'Ceny masażu w Warszawie zaczynają się od około 100 zł za godzinę, w zależności od rodzaju masażu i doświadczenia specjalisty.',
      },
      {
        question: 'Czy zapytanie jest bezpłatne?',
        answer:
          'Tak, wysłanie zapytania przez Nevumo jest całkowicie bezpłatne i bez zobowiązań.',
      },
    ],
  },
  sprzatanie: {
    apiSlug: 'cleaning',
    displayName: 'sprzątanie',
    heading: 'Sprzątanie w Warszawie',
    subtitle:
      'Znajdź sprawdzonych specjalistów od sprzątania w Warszawie. Bezpłatne zapytanie, bez zobowiązań.',
    metadataTitle: 'Sprzątanie w Warszawie — znajdź specjalistę | Nevumo',
    metadataDescription:
      'Znajdź sprawdzone firmy sprzątające w Warszawie. Bezpłatne zapytanie, bez zobowiązań.',
    seoTitle: 'Sprzątanie w Warszawie — co warto wiedzieć?',
    seoParagraphs: [
      'Profesjonalne firmy sprzątające w Warszawie oferują kompleksowe usługi dla domów, mieszkań i biur. Na Nevumo znajdziesz sprawdzonych specjalistów dostępnych na terenie całej Warszawy.',
      'Zwróć uwagę na opinie klientów, zakres usług oraz elastyczność terminów. Najlepsze firmy oferują stałą współpracę z rabatem.',
      'Standardowe sprzątanie mieszkania w Warszawie kosztuje od 150 do 300 zł, w zależności od metrażu i zakresu prac.',
    ],
    seoQuestions: ['Jak wybrać firmę sprzątającą?', 'Ile kosztuje sprzątanie w Warszawie?'],
    relatedLinks: [
      { href: '/pl/warszawa/masaz', label: 'Masaż w Warszawie' },
      { href: '/pl/warszawa/hydraulik', label: 'Hydraulik w Warszawie' },
    ],
    faq: [
      {
        question: 'Jak znaleźć firmę sprzątającą w Warszawie?',
        answer:
          'Na Nevumo możesz bezpłatnie wysłać zapytanie do sprawdzonych firm sprzątających w Warszawie i szybko otrzymać odpowiedzi od dostępnych specjalistów.',
      },
      {
        question: 'Ile kosztuje sprzątanie w Warszawie?',
        answer:
          'Standardowe sprzątanie mieszkania w Warszawie kosztuje zwykle od 150 do 300 zł, zależnie od metrażu i zakresu usług.',
      },
      {
        question: 'Czy zapytanie jest bezpłatne?',
        answer:
          'Tak, wysłanie zapytania przez Nevumo jest całkowicie bezpłatne i bez zobowiązań.',
      },
    ],
  },
  hydraulik: {
    apiSlug: 'plumbing',
    displayName: 'hydraulik',
    heading: 'Hydraulik w Warszawie',
    subtitle:
      'Znajdź sprawdzonego hydraulika w Warszawie. Bezpłatne zapytanie, bez zobowiązań.',
    metadataTitle: 'Hydraulik w Warszawie — znajdź specjalistę | Nevumo',
    metadataDescription:
      'Znajdź sprawdzonego hydraulika w Warszawie. Szybka odpowiedź, bezpłatne zapytanie.',
    seoTitle: 'Hydraulik w Warszawie — co warto wiedzieć?',
    seoParagraphs: [
      'Awaria hydrauliczna wymaga szybkiej reakcji. Na Nevumo znajdziesz sprawdzonych hydraulików w Warszawie, dostępnych nawet w trybie pilnym. Bezpłatne zapytanie, szybka odpowiedź.',
      'Hydraulika wzywamy przy awariach instalacji wodnej, cieknących kranach, zatkanej kanalizacji oraz podczas remontu łazienki lub kuchni.',
      'Stawki hydraulików w Warszawie zaczynają się od 100-150 zł za roboczogodzinę. Cena zależy od rodzaju awarii i czasu realizacji.',
    ],
    seoQuestions: ['Kiedy wezwać hydraulika?', 'Ile kosztuje hydraulik w Warszawie?'],
    relatedLinks: [
      { href: '/pl/warszawa/masaz', label: 'Masaż w Warszawie' },
      { href: '/pl/warszawa/sprzatanie', label: 'Sprzątanie w Warszawie' },
    ],
    faq: [
      {
        question: 'Jak znaleźć hydraulika w Warszawie?',
        answer:
          'Na Nevumo możesz bezpłatnie wysłać zapytanie do sprawdzonych hydraulików w Warszawie i otrzymać odpowiedź nawet w krótkim czasie.',
      },
      {
        question: 'Ile kosztuje hydraulik w Warszawie?',
        answer:
          'Stawki hydraulików w Warszawie zaczynają się zwykle od 100-150 zł za roboczogodzinę, zależnie od rodzaju awarii i terminu realizacji.',
      },
      {
        question: 'Czy zapytanie jest bezpłatne?',
        answer:
          'Tak, wysłanie zapytania przez Nevumo jest całkowicie bezpłatne i bez zobowiązań.',
      },
    ],
  },
};

function getCategoryContent(category: string): CategoryContent {
  return CATEGORY_CONTENT[(category as CategoryKey)] ?? CATEGORY_CONTENT.masaz;
}

function formatRelativeTime(dateString: string): string {
  const diffMs = Date.now() - new Date(dateString).getTime();
  const diffMinutes = Math.max(1, Math.round(diffMs / 60000));

  if (diffMinutes < 60) {
    return `${diffMinutes} min temu`;
  }

  const diffHours = Math.round(diffMinutes / 60);
  if (diffHours < 24) {
    return `${diffHours} godz. temu`;
  }

  const diffDays = Math.round(diffHours / 24);
  return `${diffDays} dni temu`;
}

function buildFaqJsonLd(content: CategoryContent): Record<string, unknown> {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: content.faq.map((item) => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: item.answer,
      },
    })),
  };
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { city, category } = await params;
  const content = getCategoryContent(category);

  return {
    title: content.metadataTitle,
    description: content.metadataDescription,
    alternates: {
      languages: generateHreflangAlternates(`/${city}/${category}`),
    },
    openGraph: {
      title: content.metadataTitle,
      description: content.metadataDescription,
    },
  };
}

async function getEnrichedProviders(
  lang: string,
  city: string,
  category: string,
): Promise<{ allCount: number; providers: EnrichedProvider[]; averageRating: number }> {
  const listItems = await getProviders(category, city, lang);

  const details = await Promise.all(
    listItems.map(async (provider) => {
      const detail = await getProviderBySlug(provider.slug, lang, city);
      return {
        id: provider.id,
        slug: provider.slug,
        businessName: provider.business_name,
        rating: detail?.rating ?? provider.rating,
        profileImageUrl: detail?.profile_image_url ?? null,
        description: detail?.description ?? null,
        jobsCompleted: detail?.jobs_completed ?? 0,
        latestLeadPreviewCreatedAt: detail?.latest_lead_preview?.created_at ?? null,
      } satisfies EnrichedProvider;
    }),
  );

  const ratedProviders = listItems.filter((provider) => provider.rating > 0);
  const averageRating = ratedProviders.length > 0
    ? ratedProviders.reduce((sum, provider) => sum + provider.rating, 0) / ratedProviders.length
    : 4.8;

  return {
    allCount: listItems.length,
    providers: details,
    averageRating,
  };
}

export default async function CategoryPage({ params }: PageProps) {
  const { lang, city, category } = await params;
  const content = getCategoryContent(category);

  const { providers, allCount, averageRating } = await getEnrichedProviders(lang, city, content.apiSlug);
  const visibleProviders = providers.slice(0, 20);
  const hiddenProviders = providers.slice(20);
  const hiddenCount = hiddenProviders.length;
  const trustSpecialistsText = allCount > 0 ? `${allCount} specjalistów` : '14 specjalistów';
  const trustRatingText = `${averageRating.toFixed(1)} ocena`;
  const trustLeadsText = '120 zapytań w tym miesiącu';
  const faqJsonLd = buildFaqJsonLd(content);

  return (
    <>
      <JsonLd data={faqJsonLd} />
      <div className="min-h-screen bg-white text-gray-900">
        <header className="border-b border-orange-100 bg-white/90 backdrop-blur">
          <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
            <Link href={`/${lang}`} className="inline-flex items-center">
              <Image src="/Nevumo_logo.svg" alt="Nevumo" width={120} height={36} priority />
            </Link>
            <Link href={`/${lang}`} className="text-sm font-semibold text-gray-700 transition hover:text-orange-600">
              Zostań specjalistą
            </Link>
          </div>
        </header>

        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 lg:py-12">
          <section className="mb-8">
            <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              {content.heading}
            </h1>
            <p className="mt-3 max-w-3xl text-base text-gray-600 sm:text-lg">
              {content.subtitle}
            </p>
            <div className="mt-5 inline-flex flex-wrap items-center gap-x-3 gap-y-2 rounded-full bg-gray-50 px-4 py-3 text-sm text-gray-700">
              <span>{trustSpecialistsText}</span>
              <span className="text-gray-400">•</span>
              <span className="flex items-center gap-1">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" className="text-orange-400">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                {trustRatingText}
              </span>
              <span className="text-gray-400">•</span>
              <span>{trustLeadsText}</span>
              <span className="text-gray-400">•</span>
              <span className="flex items-center gap-1">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" className="text-orange-400">
                  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                </svg>
                Średni czas odpowiedzi: ~30 min
              </span>
            </div>
          </section>

          <section className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_20rem] lg:items-start">
            <div className="space-y-4">
              {providers.length === 0 ? (
                <div className="rounded-xl border border-gray-100 bg-white px-6 py-12 text-center shadow-sm">
                  <p className="text-base font-medium text-gray-700">
                    Pierwsi specjaliści już dołączają. Sprawdź ponownie jutro.
                  </p>
                </div>
              ) : (
                <>
                  {visibleProviders.map((provider) => {
                    const providerHref = `/${lang}/${city}/${category}/${provider.slug}`;
                    return <ProviderCard key={provider.id} provider={provider} href={providerHref} />;
                  })}
                  {hiddenCount > 0 && (
                    <details className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
                      <summary className="cursor-pointer list-none text-center text-sm font-semibold text-orange-600">
                        Pokaż więcej
                      </summary>
                      <div className="mt-4 space-y-4">
                        {hiddenProviders.map((provider) => {
                          const providerHref = `/${lang}/${city}/${category}/${provider.slug}`;
                          return <ProviderCard key={provider.id} provider={provider} href={providerHref} />;
                        })}
                      </div>
                    </details>
                  )}
                </>
              )}
              <section className="mt-8 rounded-xl bg-gray-50 p-6 sm:p-8">
                <h2 className="text-2xl font-bold text-gray-900">{content.seoTitle}</h2>
                <p className="mt-4 text-base leading-7 text-gray-700">{content.seoParagraphs[0]}</p>
                <h3 className="mt-6 text-xl font-semibold text-gray-900">{content.seoQuestions[0]}</h3>
                <p className="mt-3 text-base leading-7 text-gray-700">{content.seoParagraphs[1]}</p>
                <h3 className="mt-6 text-xl font-semibold text-gray-900">{content.seoQuestions[1]}</h3>
                <p className="mt-3 text-base leading-7 text-gray-700">{content.seoParagraphs[2]}</p>
                <div className="mt-6 flex flex-wrap items-center gap-2 text-sm text-gray-700">
                  <span>Sprawdź również:</span>
                  {content.relatedLinks.map((link, index) => (
                    <span key={link.href}>
                      <Link href={link.href} className="font-medium text-orange-600 underline underline-offset-2">
                        {link.label}
                      </Link>
                      {index < content.relatedLinks.length - 1 ? <span className="ml-2 text-gray-400">•</span> : null}
                    </span>
                  ))}
                </div>
              </section>
            </div>

            <aside className="lg:sticky lg:top-6">
              <div id="lead-form" className="rounded-xl border border-orange-100 bg-white p-6 shadow-lg">
                <h2 className="text-xl font-bold text-gray-900">Wyślij zapytanie</h2>
                <p className="mt-1 text-sm text-gray-500">Bezpłatnie • Bez zobowiązań</p>
                <div className="mt-5">
                  <LeadForm categorySlug={content.apiSlug} citySlug="warszawa" />
                </div>
              </div>
            </aside>
          </section>

          <section className="mt-12 rounded-xl bg-gray-50 border-t border-gray-200 px-6 py-8 text-center">
            <p className="text-sm text-gray-500">Oferujesz {content.displayName} w Warszawie?</p>
            <Link href={`/${lang}`} className="mt-2 inline-block text-sm font-semibold text-orange-500 hover:text-orange-600 underline underline-offset-2">
              Dołącz za darmo →
            </Link>
          </section>
        </main>
      </div>
    </>
  );
}
