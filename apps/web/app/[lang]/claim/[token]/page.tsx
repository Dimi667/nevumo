import { SUPPORTED_LANGUAGES } from '@/lib/locales';

interface PageProps {
  params: Promise<{ lang: string; token: string }>;
}

interface ProviderData {
  business_name: string;
  slug: string;
  is_claimed: boolean;
  city_name: string;
  category_slug: string;
}

interface ApiResponse {
  success: boolean;
  data?: ProviderData;
}

function getInitials(name: string): string {
  return name
    .split(' ')
    .slice(0, 2)
    .map(word => word[0]?.toUpperCase() || '')
    .join('');
}

async function fetchProviderByToken(token: string): Promise<ApiResponse> {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const response = await fetch(
      `${apiUrl}/api/v1/providers/by-claim-token/${token}`,
      { cache: 'no-store' }
    );

    if (!response.ok) {
      return { success: false };
    }

    return await response.json() as ApiResponse;
  } catch {
    return { success: false };
  }
}

export default async function ClaimPage({ params }: PageProps) {
  const { lang, token } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : 'en';

  const result = await fetchProviderByToken(token);
  const isValid = result.success && result.data && !result.data.is_claimed;

  return (
    <div className="bg-white">
      {/* TOP BAR */}
      <header className="border-b border-gray-200 bg-white">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center">
          <a href={`/${normalizedLang}`} className="flex items-center">
            <span className="text-2xl font-bold">
              <span className="text-orange-500">N</span>
              <span className="text-gray-900">evumo</span>
            </span>
          </a>
        </div>
      </header>

      {isValid && result.data ? (
        /* STATE A: Token valid */
        <main className="max-w-2xl mx-auto px-6 pt-6 pb-12">
          {/* HERO SECTION */}
          <div className="text-center">
            <span className="inline-block bg-orange-100 text-orange-700 text-sm font-medium px-4 py-1.5 rounded-full mb-4">
              Bezpłatna platforma dla specjalistów
            </span>
            <h1 className="text-3xl font-bold text-gray-900">
              Twoja firma jest już na Nevumo
            </h1>
            <p className="text-lg text-gray-600 mt-3">
              Odbierz profil dla {result.data.business_name} i zacznij otrzymywać zapytania od klientów w {result.data.city_name}.
            </p>
          </div>

          {/* PROVIDER CARD */}
          <div className="max-w-sm mx-auto mt-8 p-6 bg-white rounded-2xl shadow-md border border-gray-200">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 text-xl font-bold flex-shrink-0">
                {getInitials(result.data.business_name)}
              </div>
              <div>
                <h3 className="font-bold text-xl text-gray-900">
                  {result.data.business_name}
                </h3>
              </div>
            </div>

            <div className="flex flex-wrap gap-2 mt-4">
              <span className="bg-gray-100 text-gray-600 text-sm px-3 py-1 rounded-full">
                {result.data.city_name}
              </span>
              <span className="bg-orange-50 text-orange-600 text-sm px-3 py-1 rounded-full">
                {result.data.category_slug}
              </span>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-100 flex justify-around text-center">
              <div>
                <div className="text-lg font-bold text-gray-900">0</div>
                <div className="text-sm text-gray-500">opinii</div>
              </div>
              <div>
                <div className="text-lg font-bold text-gray-900">0</div>
                <div className="text-sm text-gray-500">zleceń</div>
              </div>
              <div>
                <span className="inline-block bg-green-100 text-green-700 text-xs font-medium px-2 py-1 rounded-full">
                  Nowy
                </span>
              </div>
            </div>
          </div>

          {/* VALUE PROPS */}
          <div className="mt-10 max-w-md mx-auto">
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <span className="text-orange-500 text-lg">✓</span>
                <span className="text-gray-700">Odbieraj zapytania od klientów bezpośrednio</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-orange-500 text-lg">✓</span>
                <span className="text-gray-700">Twój profil widoczny w Google</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-orange-500 text-lg">✓</span>
                <span className="text-gray-700">Bezpłatnie przez pierwsze 6 miesięcy</span>
              </li>
            </ul>
          </div>

          {/* CTA SECTION */}
          <div className="mt-10 text-center">
            <a
              href={`/${normalizedLang}/auth?mode=register&claim=${token}`}
              className="block max-w-sm mx-auto bg-orange-500 hover:bg-orange-600 text-white font-semibold py-4 rounded-xl text-lg transition-colors"
            >
              Odbierz mój profil bezpłatnie →
            </a>

            <p className="mt-3">
              <a
                href={`/${normalizedLang}/auth?mode=login&claim=${token}`}
                className="text-gray-500 text-sm hover:text-gray-700"
              >
                Masz już konto? Zaloguj się
              </a>
            </p>

            <p className="text-gray-400 text-xs mt-2">
              Bezpłatnie • Bez zobowiązań • Zajmuje 2 minuty
            </p>
          </div>
        </main>
      ) : (
        /* STATE B: Token invalid or already claimed */
        <main className="max-w-md mx-auto px-6 py-20 text-center">
          <div className="text-5xl mb-6">🔒</div>
          <h2 className="text-2xl font-bold text-gray-900">
            Ten link wygasł lub profil został już odebrany
          </h2>
          <p className="text-gray-500 mt-3">
            Jeśli to Twoja firma, możesz zarejestrować się bezpośrednio.
          </p>
          <a
            href={`/${normalizedLang}/auth?mode=register`}
            className="inline-block mt-8 bg-orange-500 hover:bg-orange-600 text-white font-semibold px-8 py-3 rounded-xl transition-colors"
          >
            Utwórz bezpłatny profil
          </a>
        </main>
      )}
    </div>
  );
}
