import { cookies, headers } from "next/headers";
import { redirect } from "next/navigation";

import {
  LANGUAGE_COOKIE_NAME,
  resolveRequestLanguage,
} from "../lib/locales";

export default async function HomePage() {
  const headerStore = await headers();
  const cookieStore = await cookies();
  const targetLang = resolveRequestLanguage({
    cookieLang: cookieStore.get(LANGUAGE_COOKIE_NAME)?.value,
    acceptLanguage: headerStore.get("accept-language"),
  });

  redirect(`/${targetLang}`);
}
