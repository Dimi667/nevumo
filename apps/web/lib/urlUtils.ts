/**
 * URL Resolution Utilities
 * Handles static file URLs that work across local dev, local network, and production with CDN
 */

/**
 * Resolves a static file URL to work in all environments
 * 
 * Logic:
 * - If URL is already absolute (starts with http/https), use as-is (CDN in production)
 * - If URL is relative (starts with /api/v1/static/), use as-is (browser resolves to current domain)
 * 
 * This avoids hydration mismatch by ensuring server and client render identical HTML.
 * 
 * @param url - The URL from backend (can be relative or absolute)
 * @returns URL that works in current environment
 */
export function resolveStaticUrl(url: string | null | undefined): string | null {
  if (!url) return null;

  // If already absolute (CDN in production), use as-is
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url;
  }

  // For relative URLs, return as-is (browser resolves to current domain)
  return url;
}
