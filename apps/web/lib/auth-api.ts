import { apiPost, API_BASE } from "@/lib/api";
import type { AuthResult, CheckEmailResult, MessageResult, ValidateTokenResult } from "@/lib/auth-types";

export interface SlugCheckResult {
  available: boolean;
  valid: boolean;
  error?: string;
  suggestions?: string[];
}

export function checkEmail(email: string): Promise<CheckEmailResult> {
  return apiPost<CheckEmailResult>("/api/v1/auth/check-email", { email });
}

export function loginWithEmail(email: string, password: string): Promise<AuthResult> {
  return apiPost<AuthResult>("/api/v1/auth/login", { email, password });
}

export function registerWithEmail(
  email: string,
  password: string,
  role: string,
  locale: string,
  slug?: string,
  citySlug?: string,
  categorySlug?: string,
  cityId?: number | null,
): Promise<AuthResult> {
  return apiPost<AuthResult>("/api/v1/auth/register", { 
    email, 
    password, 
    role, 
    locale,
    slug,
    city_slug: citySlug,
    category_slug: categorySlug,
    city_id: cityId,
  });
}

export function forgotPassword(email: string): Promise<MessageResult> {
  return apiPost<MessageResult>("/api/v1/auth/forgot-password", { email });
}

export function validateResetToken(token: string): Promise<ValidateTokenResult> {
  return apiPost<ValidateTokenResult>("/api/v1/auth/validate-reset-token", { token });
}

export function resetPassword(token: string, password: string): Promise<AuthResult> {
  return apiPost<AuthResult>("/api/v1/auth/reset-password", { token, password });
}

export function magicLinkAuth(token: string): Promise<AuthResult> {
  return apiPost<AuthResult>("/api/v1/auth/magic-link", { token });
}

export async function checkRegistrationSlugAvailability(
  slug: string,
  citySlug?: string,
  categorySlug?: string
): Promise<SlugCheckResult> {
  const params = new URLSearchParams({ slug });
  if (citySlug) params.set('city_slug', citySlug);
  if (categorySlug) params.set('category_slug', categorySlug);
  
  const res = await fetch(`${API_BASE}/api/v1/auth/register/slug/check?${params}`);
  const json = await res.json();
  
  if (!json.success) {
    throw new Error(json.error?.message || 'Failed to check slug availability');
  }
  
  return json.data;
}
