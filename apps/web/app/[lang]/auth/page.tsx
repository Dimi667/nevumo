import { Metadata } from "next";
import LoginClient from "./LoginClient";
import { fetchTranslations } from "@/lib/ui-translations";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ lang: string }>;
}): Promise<Metadata> {
  const { lang } = await params;
  const dict = await fetchTranslations(lang, "auth");
  const title = dict?.page_title ?? "Login | Nevumo";
  const description = dict?.meta_description ?? "Sign in or create your Nevumo account.";
  return {
    title: { absolute: title },
    description,
    openGraph: { title, description },
    robots: { index: false, follow: false },
  };
}

export default async function AuthPage({
  params,
  searchParams,
}: {
  params: Promise<{ lang: string }>;
  searchParams: Promise<{ role?: string }>;
}) {
  const { lang } = await params;
  const { role } = await searchParams;
  const authDict = await fetchTranslations(lang, "auth");
  return <LoginClient lang={lang} initialRole={role ?? null} authDict={authDict} />;
}
