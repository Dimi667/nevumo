import Link from 'next/link';
import Image from 'next/image';
import { SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE } from '@/lib/locales';
import { t, type TranslationDict } from '@/lib/ui-translations';
import { generateHreflangAlternates } from '@/lib/seo';
import { ReactNode } from 'react';

interface PageProps {
  params: Promise<{ lang: string }>;
}

const API_BASE = typeof window === 'undefined' 
  ? (process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000')
  : (process.env.NEXT_PUBLIC_API_URL || '');

async function getTranslations(lang: string): Promise<TranslationDict> {
  try {
    const res = await fetch(
      `${API_BASE}/api/v1/translations/cookies?lang=${lang}`,
      { next: { revalidate: 3600 } }
    );
    if (!res.ok) return {};
    return (await res.json()) as TranslationDict;
  } catch (error) {
    console.error('Fetch error:', error);
    return {};
  }
}

export async function generateStaticParams() {
  return SUPPORTED_LANGUAGES.map((lang) => ({ lang }));
}

export async function generateMetadata({ params }: PageProps) {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : DEFAULT_LANGUAGE;
  const dict = await getTranslations(normalizedLang);

  const title = t(dict, 'page_title', 'Cookie Policy');

  return {
    title,
    alternates: {
      canonical: `/${normalizedLang}/cookies`,
      languages: generateHreflangAlternates('/cookies'),
    },
    openGraph: {
      title,
      url: `${process.env.NEXT_PUBLIC_SITE_URL}/${normalizedLang}/cookies`,
      siteName: 'Nevumo',
      locale: normalizedLang,
      type: 'website',
    },
  };
}

export default async function CookiesPage({ params }: PageProps) {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : DEFAULT_LANGUAGE;
  const cookiesT = await getTranslations(normalizedLang);

  const Table = ({ headers, rows }: { headers: string[], rows: (string | ReactNode)[][] }) => (
    <div className="overflow-x-auto my-6">
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="border-b border-border">
            {headers.map((header, i) => (
              <th key={i} className="text-left py-2 pr-4 font-medium text-foreground">
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} className="border-b border-border/50">
              {row.map((cell, j) => (
                <td key={j} className="py-2 pr-4 text-muted-foreground">
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  return (
    <div className="min-h-screen bg-white">
      {/* NAVBAR */}
      <nav className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto border-b border-gray-100">
        <Link href={`/${normalizedLang}`} className="text-sm text-gray-600 transition-colors hover:text-orange-600">
          {t(cookiesT, 'back_to_home', 'Back to home')}
        </Link>
      </nav>

      <main>
        <article className="max-w-3xl mx-auto px-4 py-12">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{t(cookiesT, 's1_title', 'Cookie Policy')}</h1>
          <p className="text-sm text-muted-foreground mb-8">
            {t(cookiesT, 'last_updated', 'Last updated: 16 May 2026')}
          </p>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(cookiesT, 's1_title', '1. What Are Cookies?')}</h2>
            <p className="text-gray-700 leading-relaxed mb-4">
              {t(cookiesT, 's1_cookies')}
            </p>
            <p className="text-gray-700 leading-relaxed mb-4">
              {t(cookiesT, 's1_localstorage')}
            </p>
            <p className="text-gray-700 leading-relaxed mb-4">
              {t(cookiesT, 's1_sessionstorage')}
            </p>
            <p className="text-gray-700 leading-relaxed">
              {t(cookiesT, 's1_note')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(cookiesT, 's2_title', '2. How We Use Cookies')}</h2>
            <p className="text-gray-700 leading-relaxed">
              {t(cookiesT, 's2_text')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(cookiesT, 's3_title', '3. Cookie Categories')}</h2>
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2">{t(cookiesT, 's3_1_title', '3.1 Strictly Necessary')}</h3>
              <p className="text-gray-700 leading-relaxed">
                {t(cookiesT, 's3_1_text')}
              </p>
            </div>
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2">{t(cookiesT, 's3_2_title', '3.2 Functional')}</h3>
              <p className="text-gray-700 leading-relaxed">
                {t(cookiesT, 's3_2_text')}
              </p>
            </div>
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2">{t(cookiesT, 's3_3_title', '3.3 Analytics')}</h3>
              <p className="text-gray-700 leading-relaxed">
                {t(cookiesT, 's3_3_text')}
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">{t(cookiesT, 's3_4_title', '3.4 Marketing')}</h3>
              <p className="text-gray-700 leading-relaxed">
                {t(cookiesT, 's3_4_text')}
              </p>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(cookiesT, 's4_title', '4. Your Cookie Choices')}</h2>
            <p className="text-gray-700 leading-relaxed">
              {t(cookiesT, 's4_text')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(cookiesT, 's5_title', '5. Cookies Used by Nevumo')}</h2>
            <p className="text-gray-700 leading-relaxed mb-4">
              {t(cookiesT, 's5_text')}
            </p>
            <Table
              headers={['Name / Key', 'Storage Type', 'Purpose', 'Provider', 'Retention', 'Category', 'Legal Basis']}
              rows={[
                [<code>nevumo_consent</code>, t(cookiesT, 's5_type_cookie_1p', 'Cookie (1st party)'), t(cookiesT, 's5_p_consent', 'Cookie consent record'), 'Nevumo', t(cookiesT, 's5_ret_12mo', '12 months'), 'Necessary', 'Legal obligation'],
                [<code>lang</code>, t(cookiesT, 's5_type_cookie_1p', 'Cookie (1st party)'), t(cookiesT, 's5_p_lang', 'Language preference'), 'Nevumo', t(cookiesT, 's5_ret_30d', '30 days'), 'Functional', 'Legitimate Interest'],
                [<code>_ga</code>, t(cookiesT, 's5_type_cookie_3p', 'Cookie (3rd party)'), t(cookiesT, 's5_p_ga', 'Google Analytics'), 'Google', t(cookiesT, 's5_ret_13mo', '13 months'), 'Analytics', 'Consent'],
                [<code>_ga_[ID]</code>, t(cookiesT, 's5_type_cookie_3p', 'Cookie (3rd party)'), t(cookiesT, 's5_p_ga_id', 'Google Analytics user ID'), 'Google', t(cookiesT, 's5_ret_13mo', '13 months'), 'Analytics', 'Consent'],
                [<code>__stripe_mid</code>, t(cookiesT, 's5_type_cookie_3p', 'Cookie (3rd party)'), t(cookiesT, 's5_p_stripe_mid', 'Stripe fraud prevention'), 'Stripe', t(cookiesT, 's5_ret_1y', '1 year'), 'Necessary', 'Legitimate Interest'],
                [<code>__stripe_sid</code>, t(cookiesT, 's5_type_cookie_3p', 'Cookie (3rd party)'), t(cookiesT, 's5_p_stripe_sid', 'Stripe session ID'), 'Stripe', t(cookiesT, 's5_ret_30min', '30 minutes'), 'Necessary', 'Legitimate Interest'],
                [<code>nevumo_auth_token</code>, t(cookiesT, 's5_type_localstorage', 'localStorage'), t(cookiesT, 's5_p_auth_token', 'Authentication JWT token'), 'Nevumo', t(cookiesT, 's5_ret_sess_30d', 'Session + 30 days'), 'Necessary', 'Contract'],
                [<code>nevumo_auth_user</code>, t(cookiesT, 's5_type_localstorage', 'localStorage'), t(cookiesT, 's5_p_auth_user', 'User info cache'), 'Nevumo', t(cookiesT, 's5_ret_sess_30d', 'Session + 30 days'), 'Necessary', 'Contract'],
                [<code>nevumo_phone</code>, t(cookiesT, 's5_type_localstorage', 'localStorage'), t(cookiesT, 's5_p_phone', 'Phone number autofill'), 'Nevumo', t(cookiesT, 's5_ret_cleared', 'Until cleared'), 'Functional', 'Legitimate Interest'],
                [<code>nevumo_intent</code>, t(cookiesT, 's5_type_localstorage', 'localStorage'), t(cookiesT, 's5_p_intent', 'User intent (client/provider)'), 'Nevumo', t(cookiesT, 's5_ret_session', 'Session'), 'Functional', 'Legitimate Interest'],
                [<code>nevumo_city_preference</code>, t(cookiesT, 's5_type_localstorage', 'localStorage'), t(cookiesT, 's5_p_city', 'Preferred city'), 'Nevumo', t(cookiesT, 's5_ret_cleared', 'Until cleared'), 'Functional', 'Legitimate Interest'],
                [<code>nevumo_city</code>, t(cookiesT, 's5_type_cookie_1p', 'Cookie (1st party)'), t(cookiesT, 's5_p_city_cookie', 'Stores the city selected by the user for homepage personalisation'), 'Nevumo', t(cookiesT, 's5_ret_1y', '1 year'), 'Functional', 'Legitimate Interest'],
                [<code>nevumo_last_url</code>, t(cookiesT, 's5_type_localstorage', 'localStorage'), t(cookiesT, 's5_p_last_url', 'Last visited page for PWA smart redirect'), 'Nevumo', t(cookiesT, 's5_ret_cleared', 'Until cleared'), 'Functional', 'Legitimate Interest'],
                [<code>nevumo_auth_email</code>, t(cookiesT, 's5_type_sessionstorage', 'sessionStorage'), t(cookiesT, 's5_p_auth_email', 'Email during registration'), 'Nevumo', t(cookiesT, 's5_ret_session_tab', 'Session (tab)'), 'Necessary', 'Contract'],
              ]}
            />
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(cookiesT, 's6_title', '6. How to Manage Cookies in Your Browser')}</h2>
            <Table
              headers={['Browser', 'Path']}
              rows={[
                ['Chrome', t(cookiesT, 's6_chrome_path', 'Settings → Privacy and security → Cookies and other site data')],
                ['Firefox', t(cookiesT, 's6_firefox_path', 'Options → Privacy & Security → Cookies and Site Data')],
                ['Safari', t(cookiesT, 's6_safari_path', 'Preferences → Privacy → Manage Website Data')],
                ['Edge', t(cookiesT, 's6_edge_path', 'Settings → Cookies and site permissions → Manage and delete cookies')],
              ]}
            />
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(cookiesT, 's7_title', '7. Third-Party Processors')}</h2>
            <Table
              headers={['Processor', 'Role', 'Privacy Policy']}
              rows={[
                ['Google LLC', t(cookiesT, 's7_role_google', 'Analytics (GA4)'), <a key="google" href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer" className="text-orange-600 hover:underline">https://policies.google.com/privacy</a>],
                ['Stripe, Inc.', t(cookiesT, 's7_role_stripe', 'Payment processing'), <a key="stripe" href="https://stripe.com/privacy" target="_blank" rel="noopener noreferrer" className="text-orange-600 hover:underline">https://stripe.com/privacy</a>],
                ['Vercel Inc.', t(cookiesT, 's7_role_vercel', 'Frontend hosting'), <a key="vercel" href="https://vercel.com/legal/privacy-policy" target="_blank" rel="noopener noreferrer" className="text-orange-600 hover:underline">https://vercel.com/legal/privacy-policy</a>],
                ['Railway Corp.', t(cookiesT, 's7_role_railway', 'Backend API hosting'), <a key="railway" href="https://railway.app/legal/privacy" target="_blank" rel="noopener noreferrer" className="text-orange-600 hover:underline">https://railway.app/legal/privacy</a>],
                ['Neon Inc.', t(cookiesT, 's7_role_neon', 'Database hosting'), <a key="neon" href="https://neon.tech/privacy-policy" target="_blank" rel="noopener noreferrer" className="text-orange-600 hover:underline">https://neon.tech/privacy-policy</a>],
                ['Upstash Inc.', t(cookiesT, 's7_role_upstash', 'Redis cache'), <a key="upstash" href="https://upstash.com/trust/privacy.pdf" target="_blank" rel="noopener noreferrer" className="text-orange-600 hover:underline">https://upstash.com/trust/privacy.pdf</a>],
                ['Cloudflare Inc.', t(cookiesT, 's7_role_cloudflare', 'File/image storage (R2)'), <a key="cloudflare" href="https://www.cloudflare.com/privacypolicy/" target="_blank" rel="noopener noreferrer" className="text-orange-600 hover:underline">https://www.cloudflare.com/privacypolicy/</a>],
              ]}
            />
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(cookiesT, 's8_title', '8. International Data Transfers')}</h2>
            <Table
              headers={['Recipient', 'Country', 'Safeguard']}
              rows={[
                ['Google LLC (GA4)', t(cookiesT, 's8_country_usa', 'USA'), t(cookiesT, 's8_safeguard_sccs_dpf', 'Standard Contractual Clauses + Data Privacy Framework')],
                ['Stripe, Inc.', t(cookiesT, 's8_country_usa', 'USA'), t(cookiesT, 's8_safeguard_sccs', 'Standard Contractual Clauses')],
                ['Vercel Inc.', t(cookiesT, 's8_country_usa', 'USA'), t(cookiesT, 's8_safeguard_sccs', 'Standard Contractual Clauses')],
                ['Railway Corp.', t(cookiesT, 's8_country_usa', 'USA'), t(cookiesT, 's8_safeguard_sccs', 'Standard Contractual Clauses')],
                ['Neon Inc.', t(cookiesT, 's8_country_usa', 'USA'), t(cookiesT, 's8_safeguard_sccs', 'Standard Contractual Clauses')],
                ['Upstash Inc.', t(cookiesT, 's8_country_usa', 'USA'), t(cookiesT, 's8_safeguard_sccs', 'Standard Contractual Clauses')],
                ['Cloudflare Inc. (R2)', t(cookiesT, 's8_country_usa', 'USA'), t(cookiesT, 's8_safeguard_sccs_dpf', 'Standard Contractual Clauses + Data Privacy Framework')],
              ]}
            />
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(cookiesT, 's9_title', '9. Cookie Consent Management')}</h2>
            <p className="text-gray-700 leading-relaxed">
              {t(cookiesT, 's9_text')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(cookiesT, 's10_title', '10. Changes to This Cookie Policy')}</h2>
            <p className="text-gray-700 leading-relaxed">
              {t(cookiesT, 's10_text')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(cookiesT, 's11_title', '11. Contact and Supervisory Authorities')}</h2>
            <p className="text-gray-700 leading-relaxed mb-4">
              {t(cookiesT, 's11_text')}
            </p>
            <p className="text-gray-700 leading-relaxed mb-2">
              {t(cookiesT, 's11_authority_bg')}
            </p>
            <p className="text-gray-700 leading-relaxed">
              {t(cookiesT, 's11_authority_pl')}
            </p>
          </section>
        </article>
      </main>
    </div>
  );
}
