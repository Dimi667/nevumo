import { cookies } from 'next/headers';
import { SUPPORTED_LANGUAGES } from '@/lib/locales';
import { generateHreflangAlternates } from '@/lib/seo';
import { fetchTranslations, t } from '@/lib/ui-translations';
import { Metadata } from 'next';
import { redirect } from 'next/navigation';

interface PageProps {
  params: Promise<{ lang: string; token: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { lang, token } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : 'en';
  const claimT = await fetchTranslations(normalizedLang, 'claim');

  const title = t(claimT, 'title', 'Claim your profile');
  const description = t(claimT, 'description', 'Claim this profile and start receiving client requests for free.');

  return {
    title,
    description,
    alternates: {
      canonical: `/${normalizedLang}/claim/${token}`,
      languages: generateHreflangAlternates(`/claim/${token}`),
    },
    robots: { index: false, follow: true },
  };
}

interface ProviderData {
  business_name: string;
  slug: string;
  is_claimed: boolean;
  city_name: string;
  category_slug: string;
  data_source: string;
}

interface ApiResponse {
  success: boolean;
  data?: ProviderData;
  error?: { code: string; message: string };
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
    const apiUrl = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
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

async function claimProfile(token: string, authToken: string): Promise<{ success: boolean; error?: string }> {
  try {
    const apiUrl = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/api/v1/providers/claim/${token}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return { 
        success: false, 
        error: errorData?.detail?.message || errorData?.detail || 'Claim failed' 
      };
    }

    return { success: true };
  } catch {
    return { success: false, error: 'Network error' };
  }
}

export default async function ClaimPage({ params }: PageProps) {
  const { lang, token } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : 'en';
  const claimT = await fetchTranslations(normalizedLang, 'claim');

  // Check auth status via cookie
  const cookieStore = await cookies();
  const authToken = cookieStore.get('nevumo_auth_token')?.value;
  const isAuthenticated = !!authToken;

  const result = await fetchProviderByToken(token);
  const isValid = result.success && result.data && !result.data.is_claimed;

  // Handle claim action if authenticated and form submitted
  // Note: In a real implementation, this would be a server action or form handler
  // For now, we'll render the page with the appropriate state

  return (
    <div className="bg-white">
      {isValid && result.data ? (
        /* STATE A: Token valid and not claimed */
        <main className="max-w-2xl mx-auto px-6 pt-6 pb-12">
          {/* HERO SECTION */}
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900">
              {t(claimT, 'subtitle', 'Is this your business on Nevumo?')}
            </h1>
            <p className="text-lg text-gray-600 mt-3">
              {t(claimT, 'description', 'Claim this profile and start receiving client requests for free.')}
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
                {t(claimT, 'category_label', 'Category')}: {result.data.category_slug}
              </span>
              <span className="bg-orange-50 text-orange-600 text-sm px-3 py-1 rounded-full">
                {t(claimT, 'city_label', 'City')}: {result.data.city_name}
              </span>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-100 flex justify-around text-center">
              <div>
                <div className="text-lg font-bold text-gray-900">0</div>
                <div className="text-sm text-gray-500">reviews</div>
              </div>
              <div>
                <div className="text-lg font-bold text-gray-900">0</div>
                <div className="text-sm text-gray-500">jobs</div>
              </div>
              <div>
                <span className="inline-block bg-green-100 text-green-700 text-xs font-medium px-2 py-1 rounded-full">
                  New
                </span>
              </div>
            </div>
          </div>

          {/* CTA SECTION */}
          <div className="mt-10 text-center">
            {isAuthenticated ? (
              /* Authenticated: Show claim button */
              <form action={async () => {
                'use server';
                const claimResult = await claimProfile(token, authToken);
                if (claimResult.success) {
                  redirect(`/${normalizedLang}/provider/dashboard`);
                }
                // On error, we'd ideally show an error state
                // For now, redirect back with error query param
                redirect(`/${normalizedLang}/claim/${token}?error=claim_failed`);
              }}>
                <button
                  type="submit"
                  className="block max-w-sm mx-auto w-full bg-orange-500 hover:bg-orange-600 text-white font-semibold py-4 rounded-xl text-lg transition-colors"
                >
                  {t(claimT, 'cta_claim', 'Claim your profile for free')}
                </button>
              </form>
            ) : (
              /* Not authenticated: Show login/register buttons */
              <div className="space-y-3">
                <a
                  href={`/${normalizedLang}/auth/login?redirect=/${normalizedLang}/claim/${token}`}
                  className="block max-w-sm mx-auto bg-orange-500 hover:bg-orange-600 text-white font-semibold py-4 rounded-xl text-lg transition-colors text-center"
                >
                  {t(claimT, 'cta_login', 'Log in to claim this profile')}
                </a>

                <a
                  href={`/${normalizedLang}/auth/register?redirect=/${normalizedLang}/claim/${token}&intent=provider`}
                  className="block max-w-sm mx-auto bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-4 rounded-xl text-lg transition-colors text-center"
                >
                  {t(claimT, 'cta_register', 'Register and claim this profile for free')}
                </a>
              </div>
            )}
          </div>
        </main>
      ) : (
        /* STATE B: Token invalid or already claimed */
        <main className="max-w-md mx-auto px-6 py-20 text-center">
          <div className="text-5xl mb-6">🔒</div>
          <h2 className="text-2xl font-bold text-gray-900">
            {result.data?.is_claimed 
              ? t(claimT, 'already_claimed', 'This profile has already been claimed.')
              : t(claimT, 'not_found', 'This profile was not found or has already been claimed.')
            }
          </h2>
          <a
            href={`/${normalizedLang}/auth/register?intent=provider`}
            className="inline-block mt-8 bg-orange-500 hover:bg-orange-600 text-white font-semibold px-8 py-3 rounded-xl transition-colors"
          >
            {t(claimT, 'cta_register', 'Register and claim this profile for free')}
          </a>
        </main>
      )}
    </div>
  );
}
