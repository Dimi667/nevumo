/**
 * Shared logic for dynamic prepositions (e.g., "in" -> "we" in PL, "във" in BG)
 */
export function getLocalizedCityText(text: string, lang: string, cityName: string, cityT: any) {
  // Backend strips namespace prefix, so keys are without "city." prefix
  const prepBase = cityT['preposition_base'] || 'in';
  const prepModified = cityT['preposition_modified'] || prepBase;
  const firstChar = cityName.charAt(0).toLowerCase();
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

  return text
    .replace(` ${prepBase} `, ` ${preposition} `)
    .replace(` ${prepBase} {city}`, ` ${preposition} {city}`)
    .replace('{city}', cityName);
}
