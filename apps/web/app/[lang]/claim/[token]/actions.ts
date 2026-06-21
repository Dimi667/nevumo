'use server';

import { redirect } from 'next/navigation';

export async function claimProfile(token: string, authToken: string): Promise<{ success: boolean; errorCode?: string }> {
  try {
    const apiUrl = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/api/v1/providers/claim/${token}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        return { success: false, errorCode: 'auth_expired' };
      }
      const errorData = await response.json().catch(() => ({}));
      const code = errorData?.detail?.code || '';
      if (code === 'ALREADY_CLAIMED') return { success: false, errorCode: 'already_claimed' };
      if (code === 'USER_ALREADY_HAS_PROVIDER') return { success: false, errorCode: 'user_has_provider' };
      if (response.status === 404) return { success: false, errorCode: 'not_found' };
      return { success: false, errorCode: 'network' };
    }

    return { success: true };
  } catch {
    return { success: false, errorCode: 'network' };
  }
}

export async function claimProfileAction(token: string, authToken: string, normalizedLang: string) {
  const claimResult = await claimProfile(token, authToken);
  if (claimResult.success) {
    redirect(`/${normalizedLang}/provider/dashboard`);
  }
  redirect(`/${normalizedLang}/claim/${token}?error=${claimResult.errorCode || 'network'}`);
}
