'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { clearAuth, getAuthToken, getAuthUser, saveAuth } from '@/lib/auth-store';
import { getReviewPreferences, updateReviewPreferences, type ReviewPreferences } from '@/lib/client-api';
import { switchRole } from '@/lib/provider-api';

export default function ClientSettingsPage() {
  const router = useRouter();
  const params = useParams();
  const lang = typeof params.lang === 'string' ? params.lang : 'en';
  const user = getAuthUser();

  const [preferences, setPreferences] = useState<ReviewPreferences | null>(null);
  const [loading, setLoading] = useState(true);
  const [savingPreference, setSavingPreference] = useState(false);
  const [switchingRole, setSwitchingRole] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [switchError, setSwitchError] = useState<string | null>(null);

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
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : 'Неуспешно зареждане на настройките.');
      } finally {
        setLoading(false);
      }
    }

    void loadPreferences();
  }, []);

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

  function handleLogout() {
    clearAuth();
    router.push(`/${lang}/auth`);
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-xl font-bold text-gray-900">Settings</h1>
        <p className="text-sm text-gray-500 mt-0.5">Акаунт и предпочитания</p>
      </div>

      {error && (
        <div className="bg-red-50 text-red-700 rounded-xl p-4 text-sm">
          {error}
        </div>
      )}

      <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-800">Account</h2>
        <div className="space-y-2">
          <label className="block text-xs font-medium text-gray-500" htmlFor="client-email">
            Email
          </label>
          <input
            id="client-email"
            type="email"
            readOnly
            value={user?.email ?? ''}
            className="w-full px-3 py-2 border border-gray-200 rounded-lg bg-gray-50 text-sm text-gray-700 focus:outline-none"
          />
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-800">Security</h2>
        <p className="text-sm text-gray-500">
          Управлявай достъпа до профила си и смени паролата при нужда.
        </p>
        <Link
          href={`/${lang}/auth/reset-password`}
          className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 text-gray-700 hover:bg-gray-100 text-sm font-medium rounded-lg transition-colors"
        >
          Смени парола
        </Link>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-800">Имейл нотификации</h2>
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm text-gray-700">Получавай имейл при отговор на ревю</p>
            <p className="text-xs text-gray-500 mt-1">
              {preferences?.description ?? 'Известия при отговор от доставчик'}
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
        <h2 className="text-sm font-semibold text-gray-800">Account Role</h2>
        <p className="text-sm text-gray-500">
          Ако искаш да предлагаш услуги в Nevumo, можеш да преминеш към доставчик без да губиш текущия си профил.
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
          {switchingRole ? 'Превключване...' : 'Стани доставчик'}
        </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h2 className="text-sm font-semibold text-gray-800 mb-3">Session</h2>
        <button
          type="button"
          onClick={handleLogout}
          className="inline-flex items-center gap-2 px-4 py-2 border border-red-200 text-red-600 hover:bg-red-50 text-sm font-medium rounded-lg transition-colors"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
