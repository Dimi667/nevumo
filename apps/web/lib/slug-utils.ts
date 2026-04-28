/**
 * Slug utilities for validation and sanitization
 */

import slugifyLib from 'slugify';

/**
 * Convert text to slug format (lowercase, replace special chars with hyphens)
 */
export function slugifyText(text: string): string {
  return slugifyLib(text, {
    lower: true,
    strict: true,
    trim: true,
    replacement: '-',
    locale: 'bg' // Добавяме поддръжка за българска транслитерация
  });
}

/**
 * Legacy slugify function for backward compatibility
 */
export function slugify(text: string): string {
  return slugifyText(text);
}

/**
 * Check if slug format is valid (no numeric suffixes, only lowercase/numbers/hyphens)
 */
export function isValidSlugFormat(slug: string): boolean {
  if (slug.length < 2 || slug.length > 50) return false;
  // Only lowercase, numbers, and single hyphen separators
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) return false;
  return true;
}

/**
 * Sanitize user input into a valid slug format
 */
export function sanitizeSlug(input: string): string {
  return input
    .toLowerCase()
    .replace(/[^a-z0-9-]/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-+/g, '');
}

/**
 * Get validation error message for a slug
 */
export function getSlugValidationError(slug: string): string | null {
  if (slug.length < 2) return 'Slug must be at least 2 characters';
  if (slug.length > 50) return 'Slug must be at most 50 characters';
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) {
    return 'Only lowercase letters, numbers, and hyphens allowed';
  }
  return null;
}
