#!/usr/bin/env python3
"""
Seed cookie banner translations.
Namespace: cookie_banner
Keys: 16 | Languages: 12
Run: docker exec nevumo-api python -m apps.api.scripts.seed_cookie_banner_translations_1
"""

import os

from sqlalchemy import create_engine, text

NAMESPACE = "cookie_banner"

TRANSLATIONS = {
    "cookie_title": {
        "bg": "Използваме бисквитки",
        "cs": "Používáme soubory cookie",
        "da": "Vi bruger cookies",
        "de": "Wir verwenden Cookies",
        "el": "Χρησιμοποιούμε cookies",
        "en": "We use cookies",
        "es": "Utilizamos cookies",
        "et": "Kasutame küpsiseid",
        "fi": "Käytämme evästeitä",
        "fr": "Nous utilisons des cookies",
        "ga": "Úsáidimid fianáin",
        "hr": "Koristimo kolačiće",
    },
    "cookie_description": {
        "bg": "Използваме бисквитки и подобни технологии, за да подобрим вашето изживяване, да анализираме трафика и да показваме подходящо съдържание. Можете да изберете кои категории да разрешите.",
        "cs": "Používáme soubory cookie a podobné technologie ke zlepšení vašeho prožitku, analýze návštěvnosti a zobrazování relevantního obsahu. Můžete si vybrat, které kategorie povolíte.",
        "da": "Vi bruger cookies og lignende teknologier til at forbedre din oplevelse, analysere trafik og vise relevant indhold. Du kan vælge, hvilke kategorier du vil tillade.",
        "de": "Wir verwenden Cookies und ähnliche Technologien, um Ihr Erlebnis zu verbessern, den Datenverkehr zu analysieren und relevante Inhalte anzuzeigen. Sie können auswählen, welche Kategorien Sie zulassen möchten.",
        "el": "Χρησιμοποιούμε cookies και παρόμοιες τεχνολογίες για να βελτιώσουμε την εμπειρία σας, να αναλύσουμε την επισκεψιμότητα και να εμφανίσουμε σχετικό περιεχόμενο. Μπορείτε να επιλέξετε ποιες κατηγορίες θα επιτρέψετε.",
        "en": "We use cookies and similar technologies to improve your experience, analyse traffic and show relevant content. You can choose which categories to allow.",
        "es": "Utilizamos cookies y tecnologías similares para mejorar su experiencia, analizar el tráfico y mostrar contenido relevante. Puede elegir qué categorías permitir.",
        "et": "Kasutame küpsiseid ja sarnaseid tehnoloogiaid, et parandada teie kasutuskogemust, analüüsida liiklust ja näidata asjakohast sisu. Saate valida, milliseid kategooriaid lubada.",
        "fi": "Käytämme evästeitä ja vastaavia teknologioita parantaaksemme käyttökokemustasi, analysoidaksemme liikennettä ja näyttääksemme sinulle olennaista sisältöä. Voit valita, mitkä kategoriat hyväksyt.",
        "fr": "Nous utilisons des cookies et des technologies similaires pour améliorer votre expérience, analyser le trafic et afficher du contenu pertinent. Vous pouvez choisir les catégories à autoriser.",
        "ga": "Úsáidimid fianáin agus teicneolaíochtaí cosúla chun do thaithí a fheabhsú, trácht a anailísiú agus ábhar ábhartha a thaispeáint. Is féidir leat na catagóirí is mian leat a cheadú a roghnú.",
        "hr": "Koristimo kolačiće i slične tehnologije kako bismo poboljšali vaše iskustvo, analizirali promet i prikazali relevantan sadržaj. Možete odabrati koje kategorije želite dopustiti.",
    },
    "accept_all": {
        "bg": "Приеми всички",
        "cs": "Přijmout vše",
        "da": "Accepter alle",
        "de": "Alle akzeptieren",
        "el": "Αποδοχή όλων",
        "en": "Accept All",
        "es": "Aceptar todo",
        "et": "Nõustu kõigiga",
        "fi": "Hyväksy kaikki",
        "fr": "Tout accepter",
        "ga": "Glac le gach ceann",
        "hr": "Prihvati sve",
    },
    "reject_all": {
        "bg": "Отхвърли всички",
        "cs": "Odmítnout vše",
        "da": "Afvis alle",
        "de": "Alle ablehnen",
        "el": "Απόρριψη όλων",
        "en": "Reject All",
        "es": "Rechazar todo",
        "et": "Keeldu kõigist",
        "fi": "Hylkää kaikki",
        "fr": "Tout refuser",
        "ga": "Diúltaigh do gach ceann",
        "hr": "Odbij sve",
    },
    "customize": {
        "bg": "Персонализиране",
        "cs": "Přizpůsobit",
        "da": "Tilpas",
        "de": "Anpassen",
        "el": "Προσαρμογή",
        "en": "Customize",
        "es": "Personalizar",
        "et": "Kohanda",
        "fi": "Mukauta",
        "fr": "Personnaliser",
        "ga": "Saincheap",
        "hr": "Prilagodi",
    },
    "necessary_label": {
        "bg": "Необходими",
        "cs": "Nezbytné",
        "da": "Nødvendige",
        "de": "Notwendig",
        "el": "Απαραίτητα",
        "en": "Necessary",
        "es": "Necesarias",
        "et": "Vajalikud",
        "fi": "Välttämättömät",
        "fr": "Nécessaires",
        "ga": "Riachtanach",
        "hr": "Nužni",
    },
    "necessary_description": {
        "bg": "Необходими са за функционирането на уебсайта. Не могат да бъдат изключени.",
        "cs": "Nutné pro fungování webu. Nelze je zakázat.",
        "da": "Påkrævet for at webstedet kan fungere. Kan ikke deaktiveres.",
        "de": "Erforderlich für das Funktionieren der Website. Kann nicht deaktiviert werden.",
        "el": "Απαιτούνται για τη λειτουργία του ιστότοπου. Δεν μπορούν να απενεργοποιηθούν.",
        "en": "Required for the website to function. Cannot be disabled.",
        "es": "Necesarias para el funcionamiento del sitio web. No se pueden desactivar.",
        "et": "Vajalikud veebisaidi toimimiseks. Neid ei saa keelata.",
        "fi": "Vaaditaan sivuston toimintaan. Ei voida poistaa käytöstä.",
        "fr": "Requis pour le fonctionnement du site. Ne peuvent pas être désactivés.",
        "ga": "Riachtanach chun an suíomh gréasáin a fheidhmiú. Ní féidir iad a dhíchumasú.",
        "hr": "Potrebni su za rad web-mjesta. Ne mogu se onemogućiti.",
    },
    "functional_label": {
        "bg": "Функционални",
        "cs": "Funkční",
        "da": "Funktionelle",
        "de": "Funktional",
        "el": "Λειτουργικά",
        "en": "Functional",
        "es": "Funcionales",
        "et": "Funktsionaalsed",
        "fi": "Toiminnalliset",
        "fr": "Fonctionnels",
        "ga": "Feidhmiúil",
        "hr": "Funkcionalni",
    },
    "functional_description": {
        "bg": "Запомнят вашите предпочитания и настройки между посещенията.",
        "cs": "Zapamatují si vaše předvolby a nastavení mezi návštěvami.",
        "da": "Husker dine præferencer og indstillinger på tværs af besøg.",
        "de": "Speichert Ihre Präferenzen und Einstellungen über Besuche hinweg.",
        "el": "Θυμούνται τις προτιμήσεις και τις ρυθμίσεις σας σε όλες τις επισκέψεις.",
        "en": "Remember your preferences and settings across visits.",
        "es": "Recuerdan sus preferencias y ajustes entre visitas.",
        "et": "Jätavad meelde teie eelistused ja seaded eri külastuste vahel.",
        "fi": "Muistavat asetuksesi ja mieltymyksesi käyntien välillä.",
        "fr": "Mémorisent vos préférences et paramètres entre les visites.",
        "ga": "Coinníonn cuimhne ar do shainroghanna agus ar do shocruithe idir cuairteanna.",
        "hr": "Pamte vaše postavke i preferencije između posjeta.",
    },
    "analytics_label": {
        "bg": "Аналитични",
        "cs": "Analytické",
        "da": "Analyse",
        "de": "Analyse",
        "el": "Αναλυτικά",
        "en": "Analytics",
        "es": "Analíticas",
        "et": "Analüütika",
        "fi": "Analytiikka",
        "fr": "Analytiques",
        "ga": "Anailísíocht",
        "hr": "Analitički",
    },
    "analytics_description": {
        "bg": "Помагат ни да разберем как посетителите използват нашия уебсайт.",
        "cs": "Pomáhají nám pochopit, jak návštěvníci používají naše webové stránky.",
        "da": "Hjælper os med at forstå, hvordan besøgende bruger vores websted.",
        "de": "Helfen uns zu verstehen, wie Besucher unsere Website nutzen.",
        "el": "Μας βοηθούν να κατανοήσουμε πώς οι επισκέπτες χρησιμοποιούν τον ιστότοπό μας.",
        "en": "Help us understand how visitors use our website.",
        "es": "Nos ayudan a entender cómo los visitantes utilizan nuestro sitio web.",
        "et": "Aitavad meil mõista, kuidas külastajad meie veebisaiti kasutavad.",
        "fi": "Auttavat meitä ymmärtämään, miten kävijät käyttävät sivustoamme.",
        "fr": "Nous aident à comprendre comment les visiteurs utilisent notre site.",
        "ga": "Cabhraíonn linn a thuiscint conas a úsáideann cuairteoirí ár suíomh gréasáin.",
        "hr": "Pomažu nam razumjeti kako posjetitelji koriste naše web-mjesto.",
    },
    "marketing_label": {
        "bg": "Маркетингови",
        "cs": "Marketingové",
        "da": "Marketing",
        "de": "Marketing",
        "el": "Μάρκετινγκ",
        "en": "Marketing",
        "es": "Marketing",
        "et": "Turundus",
        "fi": "Markkinointi",
        "fr": "Marketing",
        "ga": "Margaíocht",
        "hr": "Marketinški",
    },
    "marketing_description": {
        "bg": "Използват се за показване на подходящи реклами на други платформи.",
        "cs": "Slouží k zobrazování relevantních reklam na jiných platformách.",
        "da": "Bruges til at vise dig relevante annoncer på andre platforme.",
        "de": "Werden verwendet, um Ihnen relevante Werbung auf anderen Plattformen anzuzeigen.",
        "el": "Χρησιμοποιούνται για να σας εμφανίζουν σχετικές διαφημίσεις σε άλλες πλατφόρμες.",
        "en": "Used to show you relevant advertisements on other platforms.",
        "es": "Se utilizan para mostrarle anuncios relevantes en otras plataformas.",
        "et": "Kasutatakse asjakohaste reklaamide kuvamiseks teistel platvormidel.",
        "fi": "Käytetään näyttämään sinulle olennaisia mainoksia muilla alustoilla.",
        "fr": "Utilisés pour vous afficher des publicités pertinentes sur d'autres plateformes.",
        "ga": "Úsáidtear iad chun fógraí ábhartha a thaispeáint duit ar ardáin eile.",
        "hr": "Koriste se za prikazivanje relevantnih oglasa na drugim platformama.",
    },
    "save_preferences": {
        "bg": "Запази предпочитанията",
        "cs": "Uložit předvolby",
        "da": "Gem præferencer",
        "de": "Einstellungen speichern",
        "el": "Αποθήκευση προτιμήσεων",
        "en": "Save Preferences",
        "es": "Guardar preferencias",
        "et": "Salvesta eelistused",
        "fi": "Tallenna asetukset",
        "fr": "Enregistrer les préférences",
        "ga": "Sábháil sainroghanna",
        "hr": "Spremi postavke",
    },
    "cookie_settings_link": {
        "bg": "Настройки на бисквитките",
        "cs": "Nastavení cookies",
        "da": "Cookieindstillinger",
        "de": "Cookie-Einstellungen",
        "el": "Ρυθμίσεις cookies",
        "en": "Cookie Settings",
        "es": "Configuración de cookies",
        "et": "Küpsiste seaded",
        "fi": "Evästeasetukset",
        "fr": "Paramètres des cookies",
        "ga": "Socruithe fianán",
        "hr": "Postavke kolačića",
    },
    "last_updated": {
        "bg": "Последна актуализация: {date}",
        "cs": "Naposledy aktualizováno: {date}",
        "da": "Sidst opdateret: {date}",
        "de": "Zuletzt aktualisiert: {date}",
        "el": "Τελευταία ενημέρωση: {date}",
        "en": "Last updated: {date}",
        "es": "Última actualización: {date}",
        "et": "Viimati uuendatud: {date}",
        "fi": "Viimeksi päivitetty: {date}",
        "fr": "Dernière mise à jour : {date}",
        "ga": "Nuashonraithe go deireanach: {date}",
        "hr": "Posljednje ažuriranje: {date}",
    },
    "cookie_privacy_link": {
        "en": "Privacy Policy",
        "bg": "Политика за поверителност",
        "pl": "Polityka prywatności",
        "cs": "Zásady ochrany osobních údajů",
        "da": "Privatlivspolitik",
        "de": "Datenschutzerklärung",
        "el": "Πολιτική Απορρήτου",
        "es": "Política de privacidad",
        "et": "Privaatsuspoliitika",
        "fi": "Tietosuojakäytäntö",
        "fr": "Politique de confidentialité",
        "ga": "Polasaí Príobháideachais",
        "hr": "Politika privatnosti",
        "hu": "Adatvédelmi irányelvek",
        "is": "Persónuverndarstefna",
        "it": "Informativa sulla privacy",
        "lb": "Datenschutzerklärung",
        "lt": "Privatumo politika",
        "lv": "Privātuma politika",
        "mk": "Политика за приватност",
        "mt": "Politika tal-Privatezza",
        "nl": "Privacybeleid",
        "no": "Personvernpolicy",
        "pt": "Política de privacidade",
        "pt-PT": "Política de privacidade",
        "ro": "Politica de confidențialitate",
        "ru": "Политика конфиденциальности",
        "sk": "Zásady ochrany osobných údajov",
        "sl": "Politika zasebnosti",
        "sq": "Politika e privatësisë",
        "sr": "Политика приватности",
        "sv": "Integritetspolicy",
        "tr": "Gizlilik Politikası",
        "uk": "Політика конфіденційності",
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
