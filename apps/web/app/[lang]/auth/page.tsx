import { Metadata } from "next";
import LoginClient from "./LoginClient";

export const metadata: Metadata = {
  title: { absolute: "Вход | Nevumo" },
  robots: { index: false, follow: false },
};

export default async function AuthPage({
  params,
  searchParams,
}: {
  params: Promise<{ lang: string }>;
  searchParams: Promise<{ role?: string }>;
}) {
  const { lang } = await params;
  const { role } = await searchParams;
  return <LoginClient lang={lang} initialRole={role ?? null} />;
}
