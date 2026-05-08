'use client';

import { useState, useEffect } from 'react';
import { useCookieConsent, type ConsentCategories } from '@/hooks/useCookieConsent';
import { useTranslation } from '@/lib/use-translation';
import { CookieSettingsButton } from '@/components/ui/CookieSettingsButton';

interface CookieConsentBannerProps {
  lang: string;
}

export default function CookieConsentBanner({ lang }: CookieConsentBannerProps) {
  const { showBanner, saveConsent, acceptAll, rejectAll, consentData, openSettings } = useCookieConsent();
  const { t } = useTranslation('cookie_banner', lang);
  const [isExpanded, setIsExpanded] = useState(false);
  const [preferences, setPreferences] = useState<ConsentCategories>(() => {
    const defaults: ConsentCategories = {
      necessary: true,
      functional: false,
      analytics: false,
      marketing: false,
    };

    if (typeof window === 'undefined') return defaults;

    try {
      const name = 'nevumo_consent';
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      const cookieValue = parts.length === 2 ? parts.pop()?.split(';').shift() : null;
      
      if (cookieValue) {
        const data = JSON.parse(decodeURIComponent(cookieValue));
        if (data && data.categories) {
          return { ...defaults, ...data.categories };
        }
      }
    } catch (e) {
      // Fallback to defaults if parsing fails
    }

    return defaults;
  });

  useEffect(() => {
    if (isExpanded && consentData?.categories) {
      setPreferences(consentData.categories);
    }
  }, [isExpanded]);

  // Listen for custom event to open settings
  useEffect(() => {
    const handleOpenSettings = () => {
      openSettings();
    };

    window.addEventListener('open-cookie-settings', handleOpenSettings);
    return () => window.removeEventListener('open-cookie-settings', handleOpenSettings);
  }, [openSettings]);

  if (!showBanner) return null;

  const handleSavePreferences = async () => {
    await saveConsent(preferences);
  };

  const togglePreference = (key: keyof ConsentCategories) => {
    if (key === 'necessary') return;
    setPreferences((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="fixed bottom-0 left-0 right-0 z-[9999] bg-gray-900 text-white p-4 md:p-6 shadow-2xl transition-all duration-300">
      <div className="max-w-7xl mx-auto">
        {!isExpanded ? (
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex-1 text-center md:text-left">
              <h3 className="text-lg font-bold mb-1">{t('cookie_title', 'We value your privacy')}</h3>
              <p className="text-sm text-gray-300">
                {t('cookie_description', 'We use cookies to enhance your browsing experience and analyze our traffic.')}
              </p>
            </div>
            <div className="flex flex-wrap items-center justify-center gap-2 w-full md:w-auto">
              <button
                onClick={() => setIsExpanded(true)}
                className="flex-1 md:flex-none min-w-[120px] min-h-[44px] px-4 py-2 text-sm font-semibold bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
              >
                {t('customize', 'Customize')}
              </button>
              <button
                onClick={() => rejectAll()}
                className="flex-1 md:flex-none min-w-[120px] min-h-[44px] px-4 py-2 text-sm font-semibold bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
              >
                {t('reject_all', 'Reject All')}
              </button>
              <button
                onClick={() => acceptAll()}
                className="flex-1 md:flex-none min-w-[120px] min-h-[44px] px-4 py-2 text-sm font-semibold bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
              >
                {t('accept_all', 'Accept All')}
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-gray-700 pb-4">
              <h3 className="text-xl font-bold">{t('cookie_settings_link', 'Cookie Preferences')}</h3>
              <div className="flex items-center gap-4">
                <CookieSettingsButton
                  onOpen={openSettings}
                  className="text-gray-400 text-sm hover:text-white transition-colors"
                >
                  {t('cookie_settings_link', 'Cookie Settings')}
                </CookieSettingsButton>
                <button
                  onClick={() => setIsExpanded(false)}
                  className="text-gray-400 hover:text-white"
                >
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                </button>
              </div>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
              <CategoryRow
                title={t('necessary_label', 'Strictly Necessary')}
                description={t('necessary_description', 'Required for the website to function properly.')}
                enabled={true}
                disabled={true}
                onChange={() => {}}
              />
              <CategoryRow
                title={t('functional_label', 'Functional')}
                description={t('functional_description', 'Remember your preferences and settings.')}
                enabled={preferences.functional}
                onChange={() => togglePreference('functional')}
              />
              <CategoryRow
                title={t('analytics_label', 'Analytics')}
                description={t('analytics_description', 'Help us understand how visitors interact with the site.')}
                enabled={preferences.analytics}
                onChange={() => togglePreference('analytics')}
              />
              <CategoryRow
                title={t('marketing_label', 'Marketing')}
                description={t('marketing_description', 'Used to deliver relevant advertisements.')}
                enabled={preferences.marketing}
                onChange={() => togglePreference('marketing')}
              />
            </div>

            <div className="flex flex-wrap items-center justify-end gap-3 pt-4 border-t border-gray-700">
              <button
                onClick={() => rejectAll()}
                className="min-w-[120px] min-h-[44px] px-6 py-2 text-sm font-semibold bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
              >
                {t('reject_all', 'Reject All')}
              </button>
              <button
                onClick={() => acceptAll()}
                className="min-w-[120px] min-h-[44px] px-6 py-2 text-sm font-semibold bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
              >
                {t('accept_all', 'Accept All')}
              </button>
              <button
                onClick={handleSavePreferences}
                className="min-w-[120px] min-h-[44px] px-6 py-2 text-sm font-semibold bg-orange-500 hover:bg-orange-600 rounded-lg transition-colors"
              >
                {t('save_preferences', 'Save Preferences')}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

interface CategoryRowProps {
  title: string;
  description: string;
  enabled: boolean;
  disabled?: boolean;
  onChange: () => void;
}

function CategoryRow({ title, description, enabled, disabled, onChange }: CategoryRowProps) {
  return (
    <div className="flex items-start justify-between gap-4">
      <div className="flex-1">
        <h4 className="font-semibold text-white">{title}</h4>
        <p className="text-xs text-gray-400 mt-1">{description}</p>
      </div>
      <button
        onClick={onChange}
        disabled={disabled}
        className={`relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none ${
          enabled ? 'bg-orange-500' : 'bg-gray-700'
        } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <span
          className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
            enabled ? 'translate-x-5' : 'translate-x-0'
          }`}
        />
      </button>
    </div>
  );
}
