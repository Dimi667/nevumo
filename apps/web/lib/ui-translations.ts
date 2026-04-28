import { SUPPORTED_LANGUAGES } from './locales';

export type TranslationDict = Record<string, string>

export async function fetchTranslations(
  lang: string,
  namespace: string
): Promise<TranslationDict> {
  const resolvedLang = SUPPORTED_LANGUAGES.includes(lang) ? lang : 'en';

  const apiBase = typeof window === 'undefined'
    ? (process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000')
    : (process.env.NEXT_PUBLIC_API_URL || '');

  try {
    const res = await fetch(
      `${apiBase}/api/v1/translations/${namespace}?lang=${resolvedLang}`,
      { cache: 'no-store', next: { revalidate: 0 } }
    );
    if (!res.ok) throw new Error('Failed to fetch translations');
    const json = (await res.json()) as TranslationDict;
    return json || {};
  } catch {
    return {};
  }
}

export function t(dict: TranslationDict, key: string, fallback = ''): string {
  if (!dict || !key) return fallback;
  const cleanKey = key.trim(); // Защита срещу случайно попадали интервали в бъдеще
  return dict[cleanKey] ?? fallback;
}

// Server-side helper: uses the already namespaced dictionary
export function createScopedT(namespace: string, dict: TranslationDict) {
  return (key: string, fallback = ''): string => {
    if (!dict || !key) return fallback;
    const cleanKey = key.trim();
    return dict[cleanKey] ?? fallback;
  };
}
