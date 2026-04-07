interface PageProps {
  params: Promise<{ lang: string }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { lang } = await params;

  return {
    title: 'Zdobywaj klientów na usługi w Warszawie — Nevumo',
    description: 'Dołącz do Nevumo i otrzymuj zapytania od klientów bezpośrednio na swój telefon. Bezpłatnie, bez prowizji.',
  };
}

export default async function DolaczPage({ params }: PageProps) {
  const { lang } = await params;

  return (
    <div className="bg-white">
      {/* TOP BAR */}
      <header className="border-b border-gray-100 py-4 px-6">
        <div className="flex justify-between items-center">
          <span>
            <span className="text-orange-500 font-bold text-xl">N</span>
            <span className="font-bold text-xl text-gray-900">evumo</span>
          </span>
          <a
            href={`/${lang}/warszawa/sprzatanie`}
            className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
          >
            Szukasz usługi?
          </a>
        </div>
      </header>

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
          className="mt-8 bg-white text-orange-600 font-bold text-lg px-10 py-4 rounded-xl hover:bg-orange-50 transition-colors inline-block"
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
            <div className="text-4xl mb-3">🔧</div>
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
            <div className="text-4xl mb-3">🧹</div>
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
            <div className="text-4xl mb-3">💆</div>
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
            <div className="text-3xl mb-2">🔍</div>
            <p className="font-semibold text-gray-900">Widoczność w Google</p>
            <p className="text-sm text-gray-500 mt-1">Twój profil w wynikach wyszukiwania</p>
          </div>
        </div>
      </section>

      {/* FINAL CTA */}
      <section className="bg-orange-500 py-16 px-6 text-center text-white">
        <h2 className="text-3xl font-bold">Gotowy na więcej zleceń?</h2>
        <p className="text-orange-100 mt-3 text-lg">
          Dołącz do Nevumo już dziś — rejestracja zajmuje 2 minuty.
        </p>

        <a
          href={`/${lang}/auth?mode=register`}
          className="mt-8 bg-white text-orange-600 font-bold text-lg px-10 py-4 rounded-xl hover:bg-orange-50 transition-colors inline-block"
        >
          Zacznij teraz — to nic nie kosztuje
        </a>
      </section>
    </div>
  );
}
