'use client';

import { use, useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated, getAuthUser } from '@/lib/auth-store';
import { getProviderDashboard } from '@/lib/provider-api';
import { DashboardI18nProvider } from '@/lib/provider-dashboard-i18n';
import DashboardSidebar from '@/components/dashboard/DashboardSidebar';
import DashboardTopBar from '@/components/dashboard/DashboardTopBar';
import PWAInstallPrompt from '@/components/pwa/PWAInstallPrompt';

interface DashboardLayoutProps {
  children: React.ReactNode;
  params: Promise<{ lang: string }>;
}

export default function DashboardLayout({ children, params }: DashboardLayoutProps) {
  const { lang } = use(params);
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [ready, setReady] = useState(false);
  const [isOnboarding, setIsOnboarding] = useState(false);
  const [showPWAPrompt, setShowPWAPrompt] = useState(false);

  const checkOnboardingStatus = useCallback(async (forceRefresh = false) => {
    try {
      const dashboard = await getProviderDashboard();
      const newIsOnboarding = !dashboard.profile.is_complete;
      
      if (forceRefresh) {
        setIsOnboarding(newIsOnboarding);
      }
      
      return newIsOnboarding;
    } catch {
      const newIsOnboarding = false;
      if (forceRefresh) {
        setIsOnboarding(newIsOnboarding);
      }
      return newIsOnboarding;
    }
  }, []);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace(`/${lang}/auth`);
      return;
    }
    const user = getAuthUser();
    if (!user) {
      router.replace(`/${lang}/auth`);
      return;
    }
    if (user.role !== 'provider') {
      router.replace(`/${lang}/client/dashboard`);
      return;
    }

    // Check if user is in onboarding mode
    checkOnboardingStatus(true).then(() => setReady(true));
  }, [lang, router, checkOnboardingStatus]);

  // Re-check onboarding status when route changes (for post-onboarding refresh)
  useEffect(() => {
    if (ready) {
      checkOnboardingStatus();
    }
  }, [ready, checkOnboardingStatus]);

  // Listen for custom events to force refresh onboarding status
  useEffect(() => {
    const handleForceRefresh = () => {
      checkOnboardingStatus(true);
    };

    window.addEventListener('force-onboarding-refresh', handleForceRefresh);
    return () => {
      window.removeEventListener('force-onboarding-refresh', handleForceRefresh);
    };
  }, [checkOnboardingStatus]);

  // Listen for onboarding complete to show PWA install prompt
  useEffect(() => {
    const handleOnboardingComplete = () => {
      setTimeout(() => setShowPWAPrompt(true), 1500);
    };

    window.addEventListener('nevumo:onboarding_complete', handleOnboardingComplete);
    return () => {
      window.removeEventListener('nevumo:onboarding_complete', handleOnboardingComplete);
    };
  }, []);

  if (!ready) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <DashboardI18nProvider lang={lang}>
      <div className={isOnboarding ? 'bg-gray-50' : 'min-h-screen bg-gray-50 flex'}>
        {/* Hide sidebar completely during onboarding */}
        {!isOnboarding && (
          <DashboardSidebar
            open={sidebarOpen}
            onClose={() => setSidebarOpen(false)}
            lang={lang}
          />
        )}

        <div className={isOnboarding ? 'w-full max-w-2xl mx-auto' : 'flex-1 flex flex-col min-w-0'}>
          {/* Hide top bar during onboarding to remove menu button */}
          {!isOnboarding ? (
            <DashboardTopBar
              onMenuClick={() => setSidebarOpen(true)}
              lang={lang}
            />
          ) : (
            <div className="h-16 flex-shrink-0" /> // Spacer to maintain layout
          )}
          <main
            className={isOnboarding ? 'p-4 md:p-6 w-full' : 'flex-1 p-4 md:p-6 overflow-auto overscroll-contain'}
            style={isOnboarding ? undefined : { WebkitOverflowScrolling: 'touch' }}
          >
            {children}
          </main>
          {showPWAPrompt && (
            <PWAInstallPrompt
              trigger="onboarding_complete"
              role="provider"
              onClose={() => setShowPWAPrompt(false)}
            />
          )}
        </div>
      </div>
    </DashboardI18nProvider>
  );
 }
