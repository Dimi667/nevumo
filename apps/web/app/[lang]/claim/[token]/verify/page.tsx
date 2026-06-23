import { cookies } from 'next/headers';
import { SUPPORTED_LANGUAGES } from '@/lib/locales';
import { generateHreflangAlternates } from '@/lib/seo';
import { fetchTranslations, t } from '@/lib/ui-translations';
import { Metadata } from 'next';
import { redirect } from 'next/navigation';
import VerifyCodeForm from './VerifyCodeForm';

interface PageProps {
  params: Promise<{ lang: string; token: string }>;
  searchParams?: Promise<{ sent_to?: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { lang, token } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : 'en';
  const claimT = await fetchTranslations(normalizedLang, 'claim');

  const title = t(claimT, 'verify_title', 'Enter verification code');
  const description = t(claimT, 'verify_subtitle', 'We sent a 6-digit code to the business email linked to this profile. Enter it below to confirm ownership.');

  return {
    title,
    description,
    alternates: {
      canonical: `/${normalizedLang}/claim/${token}/verify`,
      languages: generateHreflangAlternates(`/claim/${token}/verify`),
    },
    robots: { index: false, follow: true },
  };
}

export default async function VerifyPage({ params, searchParams }: PageProps) {
  const { lang, token } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : 'en';
  const claimT = await fetchTranslations(normalizedLang, 'claim');

  const resolvedSearchParams = searchParams ? await searchParams : {};
  const sentTo = (resolvedSearchParams as Record<string, string>)?.sent_to ?? '';

  // Check auth status via cookie
  const cookieStore = await cookies();
  const authToken = cookieStore.get('nevumo_auth_token')?.value || '';

  if (!authToken) {
    redirect(`/${normalizedLang}/auth?redirect=/${normalizedLang}/claim/${token}/verify`);
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
          {/* Orange top accent strip */}
          <div className="h-1 bg-orange-500" />
          
          <div className="p-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-3">
              {t(claimT, 'verify_title', 'Enter verification code')}
            </h1>
            
            <p className="text-gray-600 mb-8 leading-relaxed">
              {t(claimT, 'verify_subtitle', 'We sent a 6-digit code to the business email linked to this profile. Enter it below to confirm ownership.')}
            </p>

            <VerifyCodeForm
              lang={normalizedLang}
              token={token}
              authToken={authToken}
              dict={claimT}
              sentTo={sentTo}
            />

            <div className="mt-6 text-center">
              <p className="text-sm text-gray-500">
                {t(claimT, 'verify_hint', "Didn't receive the code? Check your spam folder.")}
              </p>
              <p className="text-sm text-gray-400 mt-1">
                {t(claimT, 'verify_expires', 'Code is valid for 24 hours.')}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
