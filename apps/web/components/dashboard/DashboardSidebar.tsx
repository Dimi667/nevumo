'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname, useRouter } from 'next/navigation';
import { saveAuth } from '@/lib/auth-store';
import { switchRole } from '@/lib/provider-api';
import { useDashboardI18n } from '@/lib/provider-dashboard-i18n';

interface NavItem {
  label: string;
  href: string;
  icon: React.ReactNode;
}

function OverviewIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="7" height="7" /><rect x="14" y="3" width="7" height="7" />
      <rect x="14" y="14" width="7" height="7" /><rect x="3" y="14" width="7" height="7" />
    </svg>
  );
}

function LeadsIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </svg>
  );
}

function ServicesIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="2" y="7" width="20" height="14" rx="2" />
      <path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2" />
    </svg>
  );
}

function AnalyticsIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="20" x2="18" y2="10" /><line x1="12" y1="20" x2="12" y2="4" />
      <line x1="6" y1="20" x2="6" y2="14" />
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

function QrIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="7" height="7" /><rect x="14" y="3" width="7" height="7" />
      <rect x="3" y="14" width="7" height="7" />
      <path d="M14 14h.01M14 17h3M17 14v3M20 17v3M20 14h.01" />
    </svg>
  );
}

function ProfileIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
      <circle cx="12" cy="7" r="4" />
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

interface DashboardSidebarProps {
  open: boolean;
  onClose: () => void;
  lang: string;
}

export default function DashboardSidebar({ open, onClose, lang }: DashboardSidebarProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { t } = useDashboardI18n();
  const base = `/${lang}/provider/dashboard`;

  const [switching, setSwitching] = useState(false);
  const [switchError, setSwitchError] = useState<string | null>(null);

  const navItems: NavItem[] = [
    { label: t('nav_dashboard', 'Dashboard'), href: base, icon: <OverviewIcon /> },
    { label: t('nav_leads', 'Leads'), href: `${base}/leads`, icon: <LeadsIcon /> },
    { label: t('nav_services', 'Services'), href: `${base}/services`, icon: <ServicesIcon /> },
    { label: t('nav_analytics', 'Analytics'), href: `${base}/analytics`, icon: <AnalyticsIcon /> },
    { label: t('nav_reviews', 'Reviews'), href: `${base}/reviews`, icon: <ReviewsIcon /> },
    { label: t('nav_qr_code', 'QR Code'), href: `${base}/qr-code`, icon: <QrIcon /> },
    { label: t('nav_profile', 'Profile'), href: `${base}/profile`, icon: <ProfileIcon /> },
    { label: t('nav_settings', 'Settings'), href: `${base}/settings`, icon: <SettingsIcon /> },
  ];

  async function handleFindService() {
    setSwitching(true);
    setSwitchError(null);
    try {
      const result = await switchRole('client');
      saveAuth(result.token, result.user);
      onClose();
      router.push(`/${lang}/client/dashboard`);
    } catch (e: unknown) {
      setSwitchError(e instanceof Error ? e.message : t('msg_failed_switch_role', 'Failed to switch role'));
      setSwitching(false);
    }
  }

  const sidebarContent = (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className="h-16 flex items-center px-5 border-b border-gray-100 flex-shrink-0">
        <Link href={base} onClick={onClose} className="flex items-center gap-1.5">
          <Image
            src="/Nevumo_logo.svg"
            alt="Nevumo"
            width={120}
            height={20}
            priority
            style={{ width: '120px', height: 'auto' }}
          />
          <span className="text-xs text-gray-400 font-medium leading-none">{t('logo_pro', 'Pro')}</span>
        </Link>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        {navItems.map((item) => {
          const isActive =
            item.href === base
              ? pathname === base || pathname === `${base}/`
              : pathname.startsWith(item.href);

          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={onClose}
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

        {/* Divider + НАМЕРИ УСЛУГА */}
        <div className="pt-5 mt-3 border-t border-gray-100">
          {switchError && (
            <p className="text-xs text-red-500 px-3 pb-2">{switchError}</p>
          )}
          <button
            onClick={handleFindService}
            disabled={switching}
            className="w-full flex items-center justify-center gap-2 px-3 py-2.5 rounded-lg text-xs font-bold tracking-widest uppercase transition-colors disabled:opacity-50 bg-gray-900 hover:bg-gray-800 text-white"
          >
            {switching ? (
              <>
                <span className="w-3.5 h-3.5 border border-white border-t-transparent rounded-full animate-spin" />
                {t('msg_switching', 'Switching…')}
              </>
            ) : (
              <>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
                </svg>
                {t('btn_find_service', 'Find Service')}
              </>
            )}
          </button>
        </div>
      </nav>
    </div>
  );

  return (
    <>
      {/* Desktop sidebar */}
      <aside className="hidden md:flex w-60 flex-col bg-white border-r border-gray-200 flex-shrink-0">
        {sidebarContent}
      </aside>

      {/* Mobile overlay */}
      {open && (
        <div className="fixed inset-0 z-40 md:hidden">
          {/* Backdrop */}
          <div
            className="absolute inset-0 bg-black/40"
            onClick={onClose}
          />
          {/* Panel */}
          <aside className="absolute left-0 top-0 h-full w-64 bg-white shadow-xl z-50">
            <button
              onClick={onClose}
              aria-label={t('aria_close_menu', 'Close menu')}
              className="absolute top-4 right-4 p-1 text-gray-400 hover:text-gray-600"
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
    </>
  );
}
