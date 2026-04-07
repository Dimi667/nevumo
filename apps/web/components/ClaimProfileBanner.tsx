'use client';

interface ClaimProfileBannerProps {
  businessName: string;
  lang: string;
}

export default function ClaimProfileBanner({ businessName, lang }: ClaimProfileBannerProps) {
  return (
    <div className="bg-gradient-to-r from-orange-500 to-orange-600 py-4 px-6 rounded-xl mb-6">
      <div className="flex flex-col md:flex-row md:justify-between md:items-center gap-3">
        {/* Left side */}
        <div className="flex flex-col">
          <span className="text-orange-100 text-sm font-medium">
            🏆 Czy to Twoja firma?
          </span>
          <h2 className="text-white text-lg font-bold">
            Odbierz bezpłatny profil dla {businessName}
          </h2>
          <p className="text-orange-100 text-sm">
            Zacznij otrzymywać zapytania od klientów już dziś — to nic nie kosztuje.
          </p>
        </div>

        {/* Right side */}
        <div className="flex flex-col items-center">
          <a
            href={`/${lang}/dolacz`}
            className="bg-white text-orange-600 font-semibold px-6 py-2.5 rounded-lg hover:bg-orange-50 transition-colors whitespace-nowrap text-sm"
          >
            Odbierz profil bezpłatnie →
          </a>
          <span className="text-orange-100 text-xs text-center mt-1">
            Bezpłatnie • Zajmuje 2 minuty
          </span>
        </div>
      </div>
    </div>
  );
}
