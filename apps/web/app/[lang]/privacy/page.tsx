import Link from 'next/link';
import Image from 'next/image';
import { SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE } from '@/lib/locales';
import { fetchTranslations, t } from '@/lib/ui-translations';
import { generateHreflangAlternates } from '@/lib/seo';

interface PageProps {
  params: Promise<{ lang: string }>;
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

export default async function PrivacyPage({ params }: PageProps) {
  const { lang } = await params;
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
      {/* NAVBAR */}
      <nav className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto border-b border-gray-100">
        <Link href={`/${normalizedLang}`} className="inline-flex items-center">
          <Image src="/Nevumo_logo.svg" alt="Nevumo" width={120} height={36} priority />
        </Link>
        <Link href={`/${normalizedLang}`} className="text-sm text-gray-600 transition-colors hover:text-orange-600">
          {t(dict, 'back_to_home', 'Back to home')}
        </Link>
      </nav>

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
              headers={['Data', 'Purpose', 'Legal Basis']}
              rows={[
                ['Email address', 'Account creation, login', 'Contract — Art. 6(1)(b)'],
                ['Password (bcrypt hash)', 'Account security', 'Contract — Art. 6(1)(b)'],
                ['Role (client / provider)', 'Platform functionality', 'Contract — Art. 6(1)(b)'],
                ['Age confirmation (18+)', 'Legal requirement', 'Legal obligation — Art. 6(1)(c)']
              ]}
            />

            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_3_2_title', '3.2 Provider Profile')}</h3>
            <Table 
              headers={['Data', 'Purpose', 'Legal Basis']}
              rows={[
                ['Name, description, category', 'Public profile', 'Contract — Art. 6(1)(b)'],
                ['Profile photo (optional)', 'Public display', 'Contract — Art. 6(1)(b)'],
                ['Phone number', 'Lead delivery, communication', 'Contract — Art. 6(1)(b)'],
                ['Location / city', 'Service area matching', 'Contract — Art. 6(1)(b)'],
                ['Services and prices', 'Marketplace listing', 'Contract — Art. 6(1)(b)']
              ]}
            />

            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_3_3_title', '3.3 Service Requests (Leads)')}</h3>
            <Table 
              headers={['Data', 'Purpose', 'Legal Basis']}
              rows={[
                ['Request details', 'Client-provider matching', 'Contract — Art. 6(1)(b)'],
                ['Contact information', 'Communication', 'Contract — Art. 6(1)(b)'],
                ['Lead status history', 'Functionality & disputes', 'Contract — Art. 6(1)(b)']
              ]}
            />

            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_3_4_title', '3.4 Security and Technical Data')}</h3>
            <Table 
              headers={['Data', 'Purpose', 'Legal Basis']}
              rows={[
                ['IP address (hashed)', 'Security, rate limiting', 'Legitimate interest — Art. 6(1)(f)'],
                ['User agent', 'Security & diagnostics', 'Legitimate interest — Art. 6(1)(f)'],
                ['Auth logs', 'Security monitoring', 'Legitimate interest — Art. 6(1)(f)']
              ]}
            />

            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_3_5_title', '3.5 Analytics')}</h3>
            <p className="text-gray-700 leading-relaxed mb-4">
              {t(dict, 'section_3_5_body')}
            </p>

            <h3 className="text-lg font-semibold mt-6 mb-2">{t(dict, 'section_3_6_title', '3.6 Communications')}</h3>
            <p className="text-gray-700 leading-relaxed mb-4">
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
              headers={['Key', 'Type', 'Purpose', 'Retention', 'Basis']}
              rows={[
                ['nevumo_consent', 'Cookie', 'Cookie consent record', '12 months', 'Necessary'],
                ['lang', 'Cookie', 'Language preference', '30 days', 'Functional'],
                ['_ga, _ga_*', 'Cookie', 'GA4 analytics', '13 months', 'Consent'],
                ['__stripe_mid', 'Cookie', 'Stripe fraud prevention (checkout)', '1 year', 'Necessary'],
                ['__stripe_sid', 'Cookie', 'Stripe fraud prevention (checkout)', '30 min', 'Necessary'],
                ['nevumo_auth_token', 'localStorage', 'Auth JWT', '30 days', 'Contract'],
                ['nevumo_auth_user', 'localStorage', 'User info cache', '30 days', 'Contract'],
                ['nevumo_phone', 'localStorage', 'Phone autofill', 'Indefinite', 'Legitimate interest'],
                ['nevumo_intent', 'localStorage', 'UX role at login', 'Session', 'Functional'],
                ['nevumo_city_preference', 'localStorage', 'Preferred city', 'Indefinite', 'Functional'],
                ['nevumo_auth_email', 'sessionStorage', 'Email during registration', 'Session (tab)', 'Contract']
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
              headers={['Processor', 'Purpose', 'Country', 'Safeguard']}
              rows={[
                ['Google LLC (GA4)', 'Analytics', 'USA', 'SCCs + DPF'],
                ['Stripe, Inc.', 'Payments (BLIK, Przelewy24)', 'USA', 'SCCs + DPF'],
                ['Resend, Inc.', 'Transactional emails', 'USA', 'SCCs'],
                ['Vercel Inc.', 'Frontend hosting', 'USA', 'SCCs'],
                ['Railway Corp.', 'Backend API hosting', 'USA', 'SCCs'],
                ['Neon Inc.', 'Database (PostgreSQL)', 'USA', 'SCCs'],
                ['Upstash Inc.', 'Redis cache', 'USA', 'SCCs'],
                ['Cloudflare Inc.', 'File/image storage (R2)', 'USA', 'SCCs + DPF']
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
            <h2 className="text-xl font-bold mb-4">{t(dict, 'section_7_title', '7. Automated Decision-Making')}</h2>
            <p className="text-gray-700 leading-relaxed">
              {t(dict, 'section_7_body')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-bold mb-4">{t(dict, 'section_8_title', '8. How Long We Keep Your Data')}</h2>
            <Table 
              headers={['Data', 'Retention']}
              rows={[
                ['Active account', 'Until deletion'],
                ['Data after deletion', 'Max 30 days (encrypted backups)'],
                ['Financial / Stripe records', '10 years'],
                ['Security logs (hashed IP)', '90 days'],
                ['GA4 analytics', '14 months'],
                ['Cookie consent records', '24 months'],
                ['Marketing consent', 'Until withdrawal + 3 years']
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
