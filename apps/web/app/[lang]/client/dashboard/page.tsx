'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { isAuthenticated, getAuthUser, saveAuth } from '@/lib/auth-store';
import { switchRole } from '@/lib/provider-api';

export default function ClientDashboardPage() {
  const router = useRouter();
  const params = useParams();
  const lang = typeof params.lang === 'string' ? params.lang : 'en';

  const [ready, setReady] = useState(false);
  const [switching, setSwitching] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace(`/${lang}/auth`);
      return;
    }
    const user = getAuthUser();
    if (user?.role === 'provider') {
      router.replace(`/${lang}/provider/dashboard`);
      return;
    }
    setReady(true);
  }, [lang, router]);

  async function handleBecomeProvider() {
    setSwitching(true);
    setError(null);
    try {
      const result = await switchRole('provider');
      saveAuth(result.token, result.user);
      router.push(`/${lang}/provider/dashboard`);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to switch role');
      setSwitching(false);
    }
  }

  const user = getAuthUser();

  if (!ready) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <div className="bg-white rounded-2xl border border-gray-200 p-8 max-w-md w-full space-y-6 text-center">
        <div className="space-y-1">
          <h1 className="text-2xl font-bold text-gray-900">Client Dashboard</h1>
          {user?.email && (
            <p className="text-sm text-gray-500">{user.email}</p>
          )}
        </div>

        <p className="text-sm text-gray-600">
          Browse services, compare providers, and submit requests.
        </p>

        <div className="border-t border-gray-100 pt-6 space-y-3">
          <p className="text-xs text-gray-500 uppercase tracking-wide font-medium">
            Are you a service provider?
          </p>
          <p className="text-sm text-gray-600">
            Switch to a provider account to list your services and receive leads.
          </p>
          {error && (
            <p className="text-xs text-red-600">{error}</p>
          )}
          <button
            onClick={handleBecomeProvider}
            disabled={switching}
            className="w-full flex items-center justify-center gap-2 py-2.5 bg-gray-900 hover:bg-gray-800 disabled:opacity-50 text-white text-xs font-bold tracking-widest uppercase rounded-xl transition-colors"
          >
            {switching ? (
              <>
                <span className="w-3.5 h-3.5 border border-white border-t-transparent rounded-full animate-spin" />
                Switching…
              </>
            ) : (
              <>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
                </svg>
                ПРЕДЛАГАЙ УСЛУГИ
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
