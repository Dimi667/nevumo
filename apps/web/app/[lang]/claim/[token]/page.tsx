import { cookies } from 'next/headers';
import { SUPPORTED_LANGUAGES } from '@/lib/locales';
import { generateHreflangAlternates } from '@/lib/seo';
import { fetchTranslations, t } from '@/lib/ui-translations';
import { Metadata } from 'next';
import { redirect } from 'next/navigation';
import Link from 'next/link';

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
  id: string;
  business_name: string;
  category_slug: string | null;
  city_slug: string | null;
  city_name: string;
  claimed_count: number;
  is_claimed: boolean;
  data_source: string | null;
}

function getInitials(name: string): string {
  return name
    .split(' ')
    .slice(0, 2)
    .map(word => word[0]?.toUpperCase() || '')
    .join('');
}

async function fetchProviderByToken(token: string, lang: string): Promise<ProviderData | null> {
  try {
    const apiUrl = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const response = await fetch(
      `${apiUrl}/api/v1/providers/by-claim-token/${token}?lang=${lang}`,
      { cache: 'no-store' }
    );

    if (!response.ok) {
      return null;
    }

    return await response.json() as ProviderData;
  } catch {
    return null;
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

  const result = await fetchProviderByToken(token, normalizedLang);

  // STATE 1: not_found (404 from API)
  if (!result) {
    return (
      <div className="min-h-screen bg-white">
        <main className="max-w-md mx-auto px-6 py-20 text-center">
          <div className="text-5xl mb-6">🔗</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            {t(claimT, 'notfound_title', 'Link not found')}
          </h2>
          <p className="text-gray-600 mb-6">
            {t(claimT, 'notfound_desc', 'This claim link is invalid or has expired.')}
          </p>
          <div className="bg-gray-50 rounded-lg p-4 mb-6 text-sm text-gray-600">
            {t(claimT, 'notfound_support', 'Need help? Contact our support team.')}
          </div>
          <Link
            href={`/${normalizedLang}/auth/register?intent=provider`}
            className="inline-block bg-orange-500 hover:bg-orange-600 text-white font-semibold py-3 px-6 rounded-xl transition-colors"
          >
            {t(claimT, 'notfound_cta', 'Register as a provider')}
          </Link>
          <div className="mt-4">
            <Link
              href={`/${normalizedLang}`}
              className="text-gray-500 hover:text-gray-700 text-sm"
            >
              {t(claimT, 'notfound_ghost', 'Back to homepage')}
            </Link>
          </div>
        </main>
      </div>
    );
  }

  // STATE 2: already_claimed
  if (result.is_claimed) {
    return (
      <div className="min-h-screen bg-white">
        <main className="max-w-md mx-auto px-6 py-20 text-center">
          <div className="text-5xl mb-6">✓</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            {t(claimT, 'claimed_title', 'Profile already claimed')}
          </h2>
          <p className="text-gray-600 mb-6">
            {t(claimT, 'claimed_desc', 'This profile has already been claimed by another user.')}
          </p>
          <Link
            href={`/${normalizedLang}/auth/login`}
            className="inline-block bg-orange-500 hover:bg-orange-600 text-white font-semibold py-3 px-6 rounded-xl transition-colors"
          >
            {t(claimT, 'claimed_cta', 'Log in to your account')}
          </Link>
          <div className="mt-6 bg-gray-50 rounded-lg p-4 text-sm text-gray-600">
            {t(claimT, 'claimed_support', 'If you believe this is an error, please contact support.')}
          </div>
        </main>
      </div>
    );
  }

  // STATE 3: valid unclaimed (main state)
  const { business_name, category_slug, city_name, claimed_count } = result;

  // Social proof logic
  const socialProof = claimed_count === 0
    ? t(claimT, 'social_proof_zero', 'Be the first provider in {city} to claim your profile!').replace('{city}', city_name)
    : claimed_count < 10
    ? t(claimT, 'social_proof_few', '{count} providers in {city} have already claimed their profiles')
        .replace('{count}', String(claimed_count))
        .replace('{city}', city_name)
    : t(claimT, 'social_proof_many', '{count}+ providers in {city} trust Nevumo')
        .replace('{count}', String(claimed_count))
        .replace('{city}', city_name);

  return (
    <div className="min-h-screen bg-white pb-20 sm:pb-0">
      {/* URGENCY BAR */}
      <div className="bg-amber-100 border-b border-amber-200">
        <div className="max-w-7xl mx-auto px-6 py-2 text-center text-sm text-amber-800">
          {t(claimT, 'urgency', '⚡ Limited time: Claim your profile before competitors do')}
        </div>
      </div>

      {/* CONTENT */}
      <main className="max-w-[520px] mx-auto px-6 py-12">
        {/* Free badge pill */}
        <div className="flex justify-center mb-4">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full
                   bg-green-50 text-green-700 text-sm font-medium
                   border border-green-200">
            ✓ {t(claimT, 'free_badge', 'Free for providers')}
          </span>
        </div>

        {/* Hero title */}
        <h1 className="text-3xl font-bold text-gray-900 text-center mb-8">
          {t(claimT, 'hero_title', 'Claim your business profile on Nevumo')}
        </h1>

        {/* Provider card */}
        <div className="border-2 border-orange-500 rounded-2xl p-6 mb-8 relative">
          <div className="absolute top-4 right-4 bg-orange-100 text-orange-600 text-xs font-medium px-2 py-1 rounded-full">
            {t(claimT, 'your_profile_badge', 'Your profile')}
          </div>
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 text-xl font-bold flex-shrink-0">
              {getInitials(business_name)}
            </div>
            <div>
              <h3 className="font-bold text-xl text-gray-900">
                {business_name}
              </h3>
              <div className="flex items-center gap-2 mt-1 text-sm text-gray-600">
                <span>🏷️</span>
                <span>{category_slug || 'N/A'}</span>
                <span className="text-gray-300">•</span>
                <span>📍</span>
                <span>{city_name}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Primary CTA (top) */}
        <div id="cta-top" className="hidden sm:block mb-8">
          {isAuthenticated ? (
            <form action={async () => {
              'use server';
              const claimResult = await claimProfile(token, authToken);
              if (claimResult.success) {
                redirect(`/${normalizedLang}/provider/dashboard`);
              }
              redirect(`/${normalizedLang}/claim/${token}?error=claim_failed`);
            }}>
              <button
                type="submit"
                className="w-full bg-orange-500 hover:bg-orange-600 text-white font-semibold py-4 rounded-xl text-lg transition-colors"
              >
                {t(claimT, 'cta_claim', 'Claim your profile for free')}
              </button>
            </form>
          ) : (
            <Link
              href={`/${normalizedLang}/auth/register?redirect=/${normalizedLang}/claim/${token}&intent=provider`}
              className="block w-full bg-orange-500 hover:bg-orange-600 text-white font-semibold py-4 rounded-xl text-lg transition-colors text-center"
            >
              {t(claimT, 'cta_register', 'Register and claim this profile for free')}
            </Link>
          )}
        </div>

        {/* Leads teaser */}
        <div className="bg-gray-50 rounded-2xl p-6 mb-8 relative overflow-hidden">
          <h3 className="font-semibold text-gray-900 mb-4">
            {t(claimT, 'leads_title', 'Recent client requests in your area')}
          </h3>
          <div className="space-y-3">
            <div className="bg-white rounded-lg p-3">
              <div className="h-3 bg-gray-200 rounded w-3/4 mb-2 blur-sm"></div>
              <div className="h-2 bg-gray-100 rounded w-1/2 blur-sm"></div>
              <div className="text-xs text-gray-400 mt-2">преди 3 мин</div>
            </div>
            <div className="bg-white rounded-lg p-3">
              <div className="h-3 bg-gray-200 rounded w-2/3 mb-2 blur-sm"></div>
              <div className="h-2 bg-gray-100 rounded w-1/3 blur-sm"></div>
              <div className="text-xs text-gray-400 mt-2">преди 41 мин</div>
            </div>
          </div>
          {/* Overlay */}
          <div className="absolute inset-0 bg-white/80 backdrop-blur-sm flex flex-col items-center justify-center">
            <div className="text-4xl mb-2">🔒</div>
            <p className="font-semibold text-gray-900 text-center">
              {t(claimT, 'leads_overlay', 'Claim to see client requests')}
            </p>
          </div>
        </div>

        {/* Benefits grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8 [&>*]:min-w-0">
          <div className="bg-gray-50 rounded-xl p-4 text-center">
            <div className="text-2xl mb-2">💰</div>
            <h4 className="font-semibold text-gray-900 text-sm mb-1">
              {t(claimT, 'benefit_1_title', 'No commission')}
            </h4>
            <p className="text-xs text-gray-600">
              {t(claimT, 'benefit_1_sub', 'Keep 100% of earnings')}
            </p>
          </div>
          <div className="bg-gray-50 rounded-xl p-4 text-center">
            <div className="text-2xl mb-2">⚡</div>
            <h4 className="font-semibold text-gray-900 text-sm mb-1">
              {t(claimT, 'benefit_2_title', 'Instant leads')}
            </h4>
            <p className="text-xs text-gray-600">
              {t(claimT, 'benefit_2_sub', 'Get requests immediately')}
            </p>
          </div>
          <div className="border-2 border-orange-500 rounded-xl p-4 text-center bg-orange-50">
            <div className="text-2xl mb-2">🎯</div>
            <h4 className="font-semibold text-orange-600 text-sm mb-1">
              {t(claimT, 'benefit_3_title', 'Targeted clients')}
            </h4>
            <p className="text-xs text-orange-600">
              {t(claimT, 'benefit_3_sub', 'Local customers only')}
            </p>
          </div>
        </div>

        {/* Fixly comparison */}
        <div className="bg-gray-100 rounded-2xl p-6 mb-8">
          <div className="grid grid-cols-2 gap-6">
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">Fixly</h4>
              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex items-start gap-2">
                  <span className="text-red-500">✗</span>
                  <span>{t(claimT, 'vs_bad_1', '20-30% commission fee')}</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-red-500">✗</span>
                  <span>{t(claimT, 'vs_bad_2', 'Hidden fees and charges')}</span>
                </div>
              </div>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">Nevumo</h4>
              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex items-start gap-2">
                  <span className="text-green-500">✓</span>
                  <span>{t(claimT, 'vs_good_1', '0% commission forever')}</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-green-500">✓</span>
                  <span>{t(claimT, 'vs_good_2', 'No hidden fees, ever')}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Primary CTA */}
        {isAuthenticated ? (
          <form action={async () => {
            'use server';
            const claimResult = await claimProfile(token, authToken);
            if (claimResult.success) {
              redirect(`/${normalizedLang}/provider/dashboard`);
            }
            redirect(`/${normalizedLang}/claim/${token}?error=claim_failed`);
          }}>
            <button
              type="submit"
              className="w-full bg-orange-500 hover:bg-orange-600 text-white font-semibold py-4 rounded-xl text-lg transition-colors"
            >
              {t(claimT, 'cta_claim', 'Claim your profile for free')}
            </button>
          </form>
        ) : (
          <Link
            href={`/${normalizedLang}/auth/register?redirect=/${normalizedLang}/claim/${token}&intent=provider`}
            className="block w-full bg-orange-500 hover:bg-orange-600 text-white font-semibold py-4 rounded-xl text-lg transition-colors text-center"
          >
            {t(claimT, 'cta_register', 'Register and claim this profile for free')}
          </Link>
        )}

        {/* Time signal */}
        <div className="flex items-center justify-center gap-2 mt-4 text-sm text-gray-500">
          <span>⏱️</span>
          <span>{t(claimT, 'time_signal', 'Takes less than 2 minutes')}</span>
        </div>

        {/* Divider and ghost link (if not authenticated) */}
        {!isAuthenticated && (
          <>
            <div className="flex items-center gap-4 my-6">
              <div className="flex-1 h-px bg-gray-200"></div>
              <span className="text-gray-400 text-sm">или</span>
              <div className="flex-1 h-px bg-gray-200"></div>
            </div>
            <div className="text-center">
              <Link
                href={`/${normalizedLang}/auth/login?redirect=/${normalizedLang}/claim/${token}`}
                className="text-gray-600 hover:text-gray-900 text-sm"
              >
                {t(claimT, 'login_hint', 'Already have an account? Log in')}
              </Link>
            </div>
          </>
        )}

        {/* Social proof */}
        <div className="mt-8 flex items-center justify-center gap-2">
          <div className="flex -space-x-2">
            <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-bold border-2 border-white">JD</div>
            <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white text-xs font-bold border-2 border-white">MK</div>
            <div className="w-8 h-8 rounded-full bg-purple-500 flex items-center justify-center text-white text-xs font-bold border-2 border-white">AP</div>
          </div>
          <span className="text-sm text-gray-600">{socialProof}</span>
        </div>

        {/* Trust row */}
        <div className="mt-8 flex flex-wrap justify-center gap-4 text-xs text-gray-500">
          <span className="flex items-center gap-1">
            <span>🔒</span>
            {t(claimT, 'trust_gdpr', 'GDPR compliant')}
          </span>
          <span className="flex items-center gap-1">
            <span>💳</span>
            {t(claimT, 'trust_no_sub', 'No subscription')}
          </span>
          <span className="flex items-center gap-1">
            <span>❌</span>
            {t(claimT, 'trust_cancel', 'Cancel anytime')}
          </span>
        </div>
      </main>

      {/* Sticky bottom bar (mobile only) */}
      <div className="fixed bottom-0 left-0 right-0 z-50 sm:hidden
                bg-white border-t border-gray-100 px-4 py-3"
           style={{ boxShadow: '0 -2px 8px rgba(0,0,0,0.06)' }}>
        <Link
          href={`/${normalizedLang}/auth/register?redirect=/${normalizedLang}/claim/${token}&intent=provider`}
          className="block w-full bg-orange-500 text-white text-center
                     py-3 rounded-xl font-semibold text-base"
        >
          {t(claimT, 'cta_register', 'Register and claim for free')}
        </Link>
      </div>
    </div>
  );
}
