import { Metadata } from "next";
import OAuthTermsClient from "./OAuthTermsClient";
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

export default async function OAuthTermsPage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  const authDict = await fetchTranslations(lang, "auth");
  return <OAuthTermsClient lang={lang} authDict={authDict} />;
}
