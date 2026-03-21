import { Metadata } from "next";
import Image from "next/image";
import { getDictionary } from "@/lib/locales";
import { ActionCard } from "@/components/ui/ActionCard";

export async function generateMetadata({ params }: { params: Promise<{ lang: string }> }): Promise<Metadata> {
  const { lang } = await params;
  const dictionary = await getDictionary(lang);
  const login = dictionary.login ?? {};

  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? "https://nevumo.com";

  return {
    title: login['login:metaTitle'] || "Вход | Nevumo",
    description: login['login:metaDescription'] || "Намери професионални услуги или предложи своите в Nevumo.",
    alternates: { canonical: `${baseUrl}/${lang}/login` },
    robots: { index: false, follow: true },
  };
}

export default async function LoginPage({ params }: { params: Promise<{ lang: string }> }) {
  const { lang } = await params;
  const dictionary = await getDictionary(lang);
  const login = dictionary.login ?? {};

  return (
    <main 
      style={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        justifyContent: 'flex-start', 
        minHeight: '100vh', 
        backgroundColor: '#f9f9f9',
        paddingTop: '80px', 
        paddingLeft: '16px',
        paddingRight: '16px'
      }}
    >
      <div style={{ width: '100%', maxWidth: '400px' }} className="flex flex-col items-center">
        
        {/* Лого */}
        <div style={{ marginBottom: '1.5rem' }}>
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
        <h1 
          style={{ marginBottom: '1.5rem' }}
          className="text-[22px] font-bold text-[#171717] text-center leading-tight tracking-tight px-2"
        >
          {login['login:heading'] || "Намери услуга или започни да предлагаш!"}
        </h1>

        {/* Карти */}
        <div className="flex flex-col w-full" style={{ gap: '1rem', marginBottom: '40px' }}>
          <ActionCard 
            href={`/${lang}/auth?role=client`}
            label={login['login:findService.label'] || "Намери услуга"}
            subtext={login['login:findService.subtext'] || "Търси и резервирай услуги."}
          />
          <ActionCard 
            href={`/${lang}/auth?role=provider`}
            label={login['login:offerService.label'] || "Предлагай услуги"}
            subtext={login['login:offerService.subtext'] || "Предлагай услуги и създай профил."}
          />
        </div>

        {/* UX Блок */}
        <div className="flex flex-col items-center w-full">
          
          {/* Текстът "Можеш да използваш..." */}
          <p className="text-[#666] text-[14px] font-medium text-center mb-8"> 
            {login['login:footerNote'] || "Можеш да използваш платформата и по двата начина"}
          </p>
          
          {/* Центриран контейнер, в който чекчетата са подравнени вляво */}
          <div style={{ display: 'inline-block', textAlign: 'left' }}>
            <div className="flex items-center gap-2 text-[#171717] text-[15px] font-bold mb-2">
              <span className="text-green-500 text-lg"></span> 
              <span>{login['login:featureFree'] || "✔ Безплатна регистрация"}</span>
            </div>
            <div className="flex items-center gap-2 text-[#171717] text-[15px] font-bold">
              <span className="text-green-500 text-lg"></span> 
              <span>{login['login:featureTime'] || "✔ Отнема под 1 минута"}</span>
            </div>
          </div>
        </div>

        {/* Футър */}
        <footer
          style={{ marginTop: '80px', paddingBottom: '40px' }}
          className="flex flex-col items-center gap-3 w-full"
        >
          {/* SEO линкове към важни страници */}
          <nav className="flex items-center gap-4">
            <a
              href={`/${lang}`}
              className="text-[#aaa] text-[11px] font-medium uppercase tracking-[0.15em] hover:text-[#666] transition-colors"
            >
              {login['login:nav.home'] || "Начало"}
            </a>
            <span className="text-[#ddd] text-[11px]">&nbsp;·&nbsp;</span>
            <a
              href={`/${lang}/services`}
              className="text-[#aaa] text-[11px] font-medium uppercase tracking-[0.15em] hover:text-[#666] transition-colors"
            >
              {login['login:nav.services'] || "Услуги"}
            </a>
          </nav>

          <p className="text-[#aaa] text-[10px] font-bold uppercase tracking-[0.25em]">
            Nevumo &copy; 2026
          </p>
        </footer>

      </div>
    </main>
  );
}