'use client';

import { use, useEffect, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { getAuthToken, getAuthUser, clearAuth, saveAuth } from '@/lib/auth-store';
import { switchRole } from '@/lib/provider-api';
import { fetchTranslations, t, type TranslationDict } from '@/lib/ui-translations';

interface DashboardLayoutProps {
  children: React.ReactNode;
  params: Promise<{ lang: string }>;
}

function OverviewIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="7" height="7" /><rect x="14" y="3" width="7" height="7" />
      <rect x="14" y="14" width="7" height="7" /><rect x="3" y="14" width="7" height="7" />
    </svg>
  );
}

function RequestsIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </svg>
  );
}

function ReviewsIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  );
}

function SettingsIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
    </svg>
  );
}

interface NavItem {
  label: string;
  href: string;
  icon: React.ReactNode;
}

interface ClientDashboardTopBarProps {
  email: string | null;
  onMenuClick: () => void;
  lang: string;
  dict: TranslationDict;
}

function ClientDashboardTopBar({ email, onMenuClick, lang, dict }: ClientDashboardTopBarProps) {
  const router = useRouter();

  function handleLogout() {
    clearAuth();
    router.push(`/${lang}/auth`);
  }

  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-4 md:px-6 flex-shrink-0">
      <div className="flex items-center gap-3 min-w-0">
        <button
          onClick={onMenuClick}
          className="md:hidden p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
          aria-label="Open menu"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </svg>
        </button>
        <h1 className="font-medium text-gray-900">{t(dict, 'nav_client_dashboard', 'Client Dashboard')}</h1>
      </div>

      <div className="flex items-center gap-3">
        {email && (
          <span className="hidden sm:block text-sm text-gray-500 truncate max-w-[220px]">
            {email}
          </span>
        )}
        <button
          onClick={handleLogout}
          className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16 17 21 12 16 7" />
            <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
          <span className="hidden sm:inline">{t(dict, 'nav_logout', 'Logout')}</span>
        </button>
      </div>
    </header>
  );
}

export default function ClientDashboardLayout({ children, params }: DashboardLayoutProps) {
  const { lang } = use(params);
  const router = useRouter();
  const pathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [ready, setReady] = useState(false);
  const [switchingRole, setSwitchingRole] = useState(false);
  const [switchError, setSwitchError] = useState<string | null>(null);
  const [dict, setDict] = useState<TranslationDict>({});
  const base = `/${lang}/client/dashboard`;
  const user = getAuthUser();

  const navItems: NavItem[] = [
    { label: t(dict, 'nav_overview', 'Overview'), href: `${base}/overview`, icon: <OverviewIcon /> },
    { label: t(dict, 'nav_requests', 'My Requests'), href: `${base}/requests`, icon: <RequestsIcon /> },
    { label: t(dict, 'nav_reviews', 'Reviews'), href: `${base}/reviews`, icon: <ReviewsIcon /> },
    { label: t(dict, 'nav_settings', 'Settings'), href: `${base}/settings`, icon: <SettingsIcon /> },
  ];

  useEffect(() => {
    const token = getAuthToken();
    const currentUser = getAuthUser();

    if (!token || currentUser?.role !== 'client') {
      router.replace(`/${lang}/auth`);
      return;
    }

    setReady(true);
  }, [lang, router]);

  useEffect(() => {
    async function loadTranslations() {
      const translations = await fetchTranslations(lang, 'client_dashboard');
      setDict(translations);
    }

    void loadTranslations();
  }, [lang]);

  if (!ready) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const sidebarContent = (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className="h-16 flex items-center px-5 border-b border-gray-100 flex-shrink-0">
        <Link href={`${base}/overview`} onClick={() => setSidebarOpen(false)} className="flex items-center gap-1.5">
          <Image
            src="/Nevumo_logo.svg"
            alt="Nevumo"
            width={120}
            height={20}
            priority
            style={{ width: '120px', height: 'auto' }}
          />
        </Link>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        {navItems.map((item) => {
          const isActive =
            item.href === `${base}/overview`
              ? pathname === base || pathname === `${base}/` || pathname.startsWith(item.href)
              : pathname.startsWith(item.href);

          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={() => setSidebarOpen(false)}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-orange-50 text-orange-600'
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
              }`}
            >
              <span className={isActive ? 'text-orange-500' : 'text-gray-400'}>
                {item.icon}
              </span>
              {item.label}
            </Link>
          );
        })}

        {/* НАМЕРИ УСЛУГА бутон след Settings */}
        <div className="pt-6 border-t border-gray-200 pb-6">
          <Link
            href={`/${lang}`}
            onClick={() => setSidebarOpen(false)}
            className="w-full flex items-center justify-center gap-2 px-3 py-2.5 rounded-lg text-xs font-bold tracking-widest uppercase transition-colors bg-orange-500 hover:bg-orange-600 text-white"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            {t(dict, 'nav_find_service', 'Find Service')}
          </Link>
        </div>

        {/* Стани доставчик секция */}
        <div className="pt-6 border-t border-gray-200 pb-6">
          <p className="text-sm text-gray-500 mb-5">
            {t(dict, 'nav_provider_pitch', 'Offer services and get clients!')}
          </p>
          <button
            onClick={async () => {
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
              setSidebarOpen(false);
            }}
            disabled={switchingRole}
            className="w-full flex items-center justify-center gap-2 px-3 py-2.5 rounded-lg text-xs font-bold tracking-widest uppercase transition-colors bg-gray-900 hover:bg-gray-700 disabled:opacity-50 text-white"
          >
            {switchingRole ? t(dict, 'nav_switching', 'Switching...') : t(dict, 'nav_become_provider', 'Become a Provider')}
          </button>
          {switchError && (
            <p className="px-3 mt-2 text-xs text-red-600">{switchError}</p>
          )}
        </div>
      </nav>

      {/* Logout */}
      <div className="p-3 border-t border-gray-100">
        <button
          onClick={() => {
            clearAuth();
            router.push(`/${lang}/auth`);
          }}
          className="w-full flex items-center justify-center gap-2 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-colors"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16 17 21 12 16 7" />
            <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
          {t(dict, 'nav_logout', 'Logout')}
        </button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Desktop sidebar */}
      <aside className="hidden md:flex w-60 flex-col bg-white border-r border-gray-200 flex-shrink-0">
        {sidebarContent}
      </aside>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-40 md:hidden">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setSidebarOpen(false)}
          />
          <aside className="absolute left-0 top-0 h-full w-64 bg-white shadow-xl z-50">
            <button
              onClick={() => setSidebarOpen(false)}
              className="absolute top-4 right-4 p-1 text-gray-400 hover:text-gray-600"
              aria-label="Close sidebar"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
            {sidebarContent}
          </aside>
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top bar */}
        <ClientDashboardTopBar
          email={user?.email ?? null}
          onMenuClick={() => setSidebarOpen(true)}
          lang={lang}
          dict={dict}
        />

        <main className="flex-1 p-4 md:p-6 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
