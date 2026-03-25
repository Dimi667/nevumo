'use client';

import { use, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated, getAuthUser } from '@/lib/auth-store';
import DashboardSidebar from '@/components/dashboard/DashboardSidebar';
import DashboardTopBar from '@/components/dashboard/DashboardTopBar';

interface DashboardLayoutProps {
  children: React.ReactNode;
  params: Promise<{ lang: string }>;
}

export default function DashboardLayout({ children, params }: DashboardLayoutProps) {
  const { lang } = use(params);
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace(`/${lang}/auth`);
      return;
    }
    const user = getAuthUser();
    if (user?.role !== 'provider') {
      router.replace(`/${lang}/client/dashboard`);
      return;
    }
    setReady(true);
  }, [lang, router]);

  if (!ready) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex">
      <DashboardSidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        lang={lang}
      />

      <div className="flex-1 flex flex-col min-w-0">
        <DashboardTopBar
          onMenuClick={() => setSidebarOpen(true)}
          lang={lang}
        />
        <main className="flex-1 p-4 md:p-6 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
