import { SUPPORTED_LANGUAGES } from '@/lib/locales';
import { fetchTranslations, t } from '@/lib/ui-translations';
import { Metadata } from 'next';
import Link from 'next/link';
import ObjectionConfirmButton from './ObjectionConfirmButton';

interface PageProps {
  params: Promise<{ lang: string }>;
  searchParams: Promise<{ status?: string; token?: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : 'en';
  const objectionT = await fetchTranslations(normalizedLang, 'outreach_objection');

  const title = t(objectionT, 'confirm_title', 'Confirm data removal');
  const description = t(objectionT, 'confirm_description', 'Once confirmed, we will immediately and permanently remove this business\'s publicly available data from Nevumo.');

  return {
    title,
    description,
    robots: { index: false, follow: false },
  };
}

export default async function OutreachObjectionPage({ params, searchParams }: PageProps) {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : 'en';
  const objectionT = await fetchTranslations(normalizedLang, 'outreach_objection');

  const resolvedSearchParams = await searchParams;
  const status = resolvedSearchParams?.status;
  const token = resolvedSearchParams?.token;

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-sm border border-gray-100 p-8 text-center">

        {status === 'confirm' && token ? (
          <>
            <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg
                className="w-8 h-8 text-orange-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01M12 3a9 9 0 100 18A9 9 0 0012 3z" />
              </svg>
            </div>

            <h1 className="text-2xl font-bold text-gray-900 mb-3">
              {t(objectionT, 'confirm_title', 'Confirm data removal')}
            </h1>
            <p className="text-gray-500 text-base leading-relaxed mb-8">
              {t(objectionT, 'confirm_description', 'Once confirmed, we will immediately and permanently remove this business\'s publicly available data from Nevumo: business name, email, and phone number. The profile will disappear from search results.')}
            </p>

            <div className="flex flex-col gap-3">
              <ObjectionConfirmButton token={token} lang={normalizedLang}>
                {t(objectionT, 'confirm_button', 'Yes, remove my data')}
              </ObjectionConfirmButton>
              <Link
                href={`/${normalizedLang}`}
                className="inline-block text-gray-600 hover:text-gray-800 font-medium px-6 py-3 rounded-xl transition-colors duration-150"
              >
                {t(objectionT, 'confirm_cancel_link', 'No, close this page')}
              </Link>
            </div>
          </>
        ) : status === 'success' ? (
          <>
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg
                className="w-8 h-8 text-green-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </div>

            <h1 className="text-2xl font-bold text-gray-900 mb-3">
              {t(objectionT, 'success_title', 'Done — your data has been removed')}
            </h1>
            <p className="text-gray-500 text-base leading-relaxed mb-8">
              {t(objectionT, 'success_description', 'This business\'s publicly available data has been removed from Nevumo. The profile no longer appears in search.')}
            </p>
            <Link
              href={`/${normalizedLang}`}
              className="inline-block bg-orange-500 hover:bg-orange-600 text-white font-semibold px-6 py-3 rounded-xl transition-colors duration-150"
            >
              {t(objectionT, 'back_button', 'Back to nevumo.com')}
            </Link>
          </>
        ) : status === 'already_done' ? (
          <>
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg
                className="w-8 h-8 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01M12 3a9 9 0 100 18A9 9 0 0012 3z" />
              </svg>
            </div>

            <h1 className="text-2xl font-bold text-gray-900 mb-3">
              {t(objectionT, 'already_done_title', 'Already processed')}
            </h1>
            <p className="text-gray-500 text-base leading-relaxed mb-8">
              {t(objectionT, 'already_done_description', 'This request has already been completed — this business\'s data has already been removed from Nevumo.')}
            </p>
            <Link
              href={`/${normalizedLang}`}
              className="inline-block bg-gray-800 hover:bg-gray-900 text-white font-semibold px-6 py-3 rounded-xl transition-colors duration-150"
            >
              {t(objectionT, 'back_button', 'Back to nevumo.com')}
            </Link>
          </>
        ) : (
          <>
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg
                className="w-8 h-8 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01M12 3a9 9 0 100 18A9 9 0 0012 3z" />
              </svg>
            </div>

            <h1 className="text-2xl font-bold text-gray-900 mb-3">
              {t(objectionT, 'invalid_title', 'This link is invalid')}
            </h1>
            <p className="text-gray-500 text-base leading-relaxed mb-8">
              {t(objectionT, 'invalid_description', 'This link is invalid, expired, or has already been used. If you believe this is a mistake, contact us at privacy@nevumo.com.')}
            </p>
            <Link
              href={`/${normalizedLang}`}
              className="inline-block bg-gray-800 hover:bg-gray-900 text-white font-semibold px-6 py-3 rounded-xl transition-colors duration-150"
            >
              {t(objectionT, 'back_button', 'Back to nevumo.com')}
            </Link>
          </>
        )}

        <p className="mt-8 text-xs text-gray-300">
          © 2026 Nevumo · FILIPIS CENTAR BALGARIYA OOD · EIK: 175369610
        </p>
      </div>
    </div>
  );
}
