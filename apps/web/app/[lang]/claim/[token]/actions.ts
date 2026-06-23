'use server';

import { redirect } from 'next/navigation';

export async function claimProfile(token: string, authToken: string): Promise<{ success: boolean; errorCode?: string; pendingVerification?: boolean }> {
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
      if (response.status === 422) {
        const errorData = await response.json().catch(() => ({}));
        if (errorData?.detail === 'cannot_verify_ownership') {
          return { success: false, errorCode: 'ownership_blocked' };
        }
        return { success: false, errorCode: 'network' };
      }
      const errorData = await response.json().catch(() => ({}));
      const code = errorData?.detail?.code || '';
      if (code === 'ALREADY_CLAIMED') return { success: false, errorCode: 'already_claimed' };
      if (code === 'USER_ALREADY_HAS_PROVIDER') return { success: false, errorCode: 'user_has_provider' };
      if (response.status === 404) return { success: false, errorCode: 'not_found' };
      return { success: false, errorCode: 'network' };
    }

    // Check for pending_verification (202 status)
    if (response.status === 202) {
      const data = await response.json().catch(() => ({}));
      if (data?.status === 'pending_verification') {
        return { success: false, errorCode: 'pending_verification', pendingVerification: true };
      }
    }

    return { success: true };
  } catch {
    return { success: false, errorCode: 'network' };
  }
}

export async function claimProfileAction(token: string, authToken: string, normalizedLang: string) {
  const claimResult = await claimProfile(token, authToken);
  if (claimResult.success) {
    redirect(`/${normalizedLang}/provider/dashboard/profile`);
  }
  if (claimResult.pendingVerification) {
    redirect(`/${normalizedLang}/claim/${token}/verify`);
  }
  redirect(`/${normalizedLang}/claim/${token}?error=${claimResult.errorCode || 'network'}`);
}
