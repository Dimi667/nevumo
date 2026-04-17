'use client';

import { useEffect, useMemo, useState } from 'react';
import { fetchTranslations, type TranslationDict } from './ui-translations';

interface UseTranslationResult {
  t: (key: string, fallback?: string) => string;
  dict: TranslationDict;
  isLoading: boolean;
}

export function useTranslation(namespace: string, lang: string): UseTranslationResult {
  const [dict, setDict] = useState<TranslationDict>({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function loadTranslations(): Promise<void> {
      setIsLoading(true);
      const translations = await fetchTranslations(lang, namespace);
      if (!cancelled) {
        setDict(translations);
        setIsLoading(false);
      }
    }

    void loadTranslations();

    return () => {
      cancelled = true;
    };
  }, [lang, namespace]);

  const t = useMemo(
    () => (key: string, fallback = ''): string => {
      if (!dict || !key) return fallback;
      const cleanKey = key.trim();
      const value = dict[cleanKey] ?? fallback;
      console.log('[use-translation] Final translation source:', cleanKey, 'value:', value, 'from dict:', !!dict[cleanKey]);
      return value;
    },
    [dict],
  );

  return { t, dict, isLoading };
}
