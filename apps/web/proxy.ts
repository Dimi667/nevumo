import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

import {
  LANGUAGE_COOKIE_MAX_AGE,
  LANGUAGE_COOKIE_NAME,
  LANGUAGE_HEADER_NAME,
  LANGUAGE_REDIRECT_COOKIE_MAX_AGE,
  LANGUAGE_REDIRECT_COOKIE_NAME,
  normalizeLanguage,
  resolveRequestLanguage,
} from "./lib/locales";

const STATIC_EXT_PATTERN = /\.(svg|png|jpg|jpeg|ico|css|js|txt|xml|json)$/i;
const METADATA_ROUTE_PATTERN = /^\/(icon|apple-icon|opengraph-image|twitter-image)(-[\w-]+)?(\/.*)?$/;

/**
 * Next.js 16 Proxy (formerly Middleware)
 * Handles language normalization, redirects, and header propagation.
 */
export default function proxy(request: NextRequest) {
  const pathname = request.nextUrl.pathname;

  // 1. Exclude internal and static routes
  if (
    pathname.startsWith("/_next") ||
    pathname.startsWith("/api/") ||
    /^\/[a-z]{2,5}\/api\//.test(pathname) ||
    STATIC_EXT_PATTERN.test(pathname) ||
    METADATA_ROUTE_PATTERN.test(pathname)
  ) {
    const response = NextResponse.next();
    response.headers.set('x-pathname', pathname);
    return response;
  }

  // 2. Resolve language from path, cookies, or headers
  const savedLang = normalizeLanguage(
    request.cookies.get(LANGUAGE_COOKIE_NAME)?.value
  );
  const redirectedLang = normalizeLanguage(
    request.cookies.get(LANGUAGE_REDIRECT_COOKIE_NAME)?.value
  );
  
  const pathSegments = pathname.split("/");
  const pathLangSegment = pathSegments[1];
  const lang = pathLangSegment ? normalizeLanguage(pathLangSegment) : null;

  // 3. Handle path language normalization (e.g., /BG -> /bg)
  if (lang && pathLangSegment !== lang) {
    const redirectUrl = request.nextUrl.clone();
    redirectUrl.pathname = ["", lang, ...pathSegments.slice(2)].join("/");

    const response = NextResponse.redirect(redirectUrl);
    response.cookies.set(LANGUAGE_COOKIE_NAME, lang, {
      path: "/",
      maxAge: LANGUAGE_COOKIE_MAX_AGE,
    });
    response.cookies.delete(LANGUAGE_REDIRECT_COOKIE_NAME);
    response.headers.set('x-pathname', redirectUrl.pathname);
    return response;
  }

  // 4. If language is in path, propagate to headers and set cookie
  if (lang) {
    const requestHeaders = new Headers(request.headers);
    requestHeaders.set(LANGUAGE_HEADER_NAME, lang);

    const response = NextResponse.next({
      request: {
        headers: requestHeaders,
      },
    });

    response.headers.set('x-pathname', pathname);

    if (savedLang !== lang || redirectedLang === lang) {
      response.cookies.set(LANGUAGE_COOKIE_NAME, lang, {
        path: "/",
        maxAge: LANGUAGE_COOKIE_MAX_AGE,
      });
    }
    
    if (redirectedLang) {
      response.cookies.delete(LANGUAGE_REDIRECT_COOKIE_NAME);
    }
    
    return response;
  }

  // 5. If no language in path, resolve and redirect
  const targetLang = resolveRequestLanguage({
    cookieLang: savedLang,
    acceptLanguage: request.headers.get("accept-language"),
  });

  const redirectUrl = request.nextUrl.clone();
  redirectUrl.pathname = pathname === "/" ? `/${targetLang}` : `/${targetLang}${pathname}`;

  const response = NextResponse.redirect(redirectUrl);
  response.headers.set('x-pathname', redirectUrl.pathname);

  if (savedLang) {
    response.cookies.delete(LANGUAGE_REDIRECT_COOKIE_NAME);
  } else {
    response.cookies.set(LANGUAGE_REDIRECT_COOKIE_NAME, targetLang, {
      path: "/",
      maxAge: LANGUAGE_REDIRECT_COOKIE_MAX_AGE,
    });
  }

  return response;
}

export const config = {
  matcher: ["/((?!_next|.*\\..*).*)"],
};
