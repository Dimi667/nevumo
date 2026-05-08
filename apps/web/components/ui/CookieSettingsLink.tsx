'use client';

import { useTranslation } from '@/lib/use-translation';

interface CookieSettingsLinkProps {
  lang: string;
  className?: string;
}

export function CookieSettingsLink({ lang, className = '' }: CookieSettingsLinkProps) {
  const { t } = useTranslation('cookie_banner', lang);

  const handleClick = () => {
    // Dispatch custom event to open cookie banner
    window.dispatchEvent(new CustomEvent('open-cookie-settings'));
  };

  return (
    <button
      onClick={handleClick}
      className={`text-gray-700 transition-colors hover:text-orange-600 ${className}`}
    >
      {t('cookie_settings_link', 'Cookie Settings')}
    </button>
  );
}
