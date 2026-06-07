import Link from 'next/link';
import Image from 'next/image';
import { SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE } from '@/lib/locales';
import { fetchTranslations, t } from '@/lib/ui-translations';
import { generateHreflangAlternates } from '@/lib/seo';

interface PageProps {
  params: Promise<{ lang: string }>;
  searchParams: { modal?: string };
}

export async function generateStaticParams() {
  return SUPPORTED_LANGUAGES.map((lang) => ({ lang }));
}

export async function generateMetadata({ params }: PageProps) {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : DEFAULT_LANGUAGE;
  const dict = await fetchTranslations(normalizedLang, 'privacy');

  const title = t(dict, 'page_title', 'Privacy Policy — Nevumo');
  const description = t(dict, 'meta_description', 'Learn how Nevumo collects, uses and protects your personal data in accordance with GDPR.');

  return {
    title,
    description,
    alternates: {
      canonical: `/${normalizedLang}/privacy`,
      languages: generateHreflangAlternates('/privacy'),
    },
    openGraph: {
      title,
      description,
      url: `${process.env.NEXT_PUBLIC_SITE_URL}/${normalizedLang}/privacy`,
      siteName: 'Nevumo',
      locale: normalizedLang,
      type: 'website',
    },
  };
}

export default async function PrivacyPage({ params, searchParams }: PageProps) {
  const { lang } = await params;
  const { modal } = await searchParams;
  const isModal = modal === 'true';
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : DEFAULT_LANGUAGE;
  const dict = await fetchTranslations(normalizedLang, 'privacy');

  const Table = ({ headers, rows }: { headers: string[], rows: string[][] }) => (
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
      <main>
        <article className="max-w-3xl mx-auto px-4 py-12">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{t(dict, 'heading', 'Privacy Policy')}</h1>
          <p className="text-sm text-muted-foreground mb-8">
            {t(dict, 'effective_date_label', 'Effective date:')} {t(dict, 'effective_date_value', '11 May 2026')} |{' '}
            {t(dict, 'version_label', 'Document version:')} {t(dict, 'version_value', '2026-05-11')}
          </p>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 'section_1_title', '1. Data Controller')}</h2>
            <p className="text-gray-700 leading-relaxed">
              {t(dict, 'section_1_body')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 'section_2_title', '2. What Is Nevumo?')}</h2>
            <p className="text-gray-700 leading-relaxed">
              {t(dict, 'section_2_body')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 'section_3_title', '3. What Data We Collect and Why')}</h2>
            
            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_3_1_title', '3.1 Account Registration')}</h3>
            <Table 
              headers={[t(dict, 'col_data', 'Data'), t(dict, 'col_purpose', 'Purpose'), t(dict, 'col_legal_basis', 'Legal Basis')]}
              rows={[
                [t(dict, 't31_email_data', 'Email address'), t(dict, 't31_email_purpose', 'Account creation, login'), t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b)')],
                [t(dict, 't31_password_data', 'Password (bcrypt hash)'), t(dict, 't31_password_purpose', 'Account security'), t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b)')],
                [t(dict, 't31_role_data', 'Role (client / provider)'), t(dict, 't31_role_purpose', 'Platform functionality'), t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b)')],
                [t(dict, 't31_age_data', 'Age confirmation (18+)'), t(dict, 't31_age_purpose', 'Legal requirement'), t(dict, 'legal_obligation_c', 'Legal obligation — Art. 6(1)(c)')]
              ]}
            />

            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_3_2_title', '3.2 Provider Profile')}</h3>
            <Table 
              headers={[t(dict, 'col_data', 'Data'), t(dict, 'col_purpose', 'Purpose'), t(dict, 'col_legal_basis', 'Legal Basis')]}
              rows={[
                [t(dict, 't32_name_data', 'Name, description, category'), t(dict, 't32_name_purpose', 'Public profile'), t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b)')],
                [t(dict, 't32_photo_data', 'Profile photo (optional)'), t(dict, 't32_photo_purpose', 'Public display'), t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b)')],
                [t(dict, 't32_phone_data', 'Phone number'), t(dict, 't32_phone_purpose', 'Lead delivery, communication'), t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b)')],
                [t(dict, 't32_location_data', 'Location / city'), t(dict, 't32_location_purpose', 'Service area matching'), t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b)')],
                [t(dict, 't32_services_data', 'Services and prices'), t(dict, 't32_services_purpose', 'Marketplace listing'), t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b)')],
                [t(dict, 't32_performance_data', 'Performance indicators (completed jobs, rating, verification level)'), t(dict, 't32_performance_purpose', 'Automatic calculation of ranking position and public status badge'), t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b)')]
              ]}
            />

            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_3_3_title', '3.3 Service Requests (Leads)')}</h3>
            <Table 
              headers={[t(dict, 'col_data', 'Data'), t(dict, 'col_purpose', 'Purpose'), t(dict, 'col_legal_basis', 'Legal Basis')]}
              rows={[
                [t(dict, 't33_request_data', 'Request details'), t(dict, 't33_request_purpose', 'Client-provider matching'), t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b)')],
                [t(dict, 't33_contact_data', 'Contact information'), t(dict, 't33_contact_purpose', 'Communication'), t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b)')],
                [t(dict, 't33_status_data', 'Lead status history'), t(dict, 't33_status_purpose', 'Functionality & disputes'), t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b)')]
              ]}
            />

            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_3_4_title', '3.4 Security and Technical Data')}</h3>
            <Table 
              headers={[t(dict, 'col_data', 'Data'), t(dict, 'col_purpose', 'Purpose'), t(dict, 'col_legal_basis', 'Legal Basis')]}
              rows={[
                [t(dict, 't34_ip_data', 'IP address (hashed)'), t(dict, 't34_ip_purpose', 'Security, rate limiting'), t(dict, 'legal_legitimate_f', 'Legitimate interest — Art. 6(1)(f)')],
                [t(dict, 't34_agent_data', 'User agent'), t(dict, 't34_agent_purpose', 'Security & diagnostics'), t(dict, 'legal_legitimate_f', 'Legitimate interest — Art. 6(1)(f)')],
                [t(dict, 't34_authlogs_data', 'Auth logs'), t(dict, 't34_authlogs_purpose', 'Security monitoring'), t(dict, 'legal_legitimate_f', 'Legitimate interest — Art. 6(1)(f)')]
              ]}
            />

            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_3_5_title', '3.5 Analytics')}</h3>
            <p className="text-gray-700 leading-relaxed mb-4">
              {t(dict, 'section_3_5_body')}
            </p>

            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_3_6_title', '3.6 Communications')}</h3>
            <Table
              headers={[t(dict, 'col_data', 'Data'), t(dict, 'col_purpose', 'Purpose'), t(dict, 'col_legal_basis', 'Legal Basis')]}
              rows={[
                [t(dict, 't36_transactional_data', 'Transactional emails'), t(dict, 't36_transactional_purpose', 'Service delivery'), t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b) GDPR')],
                [t(dict, 't36_marketing_data', 'Marketing emails'), t(dict, 't36_marketing_purpose', 'Marketing'), t(dict, 'legal_consent_a', 'Consent — Art. 6(1)(a) GDPR')]
              ]}
            />
            <p className="text-sm text-muted-foreground mt-2">
              {t(dict, 'section_3_6_note')}
            </p>

            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_3_7_title', '3.7 Claimed Provider Profiles (Article 14 GDPR)')}</h3>
            <p className="text-gray-700 leading-relaxed">
              {t(dict, 'section_3_7_body')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 'section_4_title', '4. Cookies and Local Storage')}</h2>
            <p className="text-gray-700 leading-relaxed mb-4">
              {t(dict, 'section_4_intro')}
            </p>
            <Table 
              headers={[t(dict, 'col_key', 'Key'), t(dict, 'col_type', 'Type'), t(dict, 'col_purpose', 'Purpose'), t(dict, 'col_retention', 'Retention'), t(dict, 'col_basis', 'Basis')]}
              rows={[
                ['nevumo_consent', 'Cookie', t(dict, 't4_purpose_consent_record', 'Cookie consent record'), t(dict, 't4_ret_12m', '12 months'), t(dict, 't4_basis_necessary', 'Necessary')],
                ['lang', 'Cookie', t(dict, 't4_purpose_lang_pref', 'Language preference'), t(dict, 't4_ret_30d', '30 days'), t(dict, 't4_basis_functional', 'Functional')],
                ['_ga, _ga_*', 'Cookie', t(dict, 't4_purpose_ga4', 'GA4 analytics'), t(dict, 't4_ret_13m', '13 months'), t(dict, 't4_basis_consent', 'Consent')],
                ['__stripe_mid', 'Cookie', t(dict, 't4_purpose_stripe_fraud', 'Stripe fraud prevention (checkout)'), t(dict, 't4_ret_1y', '1 year'), t(dict, 't4_basis_necessary', 'Necessary')],
                ['__stripe_sid', 'Cookie', t(dict, 't4_purpose_stripe_fraud', 'Stripe fraud prevention (checkout)'), t(dict, 't4_ret_30min', '30 min'), t(dict, 't4_basis_necessary', 'Necessary')],
                ['nevumo_auth_token', 'localStorage', t(dict, 't4_purpose_auth_jwt', 'Auth JWT'), t(dict, 't4_ret_30d', '30 days'), t(dict, 't4_basis_contract', 'Contract')],
                ['nevumo_auth_user', 'localStorage', t(dict, 't4_purpose_user_cache', 'User info cache'), t(dict, 't4_ret_30d', '30 days'), t(dict, 't4_basis_contract', 'Contract')],
                ['nevumo_phone', 'localStorage', t(dict, 't4_purpose_phone_autofill', 'Phone autofill'), t(dict, 't4_ret_indefinite', 'Indefinite'), t(dict, 't4_basis_legint', 'Legitimate interest')],
                ['nevumo_intent', 'localStorage', t(dict, 't4_purpose_ux_role', 'UX role at login'), t(dict, 't4_ret_session', 'Session'), t(dict, 't4_basis_functional', 'Functional')],
                ['nevumo_city_preference', 'localStorage', t(dict, 't4_purpose_city_pref', 'Preferred city'), t(dict, 't4_ret_indefinite', 'Indefinite'), t(dict, 't4_basis_functional', 'Functional')],
                ['nevumo_city', 'Cookie', t(dict, 't4_purpose_city_cookie', 'Stores the city selected by the user for homepage personalisation'), t(dict, 't4_ret_1y', '1 year'), t(dict, 't4_basis_functional', 'Functional')],
                ['nevumo_last_url', 'localStorage', t(dict, 't4_purpose_pwa_redirect', 'Last visited page for PWA smart redirect'), t(dict, 't4_ret_indefinite', 'Indefinite'), t(dict, 't4_basis_functional', 'Functional')],
                ['nevumo_auth_email', 'sessionStorage', t(dict, 't4_purpose_email_reg', 'Email during registration'), t(dict, 't4_ret_session_tab', 'Session (tab)'), t(dict, 't4_basis_contract', 'Contract')]
              ]}
            />
            <Link href={`/${normalizedLang}/cookies`} className="text-orange-600 hover:underline">
              {t(dict, 'cookies_link_text', 'Cookie Policy')}
            </Link>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 'section_5_title', '5. Who We Share Your Data With')}</h2>
            <p className="text-gray-700 leading-relaxed mb-4 italic">
              {t(dict, 'section_5_note')}
            </p>
            <Table 
              headers={[t(dict, 'col_processor', 'Processor'), t(dict, 'col_purpose', 'Purpose'), t(dict, 'col_country', 'Country'), t(dict, 'col_safeguard', 'Safeguard')]}
              rows={[
                ['Google LLC (GA4)', t(dict, 't5_analytics', 'Analytics'), t(dict, 't5_usa', 'USA'), t(dict, 't5_sccs_dpf', 'SCCs + DPF')],
                ['Stripe, Inc.', t(dict, 't5_payments', 'Payments (BLIK, Przelewy24)'), t(dict, 't5_usa', 'USA'), t(dict, 't5_sccs_dpf', 'SCCs + DPF')],
                ['Resend, Inc.', t(dict, 't5_emails', 'Transactional emails'), t(dict, 't5_usa', 'USA'), t(dict, 't5_sccs', 'SCCs')],
                ['Vercel Inc.', t(dict, 't5_frontend', 'Frontend hosting'), t(dict, 't5_usa', 'USA'), t(dict, 't5_sccs', 'SCCs')],
                ['Railway Corp.', t(dict, 't5_backend', 'Backend API hosting'), t(dict, 't5_usa', 'USA'), t(dict, 't5_sccs', 'SCCs')],
                ['Neon Inc.', t(dict, 't5_database', 'Database (PostgreSQL)'), t(dict, 't5_usa', 'USA'), t(dict, 't5_sccs', 'SCCs')],
                ['Upstash Inc.', t(dict, 't5_redis', 'Redis cache'), t(dict, 't5_usa', 'USA'), t(dict, 't5_sccs', 'SCCs')],
                ['Cloudflare Inc.', t(dict, 't5_storage', 'File/image storage (R2)'), t(dict, 't5_usa', 'USA'), t(dict, 't5_sccs_dpf', 'SCCs + DPF')]
              ]}
            />
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 'section_6_title', '6. Transfers Outside the EEA')}</h2>
            <p className="text-gray-700 leading-relaxed">
              {t(dict, 'section_6_body')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 'section_7_title', '7. Automated Processing')}</h2>
            <p className="text-gray-700 leading-relaxed mb-6">
              {t(dict, 'section_7_intro')}
            </p>

            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_7_1_title', '7.1 Provider Ranking')}</h3>
            <p className="text-gray-700 leading-relaxed mb-2">
              {t(dict, 'section_7_1_body')}
            </p>
            <p className="text-sm text-muted-foreground mb-6">
              <span className="font-medium">{t(dict, 'section_7_legal_basis_label', 'Legal basis:')}</span>{' '}
              {t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b) GDPR')}
            </p>

            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_7_2_title', '7.2 Provider Status Badge')}</h3>
            <p className="text-gray-700 leading-relaxed mb-2">
              {t(dict, 'section_7_2_body')}
            </p>
            <p className="text-sm text-muted-foreground mb-6">
              <span className="font-medium">{t(dict, 'section_7_legal_basis_label', 'Legal basis:')}</span>{' '}
              {t(dict, 'legal_contract_b', 'Contract — Art. 6(1)(b) GDPR')}
            </p>

            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_7_3_title', '7.3 Payment Fraud Detection (Stripe)')}</h3>
            <p className="text-gray-700 leading-relaxed mb-4">
              {t(dict, 'section_7_3_body')}
            </p>

            <p className="text-sm text-muted-foreground italic mt-6">
              {t(dict, 'section_7_note')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 'section_8_title', '8. How Long We Keep Your Data')}</h2>
            <Table 
              headers={[t(dict, 'col_data', 'Data'), t(dict, 'col_retention', 'Retention')]}
              rows={[
                [t(dict, 't8_active_account', 'Active account'), t(dict, 't8_until_deletion', 'Until deletion')],
                [t(dict, 't8_data_after_deletion', 'Data after deletion'), t(dict, 't8_ret_30days_backups', 'Max 30 days (encrypted backups)')],
                [t(dict, 't8_financial_records', 'Financial / Stripe records'), t(dict, 't8_ret_10years', '10 years')],
                [t(dict, 't8_security_logs', 'Security logs (hashed IP)'), t(dict, 't8_ret_90days', '90 days')],
                [t(dict, 't8_ga4_analytics', 'GA4 analytics'), t(dict, 't8_ret_14months', '14 months')],
                [t(dict, 't8_cookie_consent_records', 'Cookie consent records'), t(dict, 't8_ret_24months', '24 months')],
                [t(dict, 't8_marketing_consent', 'Marketing consent'), t(dict, 't8_ret_withdrawal_3y', 'Until withdrawal + 3 years')]
              ]}
            />
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 'section_9_title', '9. Your Rights Under GDPR')}</h2>
            <ul className="list-disc pl-6 space-y-2 text-gray-700">
              <li>{t(dict, 'rights_access')}</li>
              <li>{t(dict, 'rights_rectification')}</li>
              <li>{t(dict, 'rights_erasure')}</li>
              <li>{t(dict, 'rights_portability')}</li>
              <li>{t(dict, 'rights_object')}</li>
              <li>{t(dict, 'rights_restrict')}</li>
              <li>{t(dict, 'rights_withdraw')}</li>
            </ul>
            <p className="text-gray-700 leading-relaxed mt-4">
              {t(dict, 'rights_response_time')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 'section_10_title', '10. Right to Lodge a Complaint')}</h2>
            <p className="text-gray-700 leading-relaxed mb-6">
              {t(dict, 'section_10_body')}
            </p>
            
            <div className="bg-gray-50 p-6 rounded-lg mb-6">
              <h4 className="font-bold mb-2">{t(dict, 'section_10_lead_label', 'Lead Supervisory Authority (Bulgaria):')}</h4>
              <p className="text-sm text-gray-700 leading-relaxed">
                {t(dict, 'section_10_lead_body')}
              </p>
            </div>

            <div className="bg-gray-50 p-6 rounded-lg">
              <h4 className="font-bold mb-2">{t(dict, 'section_10_pl_label', 'Concerned Authority for Polish Users:')}</h4>
              <p className="text-sm text-gray-700 leading-relaxed">
                {t(dict, 'section_10_pl_body')}
              </p>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 'section_11_title', '11. Changes to This Policy')}</h2>
            <p className="text-gray-700 leading-relaxed">
              {t(dict, 'section_11_body')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 'section_12_title', '12. Contact')}</h2>
            <p className="text-gray-700 leading-relaxed">
              {t(dict, 'section_12_body')}
            </p>
          </section>

          <div className="mt-12 pt-8 border-t border-gray-100 italic text-sm text-gray-500">
            {t(dict, 'min_age_note')}
          </div>
        </article>
      </main>
    </div>
  );
}
