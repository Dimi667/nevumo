'use client';

import {
  createContext,
  useContext,
  type ReactNode,
} from 'react';
import { useTranslation } from './use-translation';

interface DashboardI18nContextValue {
  t: (key: string, fallback?: string) => string;
  lang: string;
  isLoading: boolean;
}

interface DashboardI18nProviderProps {
  children: ReactNode;
  lang: string;
}

const DashboardI18nContext = createContext<DashboardI18nContextValue | null>(null);

export function DashboardI18nProvider({ children, lang }: DashboardI18nProviderProps) {
  const { t, isLoading } = useTranslation('provider_dashboard', lang);

  const value = {
    t,
    lang,
    isLoading,
  };

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
