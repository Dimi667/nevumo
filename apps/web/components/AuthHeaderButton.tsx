'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { UserCircle } from 'lucide-react';
import { getAuthUser, getAuthToken } from '@/lib/auth-store';
import type { UserInfo } from '@/lib/auth-types';

interface AuthHeaderButtonProps {
  lang: string;
}

const RESERVED_ROUTES = [
  'auth',
  'terms',
  'privacy',
  'cookies',
  'withdrawal',
  'izberi-grad',
  'dolacz',
  'claim',
  'provider',
  'client',
  'oauth-terms',
];

const HIDDEN_PATHS = [
  '/auth',
  '/provider/dashboard',
  '/client/dashboard',
  '/oauth-terms',
];

export default function AuthHeaderButton({ lang }: AuthHeaderButtonProps) {
  const router = useRouter();
  const pathname = usePathname();
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<UserInfo | null>(null);

  useEffect(() => {
    setToken(getAuthToken());
    setUser(getAuthUser());
  }, []);

  // Hide on specific routes
  if (HIDDEN_PATHS.some(path => pathname.includes(path))) {
    return null;
  }

  const handleLoggedInClick = () => {
    if (user?.role === 'provider') {
      router.push(`/${lang}/provider/dashboard`);
    } else {
      router.push(`/${lang}/client/dashboard`);
    }
  };

  const handleLoggedOutClick = () => {
    const segments = pathname.split('/').filter(Boolean);
    let authUrl = `/${lang}/auth`;

    if (segments[1] && !RESERVED_ROUTES.includes(segments[1])) {
      authUrl += `?city=${segments[1]}`;
      
      if (segments[2] && !RESERVED_ROUTES.includes(segments[2])) {
        authUrl += `&category=${segments[2]}`;
      }
    }

    router.push(authUrl);
  };

  if (token && user) {
    const initial = (user.email ?? '').charAt(0).toUpperCase() || '?';

    return (
      <div>
        <button
          onClick={handleLoggedInClick}
          className="w-10 h-10 bg-orange-500 text-white font-semibold rounded-full flex items-center justify-center text-sm hover:bg-orange-600 transition-colors"
          aria-label="Go to dashboard"
        >
          {initial}
        </button>
      </div>
    );
  }

  return (
    <div>
      <UserCircle
        size={36}
        className="text-gray-500 hover:text-orange-500 transition-colors cursor-pointer"
        onClick={handleLoggedOutClick}
      />
    </div>
  );
}
