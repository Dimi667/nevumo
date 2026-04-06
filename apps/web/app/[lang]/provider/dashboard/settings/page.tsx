'use client';

import { useEffect, useRef, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { clearAuth, getAuthUser, saveAuth } from '@/lib/auth-store';
import {
  ProviderApiError,
  checkSlugAvailability,
  getProviderProfile,
  updateProviderProfile,
  switchRole,
} from '@/lib/provider-api';
import type { AvailabilityStatus, ProviderProfile } from '@/types/provider';
import { getSlugValidationError, sanitizeSlug } from '@/lib/slug-utils';
import { usePhone } from '@/hooks/usePhone';
import PhoneInput from '@/components/ui/PhoneInput';

const AVAILABILITY_OPTIONS: { value: AvailabilityStatus; label: string }[] = [
  { value: 'active', label: 'Active' },
  { value: 'busy', label: 'Busy' },
  { value: 'offline', label: 'Offline' },
];

const SITE_HOST = 'nevumo.com';
const MAX_SLUG_CHANGES = 1;

export default function SettingsPage() {
  const router = useRouter();
  const params = useParams();
  const lang = typeof params.lang === 'string' ? params.lang : 'en';
  const user = getAuthUser();

  const [profile, setProfile] = useState<ProviderProfile | null>(null);
  const [loadingProfile, setLoadingProfile] = useState(true);
  const [savingAvailability, setSavingAvailability] = useState(false);
  const [slugInput, setSlugInput] = useState('');
  const [slugChecking, setSlugChecking] = useState(false);
  const [slugAvailable, setSlugAvailable] = useState<boolean | null>(null);
  const [slugError, setSlugError] = useState<string | null>(null);
  const [slugSuggestions, setSlugSuggestions] = useState<string[]>([]);
  const [savingSlug, setSavingSlug] = useState(false);
  const [slugSaved, setSlugSaved] = useState(false);
  const [phoneValue, setPhoneValue] = useState('');
  const [savingPhone, setSavingPhone] = useState(false);
  const [phoneSaved, setPhoneSaved] = useState(false);
  const slugCheckRequestRef = useRef(0);
  const { phone: savedPhone, savePhone } = usePhone();

  const [switchingRole, setSwitchingRole] = useState(false);
  const [switchError, setSwitchError] = useState<string | null>(null);
  const slugChangesRemaining = profile
    ? Math.max(0, MAX_SLUG_CHANGES - profile.slug_change_count)
    : MAX_SLUG_CHANGES;
  const canEditSlug = !!profile && profile.slug_change_count < MAX_SLUG_CHANGES;

  useEffect(() => {
    getProviderProfile()
      .then(data => {
        setProfile(data);
        setSlugInput(data.slug);
      })
      .catch(() => { /* non-fatal, settings still usable */ })
      .finally(() => setLoadingProfile(false));
  }, []);

  useEffect(() => {
    if (savedPhone && !phoneValue) {
      setPhoneValue(savedPhone);
    }
  }, [savedPhone, phoneValue]);

  async function runSlugCheck(candidate: string): Promise<boolean> {
    const trimmed = candidate.trim();
    const validationError = getSlugValidationError(trimmed);

    if (!trimmed) {
      setSlugAvailable(null);
      setSlugError(null);
      setSlugSuggestions([]);
      setSlugChecking(false);
      return false;
    }

    if (validationError) {
      setSlugAvailable(false);
      setSlugError(validationError);
      setSlugSuggestions([]);
      setSlugChecking(false);
      return false;
    }

    if (profile && trimmed === profile.slug) {
      setSlugAvailable(true);
      setSlugError(null);
      setSlugSuggestions([]);
      setSlugChecking(false);
      return true;
    }

    if (!canEditSlug) {
      setSlugAvailable(false);
      setSlugError('URL can only be changed once. Contact support for assistance.');
      setSlugSuggestions([]);
      setSlugChecking(false);
      return false;
    }

    const requestId = slugCheckRequestRef.current + 1;
    slugCheckRequestRef.current = requestId;
    setSlugChecking(true);

    try {
      const result = await checkSlugAvailability(
        trimmed,
        profile?.current_city?.slug,
        profile?.current_category?.slug
      );
      if (slugCheckRequestRef.current !== requestId) {
        return result.available;
      }

      setSlugAvailable(result.available);
      setSlugError(result.error ?? (result.available ? null : 'This URL is already taken'));
      setSlugSuggestions(result.available ? [] : (result.suggestions ?? []));
      return result.available;
    } catch {
      if (slugCheckRequestRef.current === requestId) {
        setSlugAvailable(null);
        setSlugError('Failed to check URL availability');
        setSlugSuggestions([]);
      }
      return false;
    } finally {
      if (slugCheckRequestRef.current === requestId) {
        setSlugChecking(false);
      }
    }
  }

  useEffect(() => {
    if (!profile) {
      return;
    }

    const trimmedSlug = slugInput.trim();
    if (!trimmedSlug) {
      setSlugAvailable(null);
      setSlugError(null);
      setSlugSuggestions([]);
      setSlugChecking(false);
      return;
    }

    const timeoutId = window.setTimeout(() => {
      void runSlugCheck(trimmedSlug);
    }, 300);

    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [canEditSlug, profile, slugInput]);

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

  async function handleSaveSlug() {
    if (!profile || savingSlug) return;

    const isAvailable = await runSlugCheck(slugInput);
    if (!isAvailable) return;

    setSavingSlug(true);
    setSlugSaved(false);
    try {
      const updated = await updateProviderProfile({ 
        slug: slugInput.trim(),
        is_onboarding_setup: false 
      });
      setProfile(updated);
      setSlugInput(updated.slug);
      setSlugSaved(true);
      setTimeout(() => setSlugSaved(false), 3000);
    } catch (e: unknown) {
      if (e instanceof ProviderApiError && e.code === 'SLUG_TAKEN') {
        const data = (e.data ?? {}) as { suggestions?: string[] };
        setSlugAvailable(false);
        setSlugError(e.message);
        setSlugSuggestions(Array.isArray(data.suggestions) ? data.suggestions : []);
      } else if (e instanceof ProviderApiError && e.code === 'INVALID_SLUG') {
        setSlugAvailable(false);
        setSlugError(e.message);
        setSlugSuggestions([]);
      } else if (e instanceof ProviderApiError && e.code === 'SLUG_CHANGE_LIMIT_EXCEEDED') {
        setSlugAvailable(false);
        setSlugError(e.message);
        setSlugSuggestions([]);
      } else {
        setSlugError(e instanceof Error ? e.message : 'Failed to save URL');
        setSlugSuggestions([]);
      }
    } finally {
      setSavingSlug(false);
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
      return `${SITE_HOST}/${lang}/${city}/${category}/${slugInput || profile.slug}`;
    }
    return `${SITE_HOST}/provider/${slugInput || profile.slug}`;
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
        <div className="space-y-2">
          <PhoneInput
            value={phoneValue}
            onChange={setPhoneValue}
            countryCode={user?.country_code ?? 'BG'}
            label="Phone"
            className="pt-2"
          />
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={handleSavePhone}
              disabled={savingPhone}
              className="px-4 py-2 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
            >
              {savingPhone ? 'Saving…' : 'Save Phone'}
            </button>
            {phoneSaved && <span className="text-xs text-green-600 font-medium">Saved!</span>}
          </div>
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
            {slugChangesRemaining > 0 ? (
              <div className="space-y-2">
                <label className="block text-xs text-gray-500">Edit public slug</label>
                <p className="text-xs text-gray-500">URL changes remaining: {slugChangesRemaining}/{MAX_SLUG_CHANGES}</p>
                <p className="text-xs text-orange-600 mt-2">
                  You can only change your URL once.<br />
                  Old links will continue working (redirected).
                </p>
                {canEditSlug ? (
                  <div className="flex items-center gap-2">
                    <input
                      type="text"
                      value={slugInput}
                      onChange={e => {
                        setSlugInput(sanitizeSlug(e.target.value));
                        setSlugSaved(false);
                        setSlugError(null);
                        setSlugSuggestions([]);
                        setSlugAvailable(null);
                      }}
                      placeholder="your-business-name"
                      className={`flex-1 px-3 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400 ${
                        slugError
                          ? 'border-red-400'
                          : slugAvailable === true
                          ? 'border-green-500'
                          : 'border-gray-300'
                      }`}
                    />
                    {slugChecking && <span className="text-xs text-gray-400 whitespace-nowrap">Checking...</span>}
                    {!slugChecking && slugAvailable === true && <span className="text-xs text-green-600 whitespace-nowrap">Available</span>}
                  </div>
                ) : (
                  <div className="rounded-lg border border-orange-200 bg-orange-50 px-3 py-2">
                    <p className="text-xs text-orange-700">
                      URL can only be changed once. Contact support for assistance.
                    </p>
                  </div>
                )}
                {slugError && (
                  <div className="p-2 bg-red-50 rounded-lg">
                    <p className="text-xs text-red-600">{slugError}</p>
                  </div>
                )}
                {slugSuggestions.length > 0 && (
                  <div>
                    <p className="text-xs text-gray-600 mb-1">Suggestions:</p>
                    <div className="flex flex-wrap gap-2">
                      {slugSuggestions.map(suggestion => (
                        <button
                          key={suggestion}
                          type="button"
                          onClick={() => {
                            setSlugInput(suggestion);
                            setSlugSaved(false);
                            setSlugError(null);
                            setSlugSuggestions([]);
                            setSlugAvailable(null);
                          }}
                          className="px-2 py-1 text-xs bg-orange-100 text-orange-700 rounded hover:bg-orange-200 transition-colors"
                        >
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
                {canEditSlug ? (
                  <div className="flex items-center gap-3">
                    <button
                      type="button"
                      onClick={handleSaveSlug}
                      disabled={savingSlug || slugChecking || !slugInput.trim() || slugInput.trim() === profile?.slug}
                      className="px-4 py-2 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
                    >
                      {savingSlug ? 'Saving…' : 'Save URL'}
                    </button>
                    {slugSaved && <span className="text-xs text-green-600 font-medium">Saved!</span>}
                  </div>
                ) : null}
              </div>
            ) : (
              <div className="space-y-3">
                <div className="rounded-lg border border-orange-200 bg-orange-50 px-3 py-3">
                  <p className="text-sm font-medium text-orange-800 mb-2">URL locked</p>
                  <p className="text-xs text-orange-700">
                    Your public URL has already been updated.<br />
                    Old links continue to work via redirects.
                  </p>
                </div>
                <p className="text-xs text-gray-600">
                  Need help? Contact support.
                </p>
              </div>
            )}
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
