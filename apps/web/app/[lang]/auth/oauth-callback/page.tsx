'use client';

import { useEffect, useState } from 'react';
import { useSearchParams, useParams } from 'next/navigation';
import { saveAuth } from '@/lib/auth-store';
import type { UserInfo } from '@/lib/auth-types';
import { setCtx } from '@/lib/ctx';

export default function OAuthCallbackPage() {
  const searchParams = useSearchParams();
  const params = useParams();
  const lang = (params?.lang as string) || 'en';
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = searchParams.get('token');
    const userParam = searchParams.get('user');
    const category = searchParams.get('category') || '';
    const city = searchParams.get('city') || '';

    if (!token) {
      window.location.href = `/${lang}/auth?error=oauth_failed`;
      return;
    }

    try {
      const parsedUser: UserInfo = userParam ? JSON.parse(decodeURIComponent(userParam)) : null;
      
      if (!parsedUser) {
        window.location.href = `/${lang}/auth?error=oauth_failed`;
        return;
      }

      saveAuth(token, parsedUser);

      const redirectParam = searchParams.get('redirect');
      const redirectPath = redirectParam
        ? redirectParam
        : parsedUser.role === 'provider'
        ? `/${lang}/provider/dashboard`
        : `/${lang}/izberi-grad`;

      if (city) setCtx({ city });
      if (category) setCtx({ category });

      setTimeout(() => {
        window.location.href = redirectPath;
      }, 100);
    } catch {
      window.location.href = `/${lang}/auth?error=oauth_failed`;
    } finally {
      setLoading(false);
    }
  }, [searchParams, lang]);

  return (
    <div className="min-h-screen bg-[#f9f9f9] flex items-center justify-center">
      <div className="flex flex-col items-center gap-4">
        <div className="w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin" />
        <p className="text-gray-600 text-sm">Processing login...</p>
      </div>
    </div>
  );
}
