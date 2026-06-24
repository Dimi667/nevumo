'use client';

import { useState, useEffect } from 'react';
import { authFetch, getMe } from '@/lib/provider-api';
import { useTranslation } from '@/lib/use-translation';

interface PasswordSectionProps {
  lang: string;
  onSuccess?: () => void;
}

function EyeIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  );
}

function EyeOffIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 5c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
      <line x1="1" y1="1" x2="23" y2="23" />
    </svg>
  );
}

export default function PasswordSection({ lang, onSuccess }: PasswordSectionProps) {
  const { t } = useTranslation('account_settings', lang);
  
  const [localHasPassword, setLocalHasPassword] = useState<boolean>(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    async function loadMe() {
      try {
        const me = await getMe();
        setLocalHasPassword(me.has_password);
      } catch (err) {
        console.error('Failed to load user info:', err);
      }
    }
    loadMe();
  }, []);

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};
    
    if (newPassword.length < 8) {
      errors.new_password = t('error_password_too_short', 'Password must be at least 8 characters.');
    }
    
    if (newPassword !== confirmPassword) {
      errors.confirm_password = t('error_passwords_dont_match', 'Passwords do not match.');
    }
    
    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);
    setFieldErrors({});

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const body: { current_password?: string; new_password: string } = {
        new_password: newPassword,
      };

      if (localHasPassword) {
        body.current_password = currentPassword;
      }

      const response = await authFetch<{ message: string }>(
        '/api/v1/auth/password',
        {
          method: 'POST',
          body: JSON.stringify(body),
        }
      );

      if (response.message === 'password_set') {
        setSuccessMessage(t('msg_password_set', 'Password set successfully.'));
        setCurrentPassword('');
        setNewPassword('');
        setConfirmPassword('');
        onSuccess?.();
      } else if (response.message === 'password_changed') {
        setSuccessMessage(t('msg_password_changed', 'Password changed successfully.'));
        setCurrentPassword('');
        setNewPassword('');
        setConfirmPassword('');
      }
    } catch (err: unknown) {
      if (err instanceof Error && 'code' in err) {
        const code = (err as { code: string }).code;
        if (code === 'INVALID_CURRENT_PASSWORD') {
          setError(t('error_current_password_invalid', 'Current password is incorrect.'));
        } else {
          setError(err.message);
        }
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
      <h2 className="text-sm font-semibold text-gray-800">{t('section_security', 'Security')}</h2>
      <p className="text-sm text-gray-500">
        {localHasPassword
          ? t('security_description_has_password', 'Change your account password.')
          : t('security_description_no_password', 'You signed in without a password. Set one now so you can log in anytime.')
        }
      </p>

      {successMessage && (
        <div className="bg-green-50 text-green-700 rounded-lg p-3 text-sm">
          {successMessage}
        </div>
      )}

      {error && (
        <div className="bg-red-50 text-red-700 rounded-lg p-3 text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-3">
        {localHasPassword && (
          <div className="space-y-1">
            <label className="block text-xs font-medium text-gray-500" htmlFor="current-password">
              {t('label_current_password', 'Current password')}
            </label>
            <div className="relative">
              <input
                id="current-password"
                type={showCurrentPassword ? 'text' : 'password'}
                value={currentPassword}
                onChange={e => setCurrentPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400"
                placeholder={t('label_current_password', 'Current password')}
              />
              <button
                type="button"
                onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                tabIndex={-1}
              >
                {showCurrentPassword ? <EyeOffIcon /> : <EyeIcon />}
              </button>
            </div>
          </div>
        )}

        <div className="space-y-1">
          <label className="block text-xs font-medium text-gray-500" htmlFor="new-password">
            {t('label_new_password', 'New password')}
          </label>
          <div className="relative">
            <input
              id="new-password"
              type={showNewPassword ? 'text' : 'password'}
              value={newPassword}
              onChange={e => setNewPassword(e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 ${
                fieldErrors.new_password ? 'border-red-400' : 'border-gray-300'
              }`}
              placeholder={t('label_new_password', 'New password')}
            />
            <button
              type="button"
              onClick={() => setShowNewPassword(!showNewPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
              tabIndex={-1}
            >
              {showNewPassword ? <EyeOffIcon /> : <EyeIcon />}
            </button>
          </div>
          {fieldErrors.new_password && (
            <p className="text-red-600 text-xs">{fieldErrors.new_password}</p>
          )}
        </div>

        <div className="space-y-1">
          <label className="block text-xs font-medium text-gray-500" htmlFor="confirm-password">
            {t('label_confirm_password', 'Confirm new password')}
          </label>
          <div className="relative">
            <input
              id="confirm-password"
              type={showConfirmPassword ? 'text' : 'password'}
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 ${
                fieldErrors.confirm_password ? 'border-red-400' : 'border-gray-300'
              }`}
              placeholder={t('label_confirm_password', 'Confirm new password')}
            />
            <button
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
              tabIndex={-1}
            >
              {showConfirmPassword ? <EyeOffIcon /> : <EyeIcon />}
            </button>
          </div>
          {fieldErrors.confirm_password && (
            <p className="text-red-600 text-xs">{fieldErrors.confirm_password}</p>
          )}
        </div>

        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
        >
          {loading ? t('btn_save_password', 'Save') : (localHasPassword ? t('btn_change_password', 'Change password') : t('btn_set_password', 'Set password'))}
        </button>
      </form>
    </div>
  );
}
