"""
seed_cookies_browser_paths_p3.py — Nevumo | namespace: cookies
Section 6 · Browser settings paths — езици 18–34 (lv → uk)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_cookies_browser_paths_p3
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nevumo:nevumo@postgres:5432/nevumo_leads",
)

NAMESPACE = "cookies"

TRANSLATIONS: dict[str, dict[str, str]] = {

    "s6_chrome_path": {
        "lv":    "Iestatījumi → Privātums un drošība → Sīkfaili un citi vietnes dati",
        "mk":    "Поставки → Приватност и безбедност → Колачиња и други податоци на сајтот",
        "mt":    "Settings → Privatezza u sigurtà → Cookies u dejta oħra tas-sit",
        "nl":    "Instellingen → Privacy en beveiliging → Cookies en andere sitegegevens",
        "no":    "Innstillinger → Personvern og sikkerhet → Informasjonskapsler og andre nettsteddata",
        "pl":    "Ustawienia → Prywatność i bezpieczeństwo → Pliki cookie i inne dane witryn",
        "pt":    "Configurações → Privacidade e segurança → Cookies e outros dados do site",
        "pt-PT": "Definições → Privacidade e segurança → Cookies e outros dados de sites",
        "ro":    "Setări → Confidențialitate și securitate → Cookie-uri și alte date ale site-urilor",
        "ru":    "Настройки → Конфиденциальность и безопасность → Файлы cookie и другие данные сайтов",
        "sk":    "Nastavenia → Súkromie a bezpečnosť → Súbory cookie a ďalšie údaje webu",
        "sl":    "Nastavitve → Zasebnost in varnost → Piškotki in drugi podatki spletnih mest",
        "sq":    "Cilësimet → Privatësia dhe siguria → Skedarët e skedarëve dhe të dhëna të tjera të faqes",
        "sr":    "Подешавања → Приватност и безбедност → Колачићи и други подаци сајта",
        "sv":    "Inställningar → Sekretess och säkerhet → Cookies och annan webbplatsdata",
        "tr":    "Ayarlar → Gizlilik ve güvenlik → Çerezler ve diğer site verileri",
        "uk":    "Налаштування → Конфіденційність і безпека → Файли cookie та інші дані сайтів",
    },

    "s6_firefox_path": {
        "lv":    "Iestatījumi → Privātums un drošība → Sīkfaili un vietnes dati",
        "mk":    "Поставки → Приватност и безбедност → Колачиња и податоци на сајтот",
        "mt":    "Settings → Privatezza & Sigurtà → Cookies u Dejta tas-Sit",
        "nl":    "Instellingen → Privacy & Beveiliging → Cookies en sitegegevens",
        "no":    "Innstillinger → Personvern og sikkerhet → Informasjonskapsler og nettsteddata",
        "pl":    "Ustawienia → Prywatność i bezpieczeństwo → Ciasteczka i dane witryn",
        "pt":    "Configurações → Privacidade e Segurança → Cookies e dados do site",
        "pt-PT": "Definições → Privacidade e Segurança → Cookies e dados de sites",
        "ro":    "Setări → Confidențialitate și securitate → Cookie-uri și date ale site-urilor",
        "ru":    "Настройки → Приватность и защита → Куки-файлы и данные сайтов",
        "sk":    "Nastavenia → Súkromie a bezpečnosť → Súbory cookie a údaje webu",
        "sl":    "Nastavitve → Zasebnost in varnost → Piškotki in podatki spletnih mest",
        "sq":    "Cilësimet → Privatësia & Siguria → Skedarët e skedarëve dhe të dhëna të faqes",
        "sr":    "Подешавања → Приватност и безбедност → Колачићи и подаци сајта",
        "sv":    "Inställningar → Integritet och säkerhet → Cookies och webbplatsdata",
        "tr":    "Ayarlar → Gizlilik ve Güvenlik → Çerezler ve Site Verileri",
        "uk":    "Налаштування → Приватність і захист → Куки та дані сайтів",
    },

    "s6_safari_path": {
        "lv":    "Iestatījumi → Privātums → Pārvaldīt vietnes datus",
        "mk":    "Поставки → Приватност → Управување со податоци на веб-страницата",
        "mt":    "Settings → Privatezza → Immaniġġja d-Dejta tal-Website",
        "nl":    "Instellingen → Privacy → Websitegegevens beheren",
        "no":    "Innstillinger → Personvern → Administrer nettsteddata",
        "pl":    "Ustawienia → Prywatność → Zarządzaj danymi witryn",
        "pt":    "Configurações → Privacidade → Gerenciar dados de sites",
        "pt-PT": "Definições → Privacidade → Gerir dados de sites",
        "ro":    "Setări → Confidențialitate → Gestionați datele site-urilor web",
        "ru":    "Настройки → Конфиденциальность → Управление данными сайтов",
        "sk":    "Nastavenia → Súkromie → Spravovať údaje webových stránok",
        "sl":    "Nastavitve → Zasebnost → Upravljanje podatkov spletnih mest",
        "sq":    "Cilësimet → Privatësia → Menaxho të dhënat e faqes",
        "sr":    "Подешавања → Приватност → Управљање подацима веб-сајтова",
        "sv":    "Inställningar → Integritet → Hantera webbplatsdata",
        "tr":    "Ayarlar → Gizlilik → Web Sitesi Verilerini Yönet",
        "uk":    "Налаштування → Конфіденційність → Керування даними сайтів",
    },

    "s6_edge_path": {
        "lv":    "Iestatījumi → Sīkfaili un vietnes atļaujas",
        "mk":    "Поставки → Колачиња и дозволи за сајтот",
        "mt":    "Settings → Cookies u permessi tas-sit",
        "nl":    "Instellingen → Cookies en sitemachtigingen",
        "no":    "Innstillinger → Informasjonskapsler og nettstedtillatelser",
        "pl":    "Ustawienia → Pliki cookie i uprawnienia witryn",
        "pt":    "Configurações → Cookies e permissões do site",
        "pt-PT": "Definições → Cookies e permissões de sites",
        "ro":    "Setări → Cookie-uri și permisiuni ale site-urilor",
        "ru":    "Настройки → Файлы cookie и разрешения сайтов",
        "sk":    "Nastavenia → Súbory cookie a povolenia webu",
        "sl":    "Nastavitve → Piškotki in dovoljenja spletnih mest",
        "sq":    "Cilësimet → Skedarët e skedarëve dhe lejet e faqes",
        "sr":    "Подешавања → Колачићи и дозволе сајта",
        "sv":    "Inställningar → Cookies och webbplatsbehörigheter",
        "tr":    "Ayarlar → Çerezler ve site izinleri",
        "uk":    "Налаштування → Файли cookie та дозволи сайтів",
    },
}


def seed() -> None:
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        count = 0
        for key, lang_values in TRANSLATIONS.items():
            db_key = f"{NAMESPACE}.{key}"
            for lang, value in lang_values.items():
                session.execute(
                    text(
                        "INSERT INTO translations (lang, key, value) "
                        "VALUES (:lang, :key, :value) "
                        "ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value"
                    ),
                    {"lang": lang, "key": db_key, "value": value},
                )
                count += 1
        session.commit()
        print(f"✅ seed_cookies_browser_paths_p3: {count} rows upserted ({NAMESPACE})")

    engine.dispose()


if __name__ == "__main__":
    seed()
