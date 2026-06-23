'use client';

import Link from 'next/link';

interface ClaimProfileBannerProps {
  businessName: string;
  lang: string;
  claimToken: string;
  searchVolume: number | null;
  categoryLabel: string;
  cityLabel: string;
  translations: {
    title: string;
    subtitle: string;
    desc: string;
    cta: string;
    trust: string;
  };
}

export default function ClaimProfileBanner({
  businessName,
  lang,
  claimToken,
  searchVolume,
  categoryLabel,
  cityLabel,
  translations,
}: ClaimProfileBannerProps) {
  const formatDesc = () => {
    let desc = translations.desc;
    if (searchVolume === null) {
      desc = desc.replace('{count} ', '');
    } else {
      desc = desc.replace('{count}', searchVolume.toLocaleString(lang));
    }
    desc = desc.replace('{category}', categoryLabel);
    desc = desc.replace('{city}', cityLabel);
    return desc;
  };

  const subtitle = translations.subtitle.replace('{businessName}', businessName);

  return (
    <div className="bg-gradient-to-r from-orange-500 to-orange-600 py-4 px-6 rounded-xl mb-6">
      <div className="flex flex-col md:flex-row md:justify-between md:items-center gap-3">
        {/* Left side */}
        <div className="flex flex-col">
          <span className="text-orange-100 text-sm font-medium">
            {translations.title}
          </span>
          <h2 className="text-white text-lg font-bold">
            {subtitle}
          </h2>
          <p className="text-orange-100 text-sm">
            {formatDesc()}
          </p>
        </div>

        {/* Right side */}
        <div className="flex flex-col items-center">
          <Link
            href={`/${lang}/claim/${claimToken}?source=banner`}
            className="bg-white text-orange-600 font-semibold px-6 py-2.5 rounded-lg hover:bg-orange-50 transition-colors whitespace-nowrap text-sm"
          >
            {translations.cta}
          </Link>
          <span className="text-orange-100 text-xs text-center mt-1">
            {translations.trust}
          </span>
        </div>
      </div>
    </div>
  );
}
