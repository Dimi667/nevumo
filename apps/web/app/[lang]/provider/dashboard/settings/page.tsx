'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { clearAuth, getAuthUser, saveAuth } from '@/lib/auth-store';
import { getProviderProfile, updateProviderProfile, switchRole } from '@/lib/provider-api';
import type { AvailabilityStatus, ProviderProfile } from '@/types/provider';

const AVAILABILITY_OPTIONS: { value: AvailabilityStatus; label: string }[] = [
  { value: 'active', label: 'Active' },
  { value: 'busy', label: 'Busy' },
  { value: 'offline', label: 'Offline' },
];

const SITE_HOST = 'nevumo.com';

export default function SettingsPage() {
  const router = useRouter();
  const params = useParams();
  const lang = typeof params.lang === 'string' ? params.lang : 'en';
  const user = getAuthUser();

  const [profile, setProfile] = useState<ProviderProfile | null>(null);
  const [loadingProfile, setLoadingProfile] = useState(true);
  const [savingAvailability, setSavingAvailability] = useState(false);

  const [switchingRole, setSwitchingRole] = useState(false);
  const [switchError, setSwitchError] = useState<string | null>(null);

  useEffect(() => {
    getProviderProfile()
      .then(setProfile)
      .catch(() => { /* non-fatal, settings still usable */ })
      .finally(() => setLoadingProfile(false));
  }, []);

  async function handleAvailability(status: AvailabilityStatus) {
    if (savingAvailability || profile?.availability_status === status) return;
    setSavingAvailability(true);
    try {
      const updated = await updateProviderProfile({ availability_status: status });
      setProfile(updated);
    } catch {
      // silently ignore; UI reverts automatically
    } finally {
      setSavingAvailability(false);
    }
  }

  async function handleSwitchToClient() {
    setSwitchingRole(true);
    setSwitchError(null);
    try {
      const result = await switchRole('client');
      saveAuth(result.token, result.user);
      router.push(`/${lang}/`);
    } catch (e: unknown) {
      setSwitchError(e instanceof Error ? e.message : 'Failed to switch role');
      setSwitchingRole(false);
    }
  }

  function handleLogout() {
    clearAuth();
    router.push(`/${lang}/auth`);
  }

  // Build public URL from profile data
  const publicUrl = (() => {
    if (!profile) return null;
    const city = profile.current_city?.slug;
    const category = profile.current_category?.slug;
    if (city && category) {
      return `${SITE_HOST}/${lang}/${city}/${category}/${profile.slug}`;
    }
    return `${SITE_HOST}/provider/${profile.slug}`;
  })();

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-xl font-bold text-gray-900">Settings</h1>
        <p className="text-sm text-gray-500 mt-0.5">Account and preferences</p>
      </div>

      {/* Account info */}
      <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-800">Account</h2>
        <div>
          <p className="text-xs text-gray-500">Email</p>
          <p className="text-sm text-gray-900 mt-0.5">{user?.email ?? '—'}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500">Role</p>
          <p className="text-sm text-gray-900 mt-0.5 capitalize">{user?.role ?? '—'}</p>
        </div>
      </div>

      {/* Availability */}
      <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-800">Availability</h2>
        <p className="text-xs text-gray-500">
          Controls whether you appear as available to new clients.
        </p>
        {loadingProfile ? (
          <div className="flex gap-2">
            {AVAILABILITY_OPTIONS.map(opt => (
              <div key={opt.value} className="px-3 py-1.5 rounded-lg border border-gray-200 text-sm text-gray-300 bg-gray-50">
                {opt.label}
              </div>
            ))}
          </div>
        ) : (
          <div className="flex items-center gap-2">
            {AVAILABILITY_OPTIONS.map(opt => {
              const isActive = profile?.availability_status === opt.value;
              return (
                <button
                  key={opt.value}
                  onClick={() => handleAvailability(opt.value)}
                  disabled={savingAvailability}
                  className={`px-3 py-1.5 text-sm font-medium rounded-lg border transition-colors disabled:opacity-60 ${
                    isActive
                      ? 'border-orange-400 bg-orange-50 text-orange-700'
                      : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  {opt.label}
                </button>
              );
            })}
            {savingAvailability && (
              <span className="w-4 h-4 border border-gray-400 border-t-transparent rounded-full animate-spin" />
            )}
          </div>
        )}
      </div>

      {/* Public URL */}
      <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-800">Public URL</h2>
        {loadingProfile ? (
          <div className="h-8 bg-gray-100 rounded-lg animate-pulse" />
        ) : publicUrl ? (
          <>
            <div className="bg-gray-50 rounded-lg px-3 py-2.5 border border-gray-200">
              <p className="text-xs text-gray-500 mb-0.5">Your profile link</p>
              <p className="text-sm font-mono text-gray-800 break-all">{publicUrl}</p>
            </div>
            {!profile?.current_city || !profile?.current_category ? (
              <p className="text-xs text-orange-600">
                Add a city and category in your Profile to get a full SEO URL.
              </p>
            ) : null}
          </>
        ) : (
          <p className="text-sm text-gray-400">Profile not loaded.</p>
        )}
      </div>

      {/* Account Role */}
      <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-800">Account Role</h2>
        <p className="text-sm text-gray-500">
          You are currently a <span className="font-medium text-gray-800">Provider</span>.
          Switching to a client account will allow you to browse services and submit requests.
          Your provider profile and data will be preserved.
        </p>
        {switchError && (
          <p className="text-xs text-red-600">{switchError}</p>
        )}
        <button
          onClick={handleSwitchToClient}
          disabled={switchingRole}
          className="px-4 py-2 border border-gray-300 text-gray-700 hover:bg-gray-100 disabled:opacity-50 text-sm font-medium rounded-lg transition-colors"
        >
          {switchingRole ? 'Switching…' : 'Switch to Client Account'}
        </button>
      </div>

      {/* Logout */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h2 className="text-sm font-semibold text-gray-800 mb-3">Session</h2>
        <button
          onClick={handleLogout}
          className="flex items-center gap-2 px-4 py-2 border border-red-200 text-red-600 hover:bg-red-50 text-sm font-medium rounded-lg transition-colors"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16 17 21 12 16 7" />
            <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
          Log out
        </button>
      </div>
    </div>
  );
}
