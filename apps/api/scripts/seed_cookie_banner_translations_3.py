#!/usr/bin/env python3
"""
Seed cookie banner translations - Batch 3.
Namespace: cookie_banner
Keys: 16 | Languages: 10 (pt-PT, ro, ru, sk, sl, sq, sr, sv, tr, uk)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_cookie_banner_translations_3
"""

import os

from sqlalchemy import create_engine, text

NAMESPACE = "cookie_banner"

TRANSLATIONS = {
    "cookie_title": {
        "pt-PT": "Utilizamos cookies",
        "ro": "Folosim module cookie",
        "ru": "Мы используем файлы cookie",
        "sk": "Používame súbory cookie",
        "sl": "Uporabljamo piškotke",
        "sq": "Ne përdorim cookies",
        "sr": "Користимо колачиће",
        "sv": "Vi använder cookies",
        "tr": "Çerezler kullanıyoruz",
        "uk": "Ми використовуємо файли cookie",
    },
    "cookie_description": {
        "pt-PT": "Utilizamos cookies e tecnologias semelhantes para melhorar a sua experiência, analisar o tráfego e apresentar conteúdo relevante. Pode escolher quais as categorias que pretende permitir.",
        "ro": "Folosim module cookie și tehnologii similare pentru a vă îmbunătăți experiența, a analiza traficul și a afișa conținut relevant. Puteți alege ce categorii să permiteți.",
        "ru": "Мы используем файлы cookie и аналогичные технологии для улучшения Вашего опыта, анализа трафика и показа релевантного контента. Вы можете выбрать, какие категории разрешить.",
        "sk": "Používame súbory cookie a podobné technológie na zlepšenie vášho zážitku, analýzu návštevnosti a zobrazovanie relevantného obsahu. Môžete si vybrať, ktoré kategórie povolíte.",
        "sl": "Uporabljamo piškotke in podobne tehnologije za izboljšanje vaše izkušnje, analizo prometa in prikaz ustrezne vsebine. Izberete lahko, katere kategorije želite dovoliti.",
        "sq": "Ne përdorim cookies dhe teknologji të ngjashme për të përmirësuar përvojën tuaj, për të analizuar trafikun dhe për të shfaqur përmbajtje të rëndësishme. Ju mund të zgjidhni se cilat kategori të lejoni.",
        "sr": "Користимо колачиће и сличне технологије kako bismo побољшали ваше искуство, анализирали саобраћај и приказали релевантан садржај. Можете изабрати које категорије желите да дозволите.",
        "sv": "Vi använder cookies och liknande tekniker för att förbättra din upplevelse, analysera trafik och visa relevant innehåll. Du kan välja vilka kategorier du vill tillåta.",
        "tr": "Deneyiminizi geliştirmek, trafiği analiz etmek ve ilgili içeriği göstermek için çerezler ve benzer teknolojiler kullanıyoruz. Hangi kategorilere izin vereceğinizi seçebilirsiniz.",
        "uk": "Ми використовуємо файли cookie та подібні технології, щоб покращити Ваш досвід, аналізувати трафік і показувати релевантний контент. Ви можете обрати, які категорії дозволити.",
    },
    "accept_all": {
        "pt-PT": "Aceitar tudo",
        "ro": "Acceptă toate",
        "ru": "Принять все",
        "sk": "Prijať všetky",
        "sl": "Sprejmi vse",
        "sq": "Prano të gjitha",
        "sr": "Прихвати све",
        "sv": "Acceptera alla",
        "tr": "Tümünü kabul et",
        "uk": "Прийняти всі",
    },
    "reject_all": {
        "pt-PT": "Rejeitar tudo",
        "ro": "Respinge toate",
        "ru": "Отклонить все",
        "sk": "Odmietnuť všetky",
        "sl": "Zavrni vse",
        "sq": "Refuzo të gjitha",
        "sr": "Одбиј све",
        "sv": "Avvisa alla",
        "tr": "Tümünü reddet",
        "uk": "Відхилити всі",
    },
    "customize": {
        "pt-PT": "Personalizar",
        "ro": "Personalizează",
        "ru": "Настроить",
        "sk": "Prispôsobiť",
        "sl": "Prilagodi",
        "sq": "Personalizo",
        "sr": "Прилагоди",
        "sv": "Anpassa",
        "tr": "Özelleştir",
        "uk": "Налаштувати",
    },
    "necessary_label": {
        "pt-PT": "Necessários",
        "ro": "Necesare",
        "ru": "Необходимые",
        "sk": "Nevyhnutné",
        "sl": "Nujni",
        "sq": "Të nevojshme",
        "sr": "Неопходни",
        "sv": "Nödvändiga",
        "tr": "Gerekli",
        "uk": "Необхідні",
    },
    "necessary_description": {
        "pt-PT": "Necessários para o funcionamento do site. Não podem ser desativados.",
        "ro": "Necesare pentru funcționarea site-ului. Nu pot fi dezactivate.",
        "ru": "Необходимы для работы сайта. Не могут быть отключены.",
        "sk": "Potrebné na fungovanie webovej stránky. Nedajú sa zakázať.",
        "sl": "Potrebni za delovanje spletnega mesta. Ni jih mogoče onemogočiti.",
        "sq": "Të nevojshme për funksionimin e faqes së internetit. Nuk mund të çaktivizohen.",
        "sr": "Потребни за рад веб-сајта. Не могу се онемогућити.",
        "sv": "Krävs för att webbplatsen ska fungera. Kan inte inaktiveras.",
        "tr": "Web sitesinin çalışması için gereklidir. Devre dışı bırakılamaz.",
        "uk": "Необхідні для роботи веб-сайту. Не можуть бути вимкнені.",
    },
    "functional_label": {
        "pt-PT": "Funcionais",
        "ro": "Funcționale",
        "ru": "Функциональные",
        "sk": "Funkčné",
        "sl": "Funkcionalni",
        "sq": "Funksionale",
        "sr": "Функционални",
        "sv": "Funktionella",
        "tr": "İşlevsel",
        "uk": "Функціональні",
    },
    "functional_description": {
        "pt-PT": "Memorizam as suas preferências e definições entre visitas.",
        "ro": "Memorează preferințele și setările dvs. între vizite.",
        "ru": "Запоминают Ваши предпочтения и настройки между посещениями.",
        "sk": "Zapamätajú si vaše predvoľby a nastavenia medzi návštevami.",
        "sl": "Zapomnijo si vaše nastavitve in preference medzi obiski.",
        "sq": "Mbajnë mend preferencat dhe cilësimet tuaja gjatë vizitave.",
        "sr": "Памте ваше поставке и подешавања између посета.",
        "sv": "Kommer ihåg dina inställningar och preferenser mellan besök.",
        "tr": "Tercihlerinizi ve ayarlarınızı ziyaretler arasında hatırlar.",
        "uk": "Запам'ятовують Ваші уподобання та налаштування між відвідуваннями.",
    },
    "analytics_label": {
        "pt-PT": "Análise",
        "ro": "Analitice",
        "ru": "Аналитические",
        "sk": "Analytické",
        "sl": "Analitični",
        "sq": "Analitike",
        "sr": "Аналитички",
        "sv": "Analys",
        "tr": "Analitik",
        "uk": "Аналітичні",
    },
    "analytics_description": {
        "pt-PT": "Ajudam-nos a compreender como os visitantes utilizam o nosso site.",
        "ro": "Ne ajută să înțelegem modul în care vizitatorii folosesc site-ul nostru.",
        "ru": "Помогают нам понять, как посетители используют наш сайт.",
        "sk": "Pomáhajú nám pochopiť, ako návštevníci používajú našu webovú stránku.",
        "sl": "Pomagajo nam razumeti, kako obiskovalci uporabljajo naše spletno mesto.",
        "sq": "Na ndihmojnë të kuptojmë se si vizitorët përdorin faqen tonë.",
        "sr": "Помажу нам да разумемо kako посетиоци користе наш веб-сајт.",
        "sv": "Hjälper oss att förstå hur besökare använder vår webbplats.",
        "tr": "Ziyaretçilerin web sitemizi nasıl kullandığını anlamamıza yardımcı olur.",
        "uk": "Допомагають нам зрозуміти, як відвідувачі використовують наш веб-сайт.",
    },
    "marketing_label": {
        "pt-PT": "Marketing",
        "ro": "Marketing",
        "ru": "Маркетинговые",
        "sk": "Marketingové",
        "sl": "Trženjski",
        "sq": "Marketing",
        "sr": "Маркетиншки",
        "sv": "Marknadsföring",
        "tr": "Pazarlama",
        "uk": "Маркетингові",
    },
    "marketing_description": {
        "pt-PT": "Utilizados para lhe apresentar anúncios relevantes noutras plataformas.",
        "ro": "Utilizate pentru a vă afișa reclame relevante pe alte platforme.",
        "ru": "Используются для показа Вам релевантной рекламы на других платформах.",
        "sk": "Používajú sa na zobrazovanie relevantných reklám na iných platformách.",
        "sl": "Uporabljajo se za prikazovanje ustreznih oglasov na drugih platformah.",
        "sq": "Përdoren për t'ju shfaqur reklama të rëndësishme në platforma të tjera.",
        "sr": "Користе се за приказивање релевантних огласа на другим платформама.",
        "sv": "Används för att visa dig relevanta annonser på andra plattformar.",
        "tr": "Diğer platformlarda size ilgili reklamları göstermek için kullanılır.",
        "uk": "Використовуються для показу Вам релевантної реклами на інших платформах.",
    },
    "save_preferences": {
        "pt-PT": "Guardar preferências",
        "ro": "Salvează preferințele",
        "ru": "Сохранить настройки",
        "sk": "Uložiť predvoľby",
        "sl": "Shrani nastavitve",
        "sq": "Ruaj preferencat",
        "sr": "Сачувај поставке",
        "sv": "Spara inställningar",
        "tr": "Tercihleri kaydet",
        "uk": "Зберегти налаштування",
    },
    "cookie_settings_link": {
        "pt-PT": "Definições de cookies",
        "ro": "Setări cookie",
        "ru": "Настройки cookie",
        "sk": "Nastavenia súborov cookie",
        "sl": "Nastavitve piškotkov",
        "sq": "Cilësimet e cookies",
        "sr": "Подешавања колачића",
        "sv": "Cookieinställningar",
        "tr": "Çerez ayarları",
        "uk": "Налаштування файлів cookie",
    },
    "last_updated": {
        "pt-PT": "Última atualização: {date}",
        "ro": "Ultima actualizare: {date}",
        "ru": "Последнее обновление: {date}",
        "sk": "Naposledy aktualizované: {date}",
        "sl": "Zadnja posodobitev: {date}",
        "sq": "Përditësuar së fundmi: {date}",
        "sr": "Последње ажурирање: {date}",
        "sv": "Senast uppdaterad: {date}",
        "tr": "Son güncelleme: {date}",
        "uk": "Останнє оновлення: {date}",
    },
}


def get_database_url() -> str:
    """Get database URL from environment or use default."""
    return os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")


def seed_translations() -> None:
    """Seed all cookie banner translations into the database."""
    engine = create_engine(get_database_url())

    with engine.connect() as conn:
        count = 0
        for key_base, translations in TRANSLATIONS.items():
            full_key = f"{NAMESPACE}.{key_base}"
            for lang, value in translations.items():
                conn.execute(
                    text("""
                        INSERT INTO translations (lang, key, value)
                        VALUES (:lang, :key, :value)
                        ON CONFLICT (lang, key)
                        DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"lang": lang, "key": full_key, "value": value}
                )
                count += 1

        conn.commit()
        print(f"Inserted/updated {count} translation rows for namespace '{NAMESPACE}'")


def verify_translations() -> None:
    """Verify the translations were inserted correctly."""
    engine = create_engine(get_database_url())

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT lang, COUNT(*) as keys
                FROM translations
                WHERE key LIKE :pattern
                GROUP BY lang
                ORDER BY lang
            """),
            {"pattern": f"{NAMESPACE}.%"}
        )
        rows = result.fetchall()
        print(f"\nVerification for namespace '{NAMESPACE}':")
        for row in rows:
            print(f"  {row[0]}: {row[1]} keys")


if __name__ == "__main__":
    seed_translations()
    verify_translations()
