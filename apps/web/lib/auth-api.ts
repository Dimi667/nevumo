import { apiPost } from "@/lib/api";
import type { AuthResult, CheckEmailResult, MessageResult, ValidateTokenResult } from "@/lib/auth-types";

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
): Promise<AuthResult> {
  return apiPost<AuthResult>("/api/v1/auth/register", { email, password, role, locale });
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
