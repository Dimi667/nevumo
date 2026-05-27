'use client';

import { useEffect, useMemo, useState } from 'react';
import { usePhone } from '@/hooks/usePhone';
import { getPhonePlaceholder, getPhonePrefix } from '@/lib/phoneUtils';
import { useTranslation } from '@/lib/use-translation';

interface PhoneInputProps {
  onChange?: (value: string) => void;  // optional callback when phone changes
  countryCode?: string;               // e.g. "PL" — drives placeholder
  label?: string;                     // default: use translation or "Phone"
  placeholder?: string;                // override auto placeholder
  className?: string;
  required?: boolean;
  lang?: string;                       // for translations
  submitted?: boolean;                // whether parent form was submitted
}

export default function PhoneInput({
  onChange,
  countryCode,
  label,
  placeholder,
  className = "",
  required = false,
  lang = 'en',
  submitted = false,
}: PhoneInputProps) {
  const { phone, savePhone, loading, isValid } = usePhone(countryCode);
  const { t } = useTranslation('widget', lang);
  const prefix = useMemo(() => getPhonePrefix(countryCode), [countryCode]);
  const inputPlaceholder = placeholder || getPhonePlaceholder(countryCode);
  const [touched, setTouched] = useState(false);

  // Initialize with country prefix if empty
  useEffect(() => {
    if (!loading && (!phone || phone.trim() === '')) {
      savePhone(prefix);
    }
  }, [loading, phone, prefix, savePhone]);

  // Call external onChange callback when phone changes
  useEffect(() => {
    if (onChange && phone) {
      onChange(phone);
    }
  }, [phone, onChange]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    savePhone(e.target.value);
    setTouched(true);
  };

  const handleBlur = () => {
    setTouched(true);
  };

  const errorMessage = t('phone_error') || 'Enter a valid phone number';
  const showError = !isValid && phone && (touched || submitted);

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
        value={phone}
        onChange={handleChange}
        onBlur={handleBlur}
        placeholder={inputPlaceholder}
        required={required}
        disabled={loading}
        className={`w-full border border-gray-300 rounded-lg px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent text-sm transition-colors ${
          showError ? 'border-red-400 focus:ring-red-300' : ''
        }`}
      />
      
      {showError && (
        <p className="text-xs text-red-500 mt-1">{errorMessage}</p>
      )}
    </div>
  );
}
