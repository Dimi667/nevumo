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

export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname;
  console.log("[Middleware] pathname:", pathname);

  // Exclude API routes from middleware logic
  if (pathname.startsWith("/api/") || /^\/[a-z]{2,5}\/api\//.test(pathname)) {
    return NextResponse.next();
  }

  if (STATIC_EXT_PATTERN.test(pathname)) {
    return NextResponse.next();
  }

  const savedLang = normalizeLanguage(
    request.cookies.get(LANGUAGE_COOKIE_NAME)?.value
  );
  const redirectedLang = normalizeLanguage(
    request.cookies.get(LANGUAGE_REDIRECT_COOKIE_NAME)?.value
  );
  const pathSegments = pathname.split("/");
  const pathLangSegment = pathSegments[1];
  const lang = pathLangSegment ? normalizeLanguage(pathLangSegment) : null;

  if (lang && pathLangSegment !== lang) {
    const redirectUrl = request.nextUrl.clone();
    redirectUrl.pathname = ["", lang, ...pathSegments.slice(2)].join("/");

    const response = NextResponse.redirect(redirectUrl);
    response.cookies.set(LANGUAGE_COOKIE_NAME, lang, {
      path: "/",
      maxAge: LANGUAGE_COOKIE_MAX_AGE,
    });
    response.cookies.delete(LANGUAGE_REDIRECT_COOKIE_NAME);
    return response;
  }

  if (lang) {
    const requestHeaders = new Headers(request.headers);
    requestHeaders.set(LANGUAGE_HEADER_NAME, lang);

    const response = NextResponse.next({
      request: {
        headers: requestHeaders,
      },
    });
    if (savedLang || redirectedLang !== lang) {
      response.cookies.set(LANGUAGE_COOKIE_NAME, lang, {
        path: "/",
        maxAge: LANGUAGE_COOKIE_MAX_AGE,
      });
    }
    response.cookies.delete(LANGUAGE_REDIRECT_COOKIE_NAME);
    return response;
  }

  const targetLang = resolveRequestLanguage({
    cookieLang: savedLang,
    acceptLanguage: request.headers.get("accept-language"),
  });
  const redirectUrl = request.nextUrl.clone();
  redirectUrl.pathname =
    pathname === "/" ? `/${targetLang}` : `/${targetLang}${pathname}`;
  const response = NextResponse.redirect(redirectUrl);

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
