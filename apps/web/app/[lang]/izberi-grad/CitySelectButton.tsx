'use client';

import { setCtx } from '@/lib/ctx';

interface CitySelectButtonProps {
  slug: string;
  lang: string;
  children: React.ReactNode;
}

export default function CitySelectButton({ slug, lang, children }: CitySelectButtonProps) {
  const handleClick = () => {
    document.cookie = `nevumo_city=${slug}; path=/; max-age=31536000; SameSite=Lax`;
    setCtx({ city: slug });
    window.location.href = `/${lang}/${slug}`;
  };

  return (
    <button onClick={handleClick} className="nevumo-card flex items-center justify-between hover:border-orange-500 hover:shadow-md transition-all group w-full text-left">
      {children}
    </button>
  );
}
