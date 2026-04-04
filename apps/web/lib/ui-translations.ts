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

  try {
    const res = await fetch(
      `http://localhost:8000/api/v1/translations?lang=${resolvedLang}&namespace=${namespace}`,
      { next: { revalidate: 3600 } }
    );
    if (!res.ok) throw new Error('Failed to fetch translations');
    const json = (await res.json()) as { data?: TranslationDict };
    return (json.data ?? {}) as TranslationDict;
  } catch {
    return {};
  }
}

export function t(dict: TranslationDict, key: string, fallback = ''): string {
  return dict[key] ?? fallback;
}
