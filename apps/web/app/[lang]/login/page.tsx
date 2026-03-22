import { Metadata } from "next";
import Image from "next/image";
import { getDictionary } from "@/lib/locales";
import { LoginCards } from "./LoginCards";

export async function generateMetadata({ params }: { params: Promise<{ lang: string }> }): Promise<Metadata> {
  const { lang } = await params;
  const dictionary = await getDictionary(lang);
  const login = dictionary.login ?? {};

  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "https://nevumo.com";
  const fullUrl = `${baseUrl}/${lang}/login`;
  const metaTitle = login['login:metaTitle'] || "Nevumo – Find services or start offering services";
  const metaDescription = login['login:metaDescription'] || "Discover and book services or start offering yours on Nevumo. Free registration and quick start for clients and providers.";

  return {
    title: { absolute: metaTitle },
    description: metaDescription,
    alternates: { canonical: fullUrl },
    robots: { index: false, follow: true },
    openGraph: {
      title: metaTitle,
      description: metaDescription,
      url: fullUrl,
      siteName: 'Nevumo',
      type: 'website',
    },
  };
}

export default async function LoginPage({ params }: { params: Promise<{ lang: string }> }) {
  const { lang } = await params;
  const dictionary = await getDictionary(lang);
  const login = dictionary.login ?? {};

  return (
    <main className="flex flex-col items-center justify-start min-h-screen bg-[#f9f9f9] pt-20 px-4">
      <div className="w-full max-w-[400px] flex flex-col items-center">

        {/* Лого */}
        <div className="mb-6">
          <Image
            src="/Nevumo_logo.svg"
            alt="Nevumo"
            height={44}
            width={120}
            priority
            style={{ width: 'auto', height: '44px' }}
          />
        </div>

        {/* Заглавие */}
        <h1 className="text-[22px] font-bold text-[#171717] text-center leading-tight tracking-tight px-2 mb-6">
          {login['login:heading'] || "Find or offer a service!"}
        </h1>

        {/* Карти */}
        <div className="flex flex-col gap-4 mb-10 w-full">
          <LoginCards
            lang={lang}
            findLabel={login['login:findService.label'] || "Find a service"}
            findSubtext={login['login:findService.subtext'] || "Search and book services. You can become a provider later."}
            offerLabel={login['login:offerService.label'] || "Offer services"}
            offerSubtext={login['login:offerService.subtext'] || "Create your profile and offer services. You can always search for services as a client."}
          />
        </div>

        {/* UX Блок */}
        <div className="flex flex-col items-center w-full">

          {/* Текстът "Можеш да използваш..." */}
          <p className="text-[#666] text-[14px] font-medium text-center mb-8">
            {login['login:footerNote'] || "You can search and offer services with one account"}
          </p>

          {/* Центриран контейнер, в който чекчетата са подравнени вляво */}
          <div className="inline-block text-left">
            <div className="flex items-center gap-2 text-[#171717] text-[15px] font-bold mb-2">
              <span className="text-green-600 mr-1">✔</span>
              <span>{login['login:featureFree'] || "Free registration"}</span>
            </div>
            <div className="flex items-center gap-2 text-[#171717] text-[15px] font-bold">
              <span className="text-green-600 mr-1">✔</span>
              <span>{login['login:featureTime'] || "Takes less than 1 minute"}</span>
            </div>
          </div>
        </div>

        {/* Футър */}
        <footer className="mt-20 pb-10 flex flex-col items-center gap-3 w-full">
          <p className="text-[#aaa] text-[10px] font-bold uppercase tracking-[0.25em]">
            Nevumo &copy; 2026
          </p>
        </footer>

      </div>
    </main>
  );
}
