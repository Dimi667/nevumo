export interface UserInfo {
  id: string;
  email: string;
  role: string;
  locale: string;
  country_code?: string;
}

export interface AuthResult {
  token: string;
  user: UserInfo;
  redirect?: string;
}

export interface CheckEmailResult {
  exists: boolean;
  has_password: boolean;
  role: string | null;
  oauth_connected: boolean;
}

export interface ValidateTokenResult {
  valid: boolean;
  error?: "expired" | "used" | "invalid";
}

export interface MessageResult {
  message: string;
}
