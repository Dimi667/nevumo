export function isDashboardPath(pathname: string): boolean {
  return pathname.includes('/client/dashboard') || pathname.includes('/provider/dashboard');
}
