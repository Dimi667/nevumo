'use client';

import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react';
import { fetchTranslations, type TranslationDict } from '@/lib/ui-translations';

interface DashboardI18nContextValue {
  dict: TranslationDict;
  lang: string;
}

interface DashboardI18nProviderProps {
  children: ReactNode;
  lang: string;
}

const DashboardI18nContext = createContext<DashboardI18nContextValue | null>(null);

export function DashboardI18nProvider({ children, lang }: DashboardI18nProviderProps) {
  const [dict, setDict] = useState<TranslationDict>({});

  useEffect(() => {
    let cancelled = false;

    async function loadTranslations(): Promise<void> {
      const translations = await fetchTranslations(lang, 'provider_dashboard');
      if (!cancelled) {
        setDict(translations);
      }
    }

    void loadTranslations();

    return () => {
      cancelled = true;
    };
  }, [lang]);

  const value = useMemo(
    () => ({ dict, lang }),
    [dict, lang],
  );

  return (
    <DashboardI18nContext.Provider value={value}>
      {children}
    </DashboardI18nContext.Provider>
  );
}

export function useDashboardI18n(): DashboardI18nContextValue {
  const context = useContext(DashboardI18nContext);

  if (!context) {
    throw new Error('useDashboardI18n must be used within DashboardI18nProvider');
  }

  return context;
}

export function getDashboardDateLocale(lang: string): string {
  return lang === 'en' ? 'en-GB' : lang;
}

export function formatDashboardDate(
  value: string | number | Date,
  lang: string,
  options: Intl.DateTimeFormatOptions = {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  },
): string {
  const date = value instanceof Date ? value : new Date(value);

  if (Number.isNaN(date.getTime())) {
    return '';
  }

  return new Intl.DateTimeFormat(getDashboardDateLocale(lang), options).format(date);
}
