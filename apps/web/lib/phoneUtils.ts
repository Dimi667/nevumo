// Country phone codes mapping
export const COUNTRY_PHONE_CODES = {
  "BG": "+359",
  "CZ": "+420", 
  "DK": "+45",
  "DE": "+49",
  "EE": "+372",
  "GR": "+30",
  "ES": "+34",
  "FR": "+33",
  "GA": "+353",  // Ireland
  "HR": "+385",
  "IT": "+39",
  "LV": "+371",
  "LT": "+370",
  "HU": "+36",
  "MT": "+356",
  "NL": "+31",
  "AT": "+43",
  "PL": "+48",
  "PT": "+351",
  "RO": "+40",
  "SK": "+421",
  "SI": "+386",
  "FI": "+358",
  "SE": "+46",
  "NO": "+47",
  "TR": "+90",
  "AL": "+355",
  "MK": "+389",
  "RS": "+381",
  "BA": "+387",
  "GB": "+44",
  "US": "+1",
  "CH": "+41",
};

// Phone validation patterns by country
export const PHONE_PATTERNS = {
  "BG": /^\+359\s?\d{9}$/,           // +359 888123456
  "CZ": /^\+420\s?\d{9}$/,           // +420 123456789
  "DK": /^\+45\s?\d{8}$/,            // +45 12345678
  "DE": /^\+49\s?\d{10,12}$/,        // +49 1234567890
  "EE": /^\+372\s?\d{7,8}$/,         // +372 1234567
  "GR": /^\+30\s?\d{10}$/,           // +30 2101234567
  "ES": /^\+34\s?\d{9}$/,            // +34 123456789
  "FR": /^\+33\s?\d{9}$/,            // +33 123456789
  "GA": /^\+353\s?\d{9}$/,           // +353 123456789
  "HR": /^\+385\s?\d{8,9}$/,         // +385 12345678
  "IT": /^\+39\s?\d{9,10}$/,         // +39 123456789
  "LV": /^\+371\s?\d{8}$/,           // +371 12345678
  "LT": /^\+370\s?\d{8}$/,           // +370 12345678
  "HU": /^\+36\s?\d{8,9}$/,          // +36 12345678
  "MT": /^\+356\s?\d{8}$/,           // +356 12345678
  "NL": /^\+31\s?\d{9}$/,            // +31 123456789
  "AT": /^\+43\s?\d{8,12}$/,         // +43 12345678
  "PL": /^\+48\s?\d{9}$/,            // +48 123456789
  "PT": /^\+351\s?\d{9}$/,           // +351 123456789
  "RO": /^\+40\s?\d{9}$/,            // +40 123456789
  "SK": /^\+421\s?\d{9}$/,           // +421 123456789
  "SI": /^\+386\s?\d{8,9}$/,         // +386 12345678
  "FI": /^\+358\s?\d{9,10}$/,        // +358 123456789
  "SE": /^\+46\s?\d{7,10}$/,         // +46 1234567
  "NO": /^\+47\s?\d{8}$/,            // +47 12345678
  "TR": /^\+90\s?\d{10}$/,           // +90 1234567890
  "AL": /^\+355\s?\d{8,9}$/,         // +355 12345678
  "MK": /^\+389\s?\d{8}$/,           // +389 12345678
  "RS": /^\+381\s?\d{8,10}$/,        // +381 12345678
  "BA": /^\+387\s?\d{8}$/,           // +387 12345678
  "GB": /^\+44\s?\d{10}$/,           // +44 1234567890
  "US": /^\+1\s?\d{10}$/,            // +1 1234567890
  "CH": /^\+41\s?\d{9}$/,            // +41 123456789
};

// Generic international phone pattern (fallback)
const GENERIC_PHONE_PATTERN = /^\+\d{1,4}\s?\d{6,14}$/;

export function validatePhone(phone: string, countryCode?: string): { isValid: boolean; error?: string } {
  if (!phone || phone.trim().length === 0) {
    return { isValid: false, error: "Phone number is required" };
  }

  const cleanPhone = phone.trim();
  
  // Try country-specific validation first
  if (countryCode && PHONE_PATTERNS[countryCode as keyof typeof PHONE_PATTERNS]) {
    const pattern = PHONE_PATTERNS[countryCode as keyof typeof PHONE_PATTERNS];
    if (pattern.test(cleanPhone)) {
      return { isValid: true };
    }
    return { 
      isValid: false, 
      error: `Invalid phone format for ${countryCode}. Expected format: ${getPhoneExample(countryCode)}` 
    };
  }
  
  // Fallback to generic validation
  if (GENERIC_PHONE_PATTERN.test(cleanPhone)) {
    return { isValid: true };
  }
  
  return { 
    isValid: false, 
    error: "Invalid international phone format. Use format: +[country code] [number]" 
  };
}

export function getPhonePlaceholder(countryCode?: string): string {
  if (countryCode && COUNTRY_PHONE_CODES[countryCode as keyof typeof COUNTRY_PHONE_CODES]) {
    const code = COUNTRY_PHONE_CODES[countryCode as keyof typeof COUNTRY_PHONE_CODES];
    switch (countryCode) {
      case "BG": return `${code} 888123456`;
      case "CZ": return `${code} 123456789`;
      case "DK": return `${code} 12345678`;
      case "DE": return `${code} 1234567890`;
      case "EE": return `${code} 1234567`;
      case "GR": return `${code} 2101234567`;
      case "ES": return `${code} 123456789`;
      case "FR": return `${code} 123456789`;
      case "GA": return `${code} 123456789`;
      case "HR": return `${code} 12345678`;
      case "IT": return `${code} 123456789`;
      case "LV": return `${code} 12345678`;
      case "LT": return `${code} 12345678`;
      case "HU": return `${code} 12345678`;
      case "MT": return `${code} 12345678`;
      case "NL": return `${code} 123456789`;
      case "AT": return `${code} 12345678`;
      case "PL": return `${code} 123456789`;
      case "PT": return `${code} 123456789`;
      case "RO": return `${code} 123456789`;
      case "SK": return `${code} 123456789`;
      case "SI": return `${code} 12345678`;
      case "FI": return `${code} 123456789`;
      case "SE": return `${code} 1234567`;
      case "NO": return `${code} 12345678`;
      case "TR": return `${code} 1234567890`;
      case "AL": return `${code} 12345678`;
      case "MK": return `${code} 12345678`;
      case "RS": return `${code} 12345678`;
      case "BA": return `${code} 12345678`;
      case "GB": return `${code} 1234567890`;
      case "US": return `${code} 1234567890`;
      case "CH": return `${code} 123456789`;
      default: return `${code} 123456789`;
    }
  }
  
  return "+359 888123456"; // Default to Bulgarian format
}

export function getPhoneExample(countryCode?: string): string {
  if (countryCode && COUNTRY_PHONE_CODES[countryCode as keyof typeof COUNTRY_PHONE_CODES]) {
    const code = COUNTRY_PHONE_CODES[countryCode as keyof typeof COUNTRY_PHONE_CODES];
    switch (countryCode) {
      case "BG": return `${code} 888123456`;
      case "CZ": return `${code} 123456789`;
      case "DK": return `${code} 12345678`;
      case "DE": return `${code} 1234567890`;
      default: return `${code} 123456789`;
    }
  }
  return "+359 888123456";
}
