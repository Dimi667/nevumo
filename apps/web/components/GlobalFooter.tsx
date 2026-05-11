'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import {
  SUPPORTED_LANGUAGES,
  LANGUAGE_DISPLAY_NAMES,
  LANGUAGE_FLAGS,
  LANGUAGE_COOKIE_NAME,
} from '@/lib/locales';

interface GlobalFooterProps {
  lang: string;
  minimal?: boolean;
}

export default function GlobalFooter({ lang, minimal = false }: GlobalFooterProps) {
  const router = useRouter();
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const dropdownRef = useRef<HTMLDivElement>(null);

  const currentYear = new Date().getFullYear();

  // Filter languages based on search query
  const filteredLanguages = SUPPORTED_LANGUAGES.filter((langCode) => {
    const displayName = LANGUAGE_DISPLAY_NAMES[langCode] || '';
    return displayName.toLowerCase().includes(searchQuery.toLowerCase());
  });

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    if (isOpen) {
      document.addEventListener('click', handleClickOutside);
    }

    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, [isOpen]);

  const handleLanguageChange = (newLang: string) => {
    // Replace lang segment in pathname
    const pathSegments = pathname.split('/').filter(Boolean);
    if (pathSegments.length > 0 && SUPPORTED_LANGUAGES.includes(pathSegments[0])) {
      pathSegments[0] = newLang;
    } else {
      pathSegments.unshift(newLang);
    }
    const newPathname = `/${pathSegments.join('/')}`;

    // Set cookie
    document.cookie = `${LANGUAGE_COOKIE_NAME}=${newLang}; path=/; max-age=2592000`;

    // Navigate
    router.push(newPathname);
    setIsOpen(false);
  };

  const footerClasses = minimal
    ? 'border-t border-gray-100 bg-white py-4 px-4'
    : 'border-t border-gray-200 bg-white py-8 px-4';

  const footerFlexClasses = minimal
    ? 'justify-end'
    : 'justify-between items-center flex-wrap gap-4';

  return (
    <footer className={footerClasses}>
      <div className={`flex ${footerFlexClasses}`}>
        {!minimal && (
          <div className="text-gray-600 text-sm">
            © {currentYear} Nevumo
          </div>
        )}

        <div className="relative" ref={dropdownRef}>
          <button
            type="button"
            onClick={() => setIsOpen(!isOpen)}
            aria-expanded={isOpen}
            aria-haspopup="listbox"
            className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-md border border-gray-200"
          >
            <span>{LANGUAGE_FLAGS[lang] || '🌐'}</span>
            <span>{LANGUAGE_DISPLAY_NAMES[lang] || lang}</span>
            <svg
              className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </button>

          {isOpen && (
            <div className="absolute bottom-full right-0 mb-2 w-64 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
              <div className="p-3 border-b border-gray-100">
                <input
                  type="text"
                  placeholder="Search..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  aria-label="Search language"
                  className="w-full px-3 py-2 text-sm border border-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="max-h-64 overflow-y-auto" role="listbox">
                {filteredLanguages.map((langCode) => {
                  const isActive = langCode === lang;
                  return (
                    <button
                      key={langCode}
                      type="button"
                      lang={langCode}
                      onClick={() => handleLanguageChange(langCode)}
                      className={`w-full flex items-center gap-2 px-3 py-2 text-sm text-left ${
                        isActive
                          ? 'bg-gray-100 font-medium text-gray-900'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                      role="option"
                      aria-selected={isActive}
                    >
                      <span>{LANGUAGE_FLAGS[langCode] || '🌐'}</span>
                      <span>{LANGUAGE_DISPLAY_NAMES[langCode] || langCode}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>
    </footer>
  );
}
