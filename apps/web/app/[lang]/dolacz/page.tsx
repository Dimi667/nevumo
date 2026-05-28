import { generateHreflangAlternates } from '@/lib/seo';
import { BarChart2, Search, LayoutTemplate, QrCode, Star, BadgeCheck } from 'lucide-react';

interface PageProps {
  params: Promise<{ lang: string }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { lang } = await params;

  return {
    title: 'Zdobywaj klientów na usługi w Warszawie — za darmo',
    description: 'Dołącz do Nevumo i otrzymuj zapytania od klientów bezpośrednio na swój telefon. Bezpłatnie, bez prowizji.',
    alternates: {
      canonical: `${process.env.NEXT_PUBLIC_SITE_URL}/${lang}/dolacz`,
      languages: generateHreflangAlternates('/dolacz'),
    },
    openGraph: {
      title: "Zdobywaj klientów na usługi w Warszawie — za darmo",
      description: "Dołącz do Nevumo i otrzymuj zapytania od klientów bezpośrednio na swój telefon. Bezpłatnie przez 6 miesięcy.",
      url: `https://nevumo.com/${lang}/dolacz`,
      siteName: "Nevumo",
      locale: "pl_PL",
      type: "website",
    },
    robots: {
      index: true,
      follow: true,
    },
  };
}

export default async function DolaczPage({ params }: PageProps) {
  const { lang } = await params;

  return (
    <div className="bg-white">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Service",
            "name": "Nevumo — platforma dla specjalistów w Warszawie",
            "description": "Dołącz do Nevumo i otrzymuj zapytania od klientów bezpośrednio na swój telefon. Bezpłatnie przez 6 miesięcy.",
            "url": `https://nevumo.com/${lang}/dolacz`,
            "areaServed": {
              "@type": "City",
              "name": "Warszawa"
            },
            "provider": {
              "@type": "Organization",
              "name": "Nevumo",
              "url": "https://nevumo.com"
            },
            "offers": {
              "@type": "Offer",
              "price": "0",
              "priceCurrency": "PLN",
              "description": "Bezpłatnie przez 6 miesięcy"
            }
          })
        }}
      />
      {/* HERO SECTION */}
      <section className="bg-gradient-to-br from-orange-500 to-orange-600 text-white py-20 px-6 text-center">
        <div className="inline-block bg-white/20 rounded-full px-4 py-1 text-sm mb-6">
          Warszawa • Bezpłatnie • Bez prowizji
        </div>

        <h1 className="text-4xl font-bold leading-tight max-w-2xl mx-auto">
          Zdobywaj klientów na usługi w Warszawie — za darmo
        </h1>

        <p className="text-xl mt-4 text-orange-100 max-w-xl mx-auto">
          Dołącz do Nevumo i otrzymuj zapytania od klientów bezpośrednio na swój telefon.
        </p>

        <a
          href={`/${lang}/auth?mode=register`}
          className="mt-8 bg-white text-orange-600 font-bold text-lg px-10 py-4 rounded-xl shadow-lg hover:bg-orange-50 hover:shadow-xl transition-all inline-block"
        >
          Utwórz bezpłatny profil →
        </a>

        <p className="mt-3 text-orange-100 text-sm">
          Bezpłatnie • Bez zobowiązań • Zajmuje 2 minuty
        </p>
      </section>

      {/* HOW IT WORKS */}
      <section className="py-16 px-6 bg-white">
        <h2 className="text-center text-2xl font-bold text-gray-900 mb-12">
          Jak to działa?
        </h2>

        <div className="flex flex-col md:flex-row gap-8 max-w-3xl mx-auto">
          {/* Step 1 */}
          <div className="text-center rounded-2xl bg-gray-50 p-8 flex-1">
            <div className="bg-orange-500 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold mx-auto mb-4">
              1
            </div>
            <h3 className="font-bold text-lg">Utwórz profil</h3>
            <p className="text-gray-600 mt-2 text-sm">
              Dodaj swoje usługi, zdjęcie i obszar działania. Zajmuje 2 minuty.
            </p>
          </div>

          {/* Step 2 */}
          <div className="text-center rounded-2xl bg-gray-50 p-8 flex-1">
            <div className="bg-orange-500 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold mx-auto mb-4">
              2
            </div>
            <h3 className="font-bold text-lg">Odbieraj zapytania</h3>
            <p className="text-gray-600 mt-2 text-sm">
              Klienci w Warszawie szukający Twoich usług kontaktują się bezpośrednio z Tobą.
            </p>
          </div>

          {/* Step 3 */}
          <div className="text-center rounded-2xl bg-gray-50 p-8 flex-1">
            <div className="bg-orange-500 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold mx-auto mb-4">
              3
            </div>
            <h3 className="font-bold text-lg">Rozwijaj biznes</h3>
            <p className="text-gray-600 mt-2 text-sm">
              Więcej zleceń, zero prowizji przez pierwsze 6 miesięcy.
            </p>
          </div>
        </div>
      </section>

      {/* CO OTRZYMUJESZ */}
      <section className="py-12 px-4 bg-white">
        <h2 className="text-2xl font-bold text-center text-gray-900 mb-2">
          Co otrzymujesz?
        </h2>
        <p className="text-center text-gray-500 mb-8">
          Wszystko bezpłatnie — bez ukrytych opłat.
        </p>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 max-w-2xl mx-auto">
          {/* Card 1 */}
          <div className="flex flex-col items-center text-center p-4 rounded-xl border border-gray-100 shadow-sm">
            <div className="w-12 h-12 rounded-full bg-orange-500 flex items-center justify-center mb-3">
              <BarChart2 className="w-6 h-6 text-white" />
            </div>
            <p className="font-semibold text-gray-900 text-sm">Statystyki profilu</p>
            <p className="text-gray-500 text-xs mt-1">Widzisz ilu klientów oglądało Twój profil</p>
          </div>
          {/* Card 2 */}
          <div className="flex flex-col items-center text-center p-4 rounded-xl border border-gray-100 shadow-sm">
            <div className="w-12 h-12 rounded-full bg-orange-500 flex items-center justify-center mb-3">
              <Search className="w-6 h-6 text-white" />
            </div>
            <p className="font-semibold text-gray-900 text-sm">Widoczność w Google</p>
            <p className="text-gray-500 text-xs mt-1">Twój profil pojawia się w wynikach wyszukiwania</p>
          </div>
          {/* Card 3 */}
          <div className="flex flex-col items-center text-center p-4 rounded-xl border border-gray-100 shadow-sm">
            <div className="w-12 h-12 rounded-full bg-orange-500 flex items-center justify-center mb-3">
              <LayoutTemplate className="w-6 h-6 text-white" />
            </div>
            <p className="font-semibold text-gray-900 text-sm">Widget na stronę</p>
            <p className="text-gray-500 text-xs mt-1">Wstaw profil na swoją stronę lub Instagram bio</p>
          </div>
          {/* Card 4 */}
          <div className="flex flex-col items-center text-center p-4 rounded-xl border border-gray-100 shadow-sm">
            <div className="w-12 h-12 rounded-full bg-orange-500 flex items-center justify-center mb-3">
              <QrCode className="w-6 h-6 text-white" />
            </div>
            <p className="font-semibold text-gray-900 text-sm">Kod QR</p>
            <p className="text-gray-500 text-xs mt-1">Drukuj na wizytówce, naklejce lub drzwiach</p>
          </div>
          {/* Card 5 */}
          <div className="flex flex-col items-center text-center p-4 rounded-xl border border-gray-100 shadow-sm">
            <div className="w-12 h-12 rounded-full bg-orange-500 flex items-center justify-center mb-3">
              <Star className="w-6 h-6 text-white" />
            </div>
            <p className="font-semibold text-gray-900 text-sm">Opinie klientów</p>
            <p className="text-gray-500 text-xs mt-1">Buduj reputację widoczną dla nowych klientów</p>
          </div>
          {/* Card 6 */}
          <div className="flex flex-col items-center text-center p-4 rounded-xl border border-gray-100 shadow-sm">
            <div className="w-12 h-12 rounded-full bg-orange-500 flex items-center justify-center mb-3">
              <BadgeCheck className="w-6 h-6 text-white" />
            </div>
            <p className="font-semibold text-gray-900 text-sm">Odznaka specjalisty</p>
            <p className="text-gray-500 text-xs mt-1">Wyróżnij się jako Top Specjalista w Warszawie</p>
          </div>
        </div>
      </section>

      <section className="py-8 px-4 text-center bg-white">
        <a
          href={`/${lang}/auth?mode=register`}
          className="bg-orange-500 text-white font-bold text-lg px-10 py-4 rounded-xl shadow-lg hover:bg-orange-600 hover:shadow-xl transition-all inline-block"
        >
          Utwórz bezpłatny profil →
        </a>
        <p className="text-sm text-gray-400 mt-3">Bezpłatnie • Bez zobowiązań • Zajmuje 2 minuty</p>
      </section>

      {/* CATEGORIES */}
      <section className="bg-gray-50 py-16 px-6">
        <h2 className="text-center text-2xl font-bold text-gray-900 mb-4">
          Dla kogo jest Nevumo?
        </h2>
        <p className="text-center text-gray-500 mb-10">
          Aktualnie przyjmujemy specjalistów w Warszawie:
        </p>

        <div className="flex flex-col md:flex-row gap-6 max-w-2xl mx-auto">
          {/* Card 1 - Hydraulik */}
          <div className="bg-white rounded-2xl p-6 text-center shadow-sm border border-gray-100 flex-1">
            <div className="text-orange-500 mb-3">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ff5a1f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
              </svg>
            </div>
            <h3 className="font-bold text-gray-900">Hydraulik</h3>
            <p className="text-sm text-gray-500 mt-1">Naprawy, instalacje, awarie 24h</p>
            <a
              href={`/${lang}/auth?mode=register&category=plumbing`}
              className="mt-4 inline-block text-orange-500 text-sm font-medium hover:underline"
            >
              Dołącz jako hydraulik →
            </a>
          </div>

          {/* Card 2 - Sprzątanie */}
          <div className="bg-white rounded-2xl p-6 text-center shadow-sm border border-gray-100 flex-1">
            <div className="text-orange-500 mb-3">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ff5a1f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>
                <path d="M20 3v4M22 5h-4M4 17v2M5 18H3"/>
              </svg>
            </div>
            <h3 className="font-bold text-gray-900">Sprzątanie</h3>
            <p className="text-sm text-gray-500 mt-1">Mieszkania, biura, po remoncie</p>
            <a
              href={`/${lang}/auth?mode=register&category=cleaning`}
              className="mt-4 inline-block text-orange-500 text-sm font-medium hover:underline"
            >
              Dołącz jako firma sprzątająca →
            </a>
          </div>

          {/* Card 3 - Masaż */}
          <div className="bg-white rounded-2xl p-6 text-center shadow-sm border border-gray-100 flex-1">
            <div className="text-orange-500 mb-3">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ff5a1f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
                <path d="M12 5 9.04 7.96a2.17 2.17 0 0 0 0 3.08c.82.82 2.13.85 3 .07l2.07-1.9a2.82 2.82 0 0 1 3.79 0l2.96 2.66"/>
                <path d="m18 15-2-2"/>
                <path d="m15 18-2-2"/>
              </svg>
            </div>
            <h3 className="font-bold text-gray-900">Masaż</h3>
            <p className="text-sm text-gray-500 mt-1">Relaksacyjny, leczniczy, sportowy</p>
            <a
              href={`/${lang}/auth?mode=register&category=massage`}
              className="mt-4 inline-block text-orange-500 text-sm font-medium hover:underline"
            >
              Dołącz jako masażysta →
            </a>
          </div>
        </div>
      </section>

      {/* TRUST BAR */}
      <section className="bg-white py-12 px-6 border-t border-gray-100">
        <div className="flex flex-col md:flex-row gap-8 max-w-3xl mx-auto text-center">
          {/* Item 1 */}
          <div className="flex-1">
            <div className="text-3xl mb-2">🆓</div>
            <p className="font-semibold text-gray-900">100% bezpłatnie przez 6 miesięcy</p>
            <p className="text-sm text-gray-500 mt-1">Bez ukrytych opłat</p>
          </div>

          {/* Item 2 */}
          <div className="flex-1">
            <div className="text-3xl mb-2">📱</div>
            <p className="font-semibold text-gray-900">Bezpośredni kontakt z klientem</p>
            <p className="text-sm text-gray-500 mt-1">Bez pośredników</p>
          </div>

          {/* Item 3 */}
          <div className="flex-1">
            <div className="text-3xl mb-2">🏆</div>
            <p className="font-semibold text-gray-900">Rośniesz w rankingu</p>
            <p className="text-sm text-gray-500 mt-1">Im więcej zleceń, tym wyżej w wynikach</p>
          </div>
        </div>
      </section>

      {/* FINAL CTA */}
      <section className="bg-orange-500 py-16 px-6 text-center text-white">
        <h2 className="text-3xl font-bold">Gotowy na więcej zleceń?</h2>
        <p className="text-white font-semibold text-base mt-2 mb-6 max-w-md mx-auto">
          Im wcześniej dołączysz — tym wyżej w rankingu i tym bardziej widoczny w Google.
        </p>
        <p className="text-orange-100 mt-3 text-lg">
          Dołącz do Nevumo już dziś — rejestracja zajmuje 2 minuty.
        </p>

        <a
          href={`/${lang}/auth?mode=register`}
          className="mt-8 bg-white text-orange-600 font-bold text-lg px-10 py-4 rounded-xl shadow-lg hover:bg-orange-50 hover:shadow-xl transition-all inline-block"
        >
          Zacznij teraz — to nic nie kosztuje
        </a>
      </section>
    </div>
  );
}
