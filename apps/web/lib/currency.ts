/**
 * Universal currency logic for Nevumo.
 * Determines the currency based on country code and project-specific rules.
 */
export function getCurrency(countryCode: string | undefined, fallbackCurrency?: string): string {
  const normalizedCountry = countryCode?.toUpperCase();

  // Rule: For Bulgaria (BG), from 01.01.2026 the currency is always EUR.
  if (normalizedCountry === 'BG') {
    return 'EUR';
  }

  // If we have a currency from the API, use it (except for BG which is overridden above)
  if (fallbackCurrency) {
    return fallbackCurrency;
  }

  // General defaults by country
  if (normalizedCountry === 'RS') return 'RSD';
  if (normalizedCountry === 'PL') return 'PLN';

  return 'EUR';
}

/**
 * Formats price with the correct currency symbol/code.
 */
export function formatCurrency(price: number | null, currency: string): string {
  if (price === null) return '';
  
  // Use Intl.NumberFormat for proper formatting if needed, 
  // but following the project's existing simple style for now.
  if (currency === 'BGN') return `${price} лв.`;
  if (currency === 'EUR') return `€${price}`;
  if (currency === 'PLN') return `${price} zł`;
  if (currency === 'RSD') return `${price} RSD`;
  
  return `${price} ${currency}`;
}
