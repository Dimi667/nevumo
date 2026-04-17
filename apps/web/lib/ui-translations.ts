export type TranslationDict = Record<string, string>

export async function fetchTranslations(
  lang: string,
  namespace: string
): Promise<TranslationDict> {
  const supportedLangs = [
    'bg', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'fi', 'fr', 'ga', 'hr', 'hu',
    'is', 'it', 'lb', 'lt', 'lv', 'mk', 'mt', 'nl', 'no', 'pl', 'pt', 'pt-PT',
    'ro', 'ru', 'sk', 'sl', 'sq', 'sr', 'sv', 'tr', 'uk',
  ];
  const resolvedLang = supportedLangs.includes(lang) ? lang : 'en';

  const apiBase = typeof window === 'undefined'
    ? (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000')
    : '';

  try {
    const res = await fetch(
      `${apiBase}/api/v1/translations/${namespace}?lang=${resolvedLang}`,
      { cache: 'no-store' }
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
