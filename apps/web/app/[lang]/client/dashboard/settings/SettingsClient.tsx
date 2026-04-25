'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { clearAuth, getAuthToken, getAuthUser, saveAuth } from '@/lib/auth-store';
import { getReviewPreferences, updateReviewPreferences, type ReviewPreferences } from '@/lib/client-api';
import { switchRole } from '@/lib/provider-api';
import { usePhone } from '@/hooks/usePhone';
import PhoneInput from '@/components/ui/PhoneInput';
import { useTranslation } from '@/lib/use-translation';

export default function SettingsClient({ lang }: { lang: string }) {
  const router = useRouter();
  const user = getAuthUser();

  const [preferences, setPreferences] = useState<ReviewPreferences | null>(null);
  const [loading, setLoading] = useState(true);
  const [savingPreference, setSavingPreference] = useState(false);
  const [switchingRole, setSwitchingRole] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [switchError, setSwitchError] = useState<string | null>(null);
  const [phoneValue, setPhoneValue] = useState('');
  const [savingPhone, setSavingPhone] = useState(false);
  const [phoneSaved, setPhoneSaved] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleteError, setDeleteError] = useState('');
  const { t } = useTranslation('client_dashboard', lang);
  const { phone: savedPhone, savePhone } = usePhone();

  useEffect(() => {
    async function loadPreferences() {
      const token = getAuthToken();

      if (!token) {
        setError('Липсва активна сесия.');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const response = await getReviewPreferences(token);
        setPreferences(response);
        setPhoneValue(savedPhone || '');
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : 'Неуспешно зареждане на настройките.');
      } finally {
        setLoading(false);
      }
    }

    void loadPreferences();
  }, [savedPhone]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  async function handleTogglePreference() {
    const token = getAuthToken();

    if (!token || !preferences) {
      setError('Липсва активна сесия.');
      return;
    }

    try {
      setSavingPreference(true);
      setError(null);
      const updated = await updateReviewPreferences(token, !preferences.review_reply_email_enabled);
      setPreferences(updated);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Неуспешно записване на настройката.');
    } finally {
      setSavingPreference(false);
    }
  }

  async function handleBecomeProvider() {
    setSwitchingRole(true);
    setSwitchError(null);

    try {
      const result = await switchRole('provider');
      saveAuth(result.token, result.user);
      router.push(`/${lang}/provider/dashboard`);
    } catch (e: unknown) {
      setSwitchError(e instanceof Error ? e.message : 'Неуспешна смяна на роля.');
      setSwitchingRole(false);
    }
  }

  async function handleSavePhone() {
    if (savingPhone) return;

    setSavingPhone(true);
    setPhoneSaved(false);
    
    try {
      await savePhone(phoneValue);
      setPhoneSaved(true);
      setTimeout(() => setPhoneSaved(false), 3000);
    } catch {
      // Silent fail - usePhone hook handles errors internally
    } finally {
      setSavingPhone(false);
    }
  }

  function handleLogout() {
    clearAuth();
    router.push(`/${lang}/auth`);
  }

  async function handleDeleteAccount() {
    const token = getAuthToken();
    if (!token) {
      setDeleteError('Could not delete account. Please try again.');
      return;
    }
    try {
      const response = await fetch('/api/v1/auth/account', {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.ok) {
        clearAuth();
        localStorage.removeItem('nevumo_selected_category');
        localStorage.removeItem('nevumo_intent');
        router.push(`/${lang}`);
      } else {
        setDeleteError('Could not delete account. Please try again.');
      }
    } catch {
      setDeleteError('Could not delete account. Please try again.');
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-lg font-semibold text-gray-900">{t('settings_title', 'Settings')}</h1>
        <p className="text-sm text-gray-500 mt-0.5">{t('settings_subtitle', 'Account and preferences')}</p>
      </div>

      {error && (
        <div className="bg-red-50 text-red-700 rounded-xl p-4 text-sm">
          {error}
        </div>
      )}

      <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-800">{t('section_account', 'Account')}</h2>
        <div className="space-y-2">
          <label className="block text-xs font-medium text-gray-500" htmlFor="client-email">
            {t('label_email', 'Email')}
          </label>
          <input
            id="client-email"
            type="email"
            readOnly
            value={user?.email ?? ''}
            className="w-full px-3 py-2 border border-gray-200 rounded-lg bg-gray-50 text-sm text-gray-700 focus:outline-none"
          />
        </div>
        <div className="space-y-2">
          <PhoneInput
            value={phoneValue}
            onChange={setPhoneValue}
            countryCode={user?.country_code ?? 'BG'}
            label={t('label_phone', 'Phone')}
            className="pt-2"
          />
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={handleSavePhone}
              disabled={savingPhone}
              className="px-4 py-2 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
            >
              {savingPhone ? t('btn_saving', 'Saving…') : t('btn_save_phone', 'Save Phone')}
            </button>
            {phoneSaved && <span className="text-xs text-green-600 font-medium">{t('btn_saved', 'Saved!')}</span>}
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-800">{t('section_security', 'Security')}</h2>
        <p className="text-sm text-gray-500">
          {t('settings_security', 'Manage access...')}
        </p>
        <Link
          href={`/${lang}/auth/reset-password`}
          className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 text-gray-700 hover:bg-gray-100 text-sm font-medium rounded-lg transition-colors"
        >
          {t('btn_change_password', 'Change Password')}
        </Link>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-800">{t('section_notifications', 'Email Notifications')}</h2>
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm text-gray-700">{t('settings_email_notif', 'Receive email on review reply')}</p>
            <p className="text-xs text-gray-500 mt-1">
              {preferences?.description ?? t('settings_email_notif_desc', 'Receive email notifications when providers reply to your reviews')}
            </p>
          </div>
          <button
            type="button"
            onClick={handleTogglePreference}
            disabled={savingPreference || !preferences}
            aria-label={preferences?.review_reply_email_enabled ? 'Disable email notifications' : 'Enable email notifications'}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors disabled:opacity-50 ${
              preferences?.review_reply_email_enabled ? 'bg-orange-500' : 'bg-gray-200'
            }`}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                preferences?.review_reply_email_enabled ? 'translate-x-6' : 'translate-x-1'
              }`}
            />
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-800">{t('section_role', 'Account Role')}</h2>
        <p className="text-sm text-gray-500">
          {t('settings_role_desc', 'If you want to offer services...')}
        </p>
        {switchError && (
          <p className="text-xs text-red-600">{switchError}</p>
        )}
        <button
          type="button"
          onClick={handleBecomeProvider}
          disabled={switchingRole}
          className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
        >
          {switchingRole ? t('nav_switching', 'Switching...') : t('nav_become_provider', 'Become a Provider')}
        </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h2 className="text-sm font-semibold text-gray-800 mb-3">{t('section_session', 'Session')}</h2>
        <button
          type="button"
          onClick={handleLogout}
          className="inline-flex items-center gap-2 px-4 py-2 border border-red-200 text-red-600 hover:bg-red-50 text-sm font-medium rounded-lg transition-colors"
        >
          {t('nav_logout', 'Logout')}
        </button>
      </div>

      <hr className="border-red-100 my-6" />

      {/* Delete Account */}
      <div className="bg-white rounded-xl border border-red-200 p-5 space-y-3">
        <h3 className="text-red-600 font-semibold">{t('delete_account_title', 'Delete Account')}</h3>
        {!showDeleteConfirm ? (
          <>
            <p className="text-sm text-gray-500 mt-1 mb-3">
              {t('delete_account_warning', 'This action cannot be undone. All your data will be permanently removed.')}
            </p>
            <button
              type="button"
              onClick={() => setShowDeleteConfirm(true)}
              className="w-full border border-red-500 text-red-500 rounded-lg py-2 px-4 hover:bg-red-50 transition-colors"
            >
              {t('delete_account_btn', 'Delete Account')}
            </button>
          </>
        ) : (
          <div>
            <p className="text-sm text-gray-500 mb-3">
              {t('delete_account_warning', 'This action cannot be undone. All your data will be permanently removed.')}
            </p>
            <div className="flex gap-3">
              <button
                type="button"
                onClick={() => {
                  setShowDeleteConfirm(false);
                  setDeleteError('');
                }}
                className="flex-1 border border-gray-300 text-gray-600 rounded-lg py-2 hover:bg-gray-50"
              >
                {t('delete_account_cancel', 'Cancel')}
              </button>
              <button
                type="button"
                onClick={handleDeleteAccount}
                className="flex-1 bg-red-600 text-white rounded-lg py-2 hover:bg-red-700"
              >
                {t('delete_account_confirm', 'Confirm Deletion')}
              </button>
            </div>
            {deleteError && <p className="text-red-500 text-sm mt-2">{deleteError}</p>}
          </div>
        )}
      </div>
    </div>
  );
}
