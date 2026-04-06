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
}

export interface CheckEmailResult {
  exists: boolean;
}

export interface ValidateTokenResult {
  valid: boolean;
  error?: "expired" | "used" | "invalid";
}

export interface MessageResult {
  message: string;
}
