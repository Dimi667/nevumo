'use client';

import { useRouter } from 'next/navigation';
import { clearAuth, getAuthUser } from '@/lib/auth-store';
import { useDashboardI18n } from '@/lib/provider-dashboard-i18n';

interface DashboardTopBarProps {
  onMenuClick: () => void;
  lang: string;
  publicUrl?: string;
}

export default function DashboardTopBar({ onMenuClick, lang, publicUrl }: DashboardTopBarProps) {
  const router = useRouter();
  const user = getAuthUser();
  const { t } = useDashboardI18n();

  function handleLogout() {
    clearAuth();
    // Ensure localStorage is cleared before redirect
    requestAnimationFrame(() => {
      router.push(`/${lang}`);
    });
  }

  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-4 md:px-6 flex-shrink-0">
      {/* Left side */}
      <div className="flex items-center gap-3">
        {/* Mobile menu button */}
        <button
          onClick={onMenuClick}
          className="md:hidden p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
          aria-label={t('aria_open_menu', 'Open menu')}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </svg>
        </button>

        {/* Spacer for desktop (sidebar takes left space) */}
        <div className="hidden md:block" />

        {/* Public profile button - left side on desktop */}
        {publicUrl && (
          <a
            href={publicUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-orange-600 hover:text-orange-700 hover:bg-orange-50 rounded-lg transition-colors border border-orange-200 hover:border-orange-300"
          >
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
            <span>{t('btn_view_profile', 'View my profile')}</span>
          </a>
        )}
      </div>

      {/* Right side */}
      <div className="flex items-center gap-3">
        {user?.email && (
          <span className="hidden sm:block text-sm text-gray-500 truncate max-w-[200px]">
            {user.email}
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
          <span className="hidden sm:inline">{t('btn_log_out', 'Log out')}</span>
        </button>
      </div>
    </header>
  );
}
