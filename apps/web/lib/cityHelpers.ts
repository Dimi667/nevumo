/**
 * Shared logic for dynamic prepositions (e.g., "in" -> "we" in PL, "във" in BG)
 */
export function getLocalizedCityText(
  text: string,
  lang: string,
  cityName: string,
  cityT: any,
  grammaticalCase: 'nominative' | 'locative' | 'genitive' = 'nominative'
) {
  // 1. Resolve city name based on case
  let resolvedCityName = cityName;
  if (grammaticalCase === 'locative' && cityT['locative_form']) {
    resolvedCityName = cityT['locative_form'];
  } else if (grammaticalCase === 'genitive' && cityT['genitive_form']) {
    resolvedCityName = cityT['genitive_form'];
  }

  // 2. Preposition logic
  const prepBase = cityT['preposition_base'] || 'in';
  const prepModified = cityT['preposition_modified'] || prepBase;
  const firstChar = resolvedCityName.charAt(0).toLowerCase();
  let preposition = prepBase;

  if (lang === 'bg' && (firstChar === 'в' || firstChar === 'ф' || firstChar === 'v' || firstChar === 'f')) {
    preposition = prepModified;
  } else if ((lang === 'cs' || lang === 'sk') && (firstChar === 'v' || firstChar === 'f')) {
    preposition = prepModified;
  } else if (lang === 'pl' && (firstChar === 'w' || firstChar === 'v')) {
    preposition = prepModified;
  } else if ((lang === 'ru' || lang === 'uk') && (firstChar === 'в' || firstChar === 'v')) {
    preposition = prepModified;
  }

  // 3. Replacements
  // Replace {city} first as requested
  let result = text.replace('{city}', resolvedCityName);

  // Apply preposition changes
  if (preposition !== prepBase) {
    // Handle " in " -> " we "
    result = result.split(` ${prepBase} `).join(` ${preposition} `);
    // Handle starting "in " -> "we "
    if (result.startsWith(`${prepBase} `)) {
      result = preposition + result.slice(prepBase.length);
    }
    // Handle "in" without leading space but with trailing space or end (e.g., "Category in {city}")
    result = result.replace(new RegExp(`\\b${prepBase}\\b`, 'g'), preposition);
  }

  return result;
}
