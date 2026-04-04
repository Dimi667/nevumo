import { SUPPORTED_LANGUAGES } from '@/lib/locales';
import { generateHreflangAlternates } from '@/lib/seo';
import Image from 'next/image';
import RotatingCategory from '@/components/homepage/RotatingCategory';

interface PageProps {
  params: Promise<{ lang: string }>;
}

export async function generateMetadata({ params }: PageProps) {
  return {
    title: "Zdobądź klientów na swoje usługi w Warszawie | Nevumo",
    description: "Pozyskuj klientów na sprzątanie, hydraulikę lub masaż w Warszawie. Bezpłatna rejestracja. Zero prowizji.",
    alternates: {
      languages: generateHreflangAlternates('/'),
    },
  };
}

export default async function Homepage({ params }: PageProps) {
  const { lang } = await params;
  const normalizedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : 'en';

  return (
    <div className="min-h-screen bg-white">
      {/* NAVBAR */}
      <nav className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto">
        <Image 
          src="/Nevumo_logo.svg" 
          alt="Nevumo" 
          width={120} 
          height={36}
          priority
        />
        <a 
          href={`/${normalizedLang}/warszawa/sprzatanie`}
          className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
        >
          Szukasz usługi?
        </a>
      </nav>

      {/* HERO SECTION */}
      <section style={{ background: 'linear-gradient(135deg, #fb923c 0%, #c2410c 100%)' }} className="py-24 px-4 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-4">
            Otrzymuj klientów na{' '}
            <RotatingCategory categories={['Masaż', 'Sprzątanie', 'Hydraulik']} />
            {' '}w Warszawie
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-white">
            Bezpłatnie. Bez prowizji. Bezpośredni kontakt.
          </p>
          
          <div className="flex flex-wrap justify-center gap-6 mb-8 text-sm md:text-base">
            <span className="flex items-center gap-2 text-white">
              <span className="text-white">✓</span> Bez prowizji
            </span>
            <span className="flex items-center gap-2 text-white">
              <span className="text-white">✓</span> Rejestracja 2 minuty
            </span>
            <span className="flex items-center gap-2 text-white">
              <span className="text-white">✓</span> Prawdziwe zapytania
            </span>
          </div>
          
          <div className="text-lg mb-10 text-orange-100">
            47 specjalistów • 120 zapytań w tym miesiącu
          </div>
          
          <a 
            href={`/${normalizedLang}/auth`}
            className="bg-white text-orange-600 font-bold px-8 py-4 rounded-full hover:bg-orange-50 transition"
          >
            Zacznij za darmo
          </a>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="bg-gray-100 py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">Jak to działa</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">Utwórz profil</h3>
              <p className="text-gray-600">2 minuty</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">Otrzymujesz zapytania od klientów</h3>
              <p className="text-gray-600">od razu po rejestracji</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">Kontaktujesz się bezpośrednio</h3>
              <p className="text-gray-600">bez pośredników</p>
            </div>
          </div>
        </div>
      </section>

      {/* CATEGORY CARDS */}
      <section className="py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="nevumo-card text-center">
              <div className="text-orange-500 mb-3">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M3 3l18 18M8.5 8.5L5 19l7-3"/><path d="M14.5 14.5L19 5l-7 3"/></svg>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">Sprzątanie</h3>
              <p className="text-gray-600 mb-6">26 zapytań w tym tygodniu</p>
              <a 
                href={`/${normalizedLang}/auth?category=cleaning`}
                className="btn-primary w-full"
              >
                Oferuję tę usługę
              </a>
            </div>
            <div className="nevumo-card text-center">
              <div className="text-orange-500 mb-3">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">Hydraulik</h3>
              <p className="text-gray-600 mb-6">18 zapytań w tym tygodniu</p>
              <a 
                href={`/${normalizedLang}/auth?category=plumbing`}
                className="btn-primary w-full"
              >
                Oferuję tę usługę
              </a>
            </div>
            <div className="nevumo-card text-center">
              <div className="text-orange-500 mb-3">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-900">Masaż</h3>
              <p className="text-gray-600 mb-6">14 zapytań w tym tygodniu</p>
              <a 
                href={`/${normalizedLang}/auth?category=massage`}
                className="btn-primary w-full"
              >
                Oferuję tę usługę
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* LIVE ACTIVITY FEED */}
      <section className="py-16 px-6 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">Ostatnie zapytania</h2>
          <div className="space-y-4">
            <div className="nevumo-card flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-red-500">🔴</span>
                <span className="text-gray-900">Krzysztof z Warszawy szuka sprzątania</span>
              </div>
              <span className="text-gray-500 text-sm">8 min temu</span>
            </div>
            <div className="nevumo-card flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-red-500">🔴</span>
                <span className="text-gray-900">Anna z Warszawy szuka masażu</span>
              </div>
              <span className="text-gray-500 text-sm">1 godz. temu</span>
            </div>
            <div className="nevumo-card flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-red-500">🔴</span>
                <span className="text-gray-900">Marek z Warszawy szuka hydraulika</span>
              </div>
              <span className="text-gray-500 text-sm">3 godz. temu</span>
            </div>
          </div>
        </div>
      </section>

      {/* WHY NEVUMO */}
      <section className="py-16 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-12 text-gray-900">Dlaczego specjaliści wybierają Nevumo</h2>
          <div className="space-y-6 text-left max-w-2xl mx-auto">
            <div className="flex items-start gap-3">
              <span className="text-green-500 text-xl mt-1">✓</span>
              <div>
                <h3 className="font-semibold text-gray-900">Bezpłatnie</h3>
                <p className="text-gray-600">bez ukrytych opłat</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-green-500 text-xl mt-1">✓</span>
              <div>
                <h3 className="font-semibold text-gray-900">Bezpośredni kontakt z klientami</h3>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-green-500 text-xl mt-1">✓</span>
              <div>
                <h3 className="font-semibold text-gray-900">Profil + strona SEO, która pracuje za ciebie 24/7</h3>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SECOND CTA */}
      <section className="py-20 px-6 bg-gray-100" id="second-cta">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-8 text-gray-900">Gotowy na nowych klientów?</h2>
          <a 
            href={`/${normalizedLang}/auth`}
            className="btn-primary text-lg px-8 py-4 inline-block"
          >
            Utwórz bezpłatny profil
          </a>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="py-12 px-6 bg-gray-50 border-t border-gray-200">
        <div className="max-w-4xl mx-auto text-center">
          <p className="mb-6 text-gray-700">Szukasz usługi w Warszawie?</p>
          <div className="flex flex-wrap justify-center gap-4 mb-6 text-sm">
            <a href={`/${normalizedLang}/warszawa/sprzatanie`} className="text-gray-700 hover:text-orange-500 transition-colors">
              Sprzątanie w Warszawie
            </a>
            <span className="text-gray-500">|</span>
            <a href={`/${normalizedLang}/warszawa/hydraulik`} className="text-gray-700 hover:text-orange-500 transition-colors">
              Hydraulik w Warszawie
            </a>
            <span className="text-gray-500">|</span>
            <a href={`/${normalizedLang}/warszawa/masaz`} className="text-gray-700 hover:text-orange-500 transition-colors">
              Masaż w Warszawie
            </a>
          </div>
          <p className="text-gray-500 text-sm">
            Popularne: <a href={`/${normalizedLang}/warszawa/masaz`} className="text-gray-500 hover:text-orange-500 transition-colors">Masaż</a> • <a href={`/${normalizedLang}/warszawa/sprzatanie`} className="text-gray-500 hover:text-orange-500 transition-colors">Sprzątanie</a> • <a href={`/${normalizedLang}/warszawa/hydraulik`} className="text-gray-500 hover:text-orange-500 transition-colors">Hydraulik</a>
          </p>
        </div>
      </footer>

      {/* MOBILE STICKY CTA */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 z-50 transition-transform duration-300" id="mobile-sticky-cta">
        <a 
          href={`/${normalizedLang}/auth`}
          className="btn-primary w-full text-center block"
        >
          Zacznij za darmo
        </a>
      </div>

      <script dangerouslySetInnerHTML={{
        __html: `
          if (typeof window !== 'undefined') {
            const mobileStickyCTA = document.getElementById('mobile-sticky-cta');
            const secondCTA = document.getElementById('second-cta');
            
            if (mobileStickyCTA && secondCTA) {
              const observer = new IntersectionObserver(
                (entries) => {
                  entries.forEach(entry => {
                    if (entry.isIntersecting) {
                      mobileStickyCTA.style.transform = 'translateY(100%)';
                    } else {
                      mobileStickyCTA.style.transform = 'translateY(0)';
                    }
                  });
                },
                { threshold: 0.1 }
              );
              
              observer.observe(secondCTA);
            }
          }
        `
      }} />
    </div>
  );
}
