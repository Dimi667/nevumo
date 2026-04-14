#!/usr/bin/env python3
"""
Seed PWA translations.
Namespace: pwa
Keys: 6 | Languages: 34
Run: python scripts/seed_pwa_translations.py
"""

import os

from sqlalchemy import create_engine, text

NAMESPACE = "pwa"

TRANSLATIONS = {
    "install_title": {
        "en": "Install Nevumo",
        "bg": "Инсталирай Nevumo",
        "cs": "Nainstaluj Nevumo",
        "da": "Installer Nevumo",
        "de": "Nevumo installieren",
        "el": "Εγκατάσταση Nevumo",
        "es": "Instalar Nevumo",
        "et": "Installi Nevumo",
        "fi": "Asenna Nevumo",
        "fr": "Installer Nevumo",
        "ga": "Suiteáil Nevumo",
        "hr": "Instaliraj Nevumo",
        "hu": "Telepítsd a Nevumót",
        "is": "Settu upp Nevumo",
        "it": "Installa Nevumo",
        "lb": "Nevumo installéieren",
        "lt": "Įdiegti Nevumo",
        "lv": "Instalēt Nevumo",
        "mk": "Инсталирај Nevumo",
        "mt": "Installa Nevumo",
        "nl": "Installeer Nevumo",
        "no": "Installer Nevumo",
        "pl": "Zainstaluj Nevumo",
        "pt": "Instalar o Nevumo",
        "pt-PT": "Instalar o Nevumo",
        "ro": "Instalează Nevumo",
        "ru": "Установить Nevumo",
        "sk": "Nainštaluj Nevumo",
        "sl": "Namesti Nevumo",
        "sq": "Instalo Nevumo",
        "sr": "Инсталирај Nevumo",
        "sv": "Installera Nevumo",
        "tr": "Nevumo'yu Yükle",
        "uk": "Встановити Nevumo",
    },
    "client_subtitle": {
        "en": "Track requests without opening a browser",
        "bg": "Следи заявките без да отваряш браузър",
        "cs": "Sledujte požadavky bez otevření prohlížeče",
        "da": "Følg forespørgsler uden at åbne en browser",
        "de": "Anfragen verfolgen ohne Browser zu öffnen",
        "el": "Παρακολουθείτε αιτήματα χωρίς να ανοίγετε πρόγραμμα περιήγησης",
        "es": "Sigue las solicitudes sin abrir el navegador",
        "et": "Jälgi päringuid ilma brauserit avamata",
        "fi": "Seuraa pyyntöjä avaamatta selainta",
        "fr": "Suivez vos demandes sans ouvrir le navigateur",
        "ga": "Lean iarratais gan brabhsálaí a oscailt",
        "hr": "Prati zahtjeve bez otvaranja preglednika",
        "hu": "Kövesd a kéréseket böngésző megnyitása nélkül",
        "is": "Fylgstu með beiðnum án þess að opna vafra",
        "it": "Monitora le richieste senza aprire il browser",
        "lb": "Ufroe verfollegen ouni de Browser opzemaachen",
        "lt": "Sekite užklausas neatidarydami naršyklės",
        "lv": "Izsekojiet pieprasījumiem, neatverot pārlūku",
        "mk": "Следи ги барањата без да отвораш прелистувач",
        "mt": "Segwi t-talbiet mingħajr ma tiftaħ il-browser",
        "nl": "Volg aanvragen zonder een browser te openen",
        "no": "Følg forespørsler uten å åpne nettleser",
        "pl": "Śledź zapytania bez otwierania przeglądarki",
        "pt": "Acompanhe pedidos sem abrir o navegador",
        "pt-PT": "Acompanhe pedidos sem abrir o navegador",
        "ro": "Urmărește cererile fără a deschide browserul",
        "ru": "Отслеживайте заявки без открытия браузера",
        "sk": "Sledujte požiadavky bez otvárania prehliadača",
        "sl": "Sledite zahtevam brez odpiranja brskalnika",
        "sq": "Gjurmo kërkesat pa hapur shfletuesin",
        "sr": "Прати захтеве без отварања прегледача",
        "sv": "Följ förfrågningar utan att öppna webbläsare",
        "tr": "Tarayıcı açmadan talepleri takip edin",
        "uk": "Відстежуйте запити без відкриття браузера",
    },
    "provider_subtitle": {
        "en": "See new requests instantly",
        "bg": "Виж нови заявки веднага",
        "cs": "Okamžitě sledujte nové požadavky",
        "da": "Se nye forespørgsler med det samme",
        "de": "Neue Anfragen sofort sehen",
        "el": "Δείτε νέα αιτήματα αμέσως",
        "es": "Ve nuevas solicitudes al instante",
        "et": "Vaata uusi päringuid koheselt",
        "fi": "Näe uudet pyynnöt heti",
        "fr": "Voyez les nouvelles demandes instantanément",
        "ga": "Féach ar iarratais nua láithreach",
        "hr": "Odmah vidi nove zahtjeve",
        "hu": "Azonnal lásd az új kéréseket",
        "is": "Sjáðu nýjar beiðnir strax",
        "it": "Vedi subito le nuove richieste",
        "lb": "Nei Ufroe direkt gesinn",
        "lt": "Matykite naujus užklausimus iš karto",
        "lv": "Uzreiz skatiet jaunus pieprasījumus",
        "mk": "Погледни нови барања веднаш",
        "mt": "Ara talbiet ġodda minnufih",
        "nl": "Bekijk nieuwe aanvragen direct",
        "no": "Se nye forespørsler umiddelbart",
        "pl": "Zobacz nowe zapytania natychmiast",
        "pt": "Veja novos pedidos instantaneamente",
        "pt-PT": "Veja novos pedidos instantaneamente",
        "ro": "Vedere cereri noi instantaneu",
        "ru": "Мгновенно видите новые заявки",
        "sk": "Okamžite uvidíte nové požiadavky",
        "sl": "Takoj vidite nove zahteve",
        "sq": "Shih kërkesat e reja menjëherë",
        "sr": "Одмах виде нове захтеве",
        "sv": "Se nya förfrågningar omedelbart",
        "tr": "Yeni talepleri anında görün",
        "uk": "Миттєво бачте нові запити",
    },
    "ios_step1": {
        "en": "Tap Share in the bottom toolbar",
        "bg": "Натисни Share в долната лента на браузъра",
        "cs": "Klepněte na Share ve spodní liště",
        "da": "Tryk på Del i den nederste værktøjslinje",
        "de": "Tippe auf Teilen in der unteren Leiste",
        "el": "Πατήστε Κοινοποίηση στη γραμμή εργαλείων",
        "es": "Toca Compartir en la barra inferior",
        "et": "Puuduta Jaga alumises tööriistaribal",
        "fi": "Napauta Jaa alapalkissa",
        "fr": "Appuyez sur Partager dans la barre du bas",
        "ga": "Tapáil Comhroinnt sa bharra íochtair",
        "hr": "Dodirnite Dijeli u donjoj traci",
        "hu": "Érintsd meg a Megosztás ikont az alsó sávban",
        "is": "Ýttu á Deila í neðri tækjastikunni",
        "it": "Tocca Condividi nella barra in basso",
        "lb": "Dréckt op Share an der ënneschter Leescht",
        "lt": "Bakstelėkite Bendrinti apatinėje įrankių juostoje",
        "lv": "Pieskarieties Kopīgot apakšējā rīkjoslā",
        "mk": "Притисни Share во долната лента",
        "mt": "Agħfas Share fil-bar ta' isfel",
        "nl": "Tik op Delen in de onderste werkbalk",
        "no": "Trykk på Del i den nedre verktøylinjen",
        "pl": "Kliknij Udostępnij w dolnym pasku",
        "pt": "Toque em Compartilhar na barra inferior",
        "pt-PT": "Toque em Partilhar na barra inferior",
        "ro": "Apasă Share în bara de jos",
        "ru": "Нажмите Share в нижней панели",
        "sk": "Klepnite na Zdieľať v spodnej lište",
        "sl": "Tapnite Deli v spodnji vrstici",
        "sq": "Prekni Share në shiritin e poshtëm",
        "sr": "Додирни Дели у доњој траци",
        "sv": "Tryck på Dela i den nedre verktygsfältet",
        "tr": "Alt araç çubuğundaki Paylaş'a dokunun",
        "uk": "Натисніть Share у нижній панелі",
    },
    "ios_step2": {
        "en": "Select \"Add to Home Screen\"",
        "bg": "Избери \"Add to Home Screen\"",
        "cs": "Vyberte \"Přidat na plochu\"",
        "da": "Vælg \"Tilføj til hjemmeskærm\"",
        "de": "Wähle \"Zum Home-Bildschirm\"",
        "el": "Επιλέξτε «Προσθήκη στην Αρχική»",
        "es": "Selecciona \"Añadir a inicio\"",
        "et": "Vali \"Lisa avakuvale\"",
        "fi": "Valitse \"Lisää aloitusnäyttöön\"",
        "fr": "Sélectionnez « Ajouter à l'écran d'accueil »",
        "ga": "Roghnaigh \"Cuir leis an Scáileán Baile\"",
        "hr": "Odaberi \"Dodaj na početni zaslon\"",
        "hu": "Válaszd a \"Kezdőképernyőre\" lehetőséget",
        "is": "Veldu \"Bæta við heimaskjá\"",
        "it": "Seleziona \"Aggiungi alla schermata Home\"",
        "lb": "Wielt \"Zum Haaptbildschierm bäifügen\"",
        "lt": "Pasirinkite \"Pridėti prie pradžios ekrano\"",
        "lv": "Izvēlieties \"Pievienot sākuma ekrānam\"",
        "mk": "Избери \"Додај на почетен екран\"",
        "mt": "Agħżel \"Żid mal-Iskrin Ewlieni\"",
        "nl": "Selecteer \"Voeg toe aan beginscherm\"",
        "no": "Velg \"Legg til på startskjerm\"",
        "pl": "Wybierz \"Dodaj do ekranu głównego\"",
        "pt": "Selecione \"Adicionar à Tela Inicial\"",
        "pt-PT": "Selecione \"Adicionar ao Ecrã Principal\"",
        "ro": "Selectează \"Adaugă la ecranul principal\"",
        "ru": "Выберите «На экран Домой»",
        "sk": "Vyberte \"Pridať na domovskú obrazovku\"",
        "sl": "Izberite \"Dodaj na začetni zaslon\"",
        "sq": "Zgjidhni \"Shto në Ekranin Kryesor\"",
        "sr": "Изабери \"Додај на почетни екран\"",
        "sv": "Välj \"Lägg till på hemskärmen\"",
        "tr": "\"Ana Ekrana Ekle\" seçeneğini seçin",
        "uk": "Виберіть «Додати на головний екран»",
    },
    "dismiss_button": {
        "en": "Got it",
        "bg": "Разбрах",
        "cs": "Rozumím",
        "da": "Forstået",
        "de": "Verstanden",
        "el": "Κατάλαβα",
        "es": "Entendido",
        "et": "Sain aru",
        "fi": "Selvä",
        "fr": "Compris",
        "ga": "Tuigim",
        "hr": "Razumijem",
        "hu": "Értettem",
        "is": "Skil",
        "it": "Capito",
        "lb": "Verstanen",
        "lt": "Supratau",
        "lv": "Sapratu",
        "mk": "Разбрав",
        "mt": "Ftahmt",
        "nl": "Begrepen",
        "no": "Skjønt",
        "pl": "Rozumiem",
        "pt": "Entendi",
        "pt-PT": "Percebi",
        "ro": "Înțeles",
        "ru": "Понятно",
        "sk": "Rozumiem",
        "sl": "Razumem",
        "sq": "Kuptova",
        "sr": "Схватио",
        "sv": "Förstått",
        "tr": "Anladım",
        "uk": "Зрозуміло",
    },
}


def get_database_url() -> str:
    """Get database URL from environment or use default."""
    return os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")


def seed_translations() -> None:
    """Seed all PWA translations into the database."""
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
