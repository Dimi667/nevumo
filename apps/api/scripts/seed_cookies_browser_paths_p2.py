"""
seed_cookies_browser_paths_p2.py — Nevumo | namespace: cookies
Section 6 · Browser settings paths — езици 1–17 (bg → lt)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_cookies_browser_paths_p2
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
        "bg": "Настройки → Поверителност и сигурност → Бисквитки и данни от сайтове",
        "cs": "Nastavení → Soukromí a zabezpečení → Soubory cookie a další data webu",
        "da": "Indstillinger → Privatliv og sikkerhed → Cookies og andre webstedsdata",
        "de": "Einstellungen → Datenschutz und Sicherheit → Cookies und andere Websitedaten",
        "el": "Ρυθμίσεις → Απόρρητο και ασφάλεια → Cookies και άλλα δεδομένα ιστότοπων",
        "en": "Settings → Privacy and security → Cookies and other site data",
        "es": "Configuración → Privacidad y seguridad → Cookies y otros datos de sitios",
        "et": "Seaded → Privaatsus ja turvalisus → Küpsised ja muud saidiandmed",
        "fi": "Asetukset → Tietosuoja ja turvallisuus → Evästeet ja muut sivuston tiedot",
        "fr": "Paramètres → Confidentialité et sécurité → Cookies et autres données des sites",
        "ga": "Socruithe → Príobháideachas agus slándáil → Fianáin agus sonraí suíomh eile",
        "hr": "Postavke → Privatnost i sigurnost → Kolačići i drugi podaci web-mjesta",
        "hu": "Beállítások → Adatvédelem és biztonság → Sütik és egyéb webhelyadatok",
        "is": "Stillingar → Friðhelgi og öryggi → Vefkökur og önnur gögn vefsvæðis",
        "it": "Impostazioni → Privacy e sicurezza → Cookie e altri dati dei siti",
        "lb": "Astellungen → Privatsphär a Sécherheet → Cookien an aner Websitten-Daten",
        "lt": "Nustatymai → Privatumas ir sauga → Slapukai ir kiti svetainių duomenys",
    },

    "s6_firefox_path": {
        "bg": "Настройки → Поверителност и сигурност → Бисквитки и данни от сайтове",
        "cs": "Nastavení → Soukromí a zabezpečení → Soubory cookie a data webu",
        "da": "Indstillinger → Privatliv og sikkerhed → Cookies og webstedsdata",
        "de": "Einstellungen → Datenschutz & Sicherheit → Cookies und Website-Daten",
        "el": "Ρυθμίσεις → Απόρρητο & Ασφάλεια → Cookies και δεδομένα ιστότοπων",
        "en": "Settings → Privacy & Security → Cookies and Site Data",
        "es": "Configuración → Privacidad y Seguridad → Cookies y datos del sitio",
        "et": "Seaded → Privaatsus ja turvalisus → Küpsised ja saidiandmed",
        "fi": "Asetukset → Yksityisyys ja tietoturva → Evästeet ja sivuston tiedot",
        "fr": "Paramètres → Vie privée et sécurité → Cookies et données du site",
        "ga": "Socruithe → Príobháideachas & Slándáil → Fianáin agus Sonraí Suímh",
        "hr": "Postavke → Privatnost i sigurnost → Kolačići i podaci web-mjesta",
        "hu": "Beállítások → Adatvédelem és biztonság → Sütik és webhelyadatok",
        "is": "Stillingar → Friðhelgi og öryggi → Vefkökur og gögn vefsvæðis",
        "it": "Impostazioni → Privacy e sicurezza → Cookie e dati dei siti",
        "lb": "Astellungen → Privatsphär & Sécherheet → Cookien a Websäit-Daten",
        "lt": "Nustatymai → Privatumas ir sauga → Slapukai ir svetainių duomenys",
    },

    "s6_safari_path": {
        "bg": "Настройки → Поверителност → Управление на данни от уебсайтове",
        "cs": "Nastavení → Soukromí → Správa dat webových stránek",
        "da": "Indstillinger → Privatliv → Administrer webstedsdata",
        "de": "Einstellungen → Datenschutz → Website-Daten verwalten",
        "el": "Ρυθμίσεις → Απόρρητο → Διαχείριση δεδομένων ιστότοπων",
        "en": "Settings → Privacy → Manage Website Data",
        "es": "Configuración → Privacidad → Administrar datos de sitios web",
        "et": "Seaded → Privaatsus → Halda veebisaidi andmeid",
        "fi": "Asetukset → Yksityisyys → Hallinnoi verkkosivuston tietoja",
        "fr": "Paramètres → Confidentialité → Gérer les données des sites web",
        "ga": "Socruithe → Príobháideachas → Bainistigh Sonraí Suímh Gréasáin",
        "hr": "Postavke → Privatnost → Upravljanje podacima web-mjesta",
        "hu": "Beállítások → Adatvédelem → Webhelyadatok kezelése",
        "is": "Stillingar → Friðhelgi → Stjórna gögnum vefsvæðis",
        "it": "Impostazioni → Privacy → Gestisci i dati dei siti web",
        "lb": "Astellungen → Privatsphär → Websäit-Daten verwalten",
        "lt": "Nustatymai → Privatumas → Tvarkyti svetainės duomenis",
    },

    "s6_edge_path": {
        "bg": "Настройки → Бисквитки и разрешения за сайтове",
        "cs": "Nastavení → Soubory cookie a oprávnění pro weby",
        "da": "Indstillinger → Cookies og webstedstilladelser",
        "de": "Einstellungen → Cookies und Websiteberechtigungen",
        "el": "Ρυθμίσεις → Cookies και άδειες ιστότοπων",
        "en": "Settings → Cookies and site permissions",
        "es": "Configuración → Cookies y permisos del sitio",
        "et": "Seaded → Küpsised ja saidi õigused",
        "fi": "Asetukset → Evästeet ja sivuston käyttöoikeudet",
        "fr": "Paramètres → Cookies et autorisations des sites",
        "ga": "Socruithe → Fianáin agus ceadanna suímh",
        "hr": "Postavke → Kolačići i dozvole web-mjesta",
        "hu": "Beállítások → Sütik és webhely-engedélyek",
        "is": "Stillingar → Vefkökur og heimildir vefsvæðis",
        "it": "Impostazioni → Cookie e autorizzazioni sito",
        "lb": "Astellungen → Cookien a Websäit-Erlaabnesser",
        "lt": "Nustatymai → Slapukai ir svetainių leidimai",
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
        print(f"✅ seed_cookies_browser_paths_p2: {count} rows upserted ({NAMESPACE})")

    engine.dispose()


if __name__ == "__main__":
    seed()
