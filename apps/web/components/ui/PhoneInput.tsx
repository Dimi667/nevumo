'use client';

import { useEffect, useMemo, useState } from 'react';
import { getPhonePlaceholder, getPhonePrefix, validatePhone } from '@/lib/phoneUtils';

interface PhoneInputProps {
  value: string;
  onChange: (value: string) => void;
  countryCode?: string;        // e.g. "PL" — drives placeholder
  error?: string | null;
  onValidChange?: (isValid: boolean) => void;
  errorMessage?: string;
  label?: string;              // default: use translation or "Phone"
  placeholder?: string;        // override auto placeholder
  className?: string;
  required?: boolean;
}

export default function PhoneInput({
  value,
  onChange,
  countryCode,
  error,
  onValidChange,
  errorMessage = 'Enter a valid phone number',
  label = "Phone",
  placeholder,
  className = "",
  required = false,
}: PhoneInputProps) {
  const [internalError, setInternalError] = useState<string | null>(null);
  const prefix = useMemo(() => getPhonePrefix(countryCode), [countryCode]);
  const inputPlaceholder = placeholder || getPhonePlaceholder(countryCode);

  useEffect(() => {
    if (!value || value.trim() === '') {
      onChange(prefix);
    }
  }, []); // empty dependency array — runs once on mount only

  useEffect(() => {
    if (error) {
      const isValid = value.replace(/\D/g, '').length >= 7;
      setInternalError(isValid ? null : errorMessage);
      onValidChange?.(isValid);
    }
  }, [error, errorMessage, onValidChange, value]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (internalError) {
      setInternalError(null);
    }

    onChange(e.target.value);
  };

  const handleBlur = () => {
    if (!value || value.trim() === '') {
      onChange(prefix);
    }
    
    const isValid = value.replace(/\D/g, '').length >= 7;
    setInternalError(isValid ? null : errorMessage);
    onValidChange?.(isValid);
  };

  const displayedError = internalError || error;

  return (
    <div className={`space-y-1 ${className}`}>
      {label && (
        <label className="block text-sm font-bold text-gray-700">
          {label}
          {required && <span className="text-red-400 ml-1">*</span>}
        </label>
      )}
      
      <input
        type="tel"
        value={value}
        onChange={handleChange}
        onBlur={handleBlur}
        placeholder={inputPlaceholder}
        required={required}
        className={`w-full border border-gray-300 rounded-lg px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent text-sm transition-colors ${
          displayedError ? 'border-red-400 focus:ring-red-300' : ''
        }`}
      />
      
      {displayedError && (
        <p className="text-xs text-red-500 mt-1">{internalError || error}</p>
      )}
    </div>
  );
}

// Re-export validatePhone for consumer convenience
export { validatePhone };
