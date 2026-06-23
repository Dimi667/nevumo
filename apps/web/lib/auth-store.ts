import type { UserInfo } from "@/lib/auth-types";

const TOKEN_KEY = "nevumo_auth_token";
const USER_KEY = "nevumo_auth_user";

export function saveAuth(token: string, user: UserInfo): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
  if (typeof document !== 'undefined') {
    document.cookie = `nevumo_auth_token=${token}; path=/; max-age=31536000; SameSite=Lax`;
  }
}

export function getAuthToken(): string | null {
  // Read from cookie first (source of truth), fallback to localStorage
  // for backwards compatibility during transition.
  if (typeof document !== 'undefined') {
    const cookie = document.cookie
      .split(';')
      .find(c => c.trim().startsWith('nevumo_auth_token='));
    if (cookie) {
      return cookie.trim().split('=').slice(1).join('=');
    }
  }
  // Fallback: localStorage (will be empty after users re-authenticate)
  if (typeof localStorage !== 'undefined') {
    return localStorage.getItem(TOKEN_KEY);
  }
  return null;
}

export function getAuthUser(): UserInfo | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? (JSON.parse(raw) as UserInfo) : null;
  } catch {
    return null;
  }
}

export function clearAuth(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  if (typeof document !== 'undefined') {
    document.cookie = 'nevumo_auth_token=; path=/; max-age=0; SameSite=Lax';
  }
}

export function isAuthenticated(): boolean {
  // Cookie is the single source of truth.
  // Works consistently with Server Components which also read the cookie.
  if (typeof document === 'undefined') return false;
  return document.cookie
    .split(';')
    .some(c => c.trim().startsWith('nevumo_auth_token='));
}
