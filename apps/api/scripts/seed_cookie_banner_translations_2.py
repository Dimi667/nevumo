#!/usr/bin/env python3
"""
Seed cookie banner translations (batch 2).
Namespace: cookie_banner
Keys: 16 | Languages: 12
Run: docker exec nevumo-api python -m apps.api.scripts.seed_cookie_banner_translations_2
"""

import os
import subprocess

from sqlalchemy import create_engine, text

NAMESPACE = "cookie_banner"

TRANSLATIONS = {
    "hu": {
        "cookie_title": "Sütiket használunk",
        "cookie_description": "Sütiket és hasonló technológiákat használunk, hogy javítsuk az Ön élményét, elemezzük a forgalmat és releváns tartalmat jelenítsünk meg. Ön kiválaszthatja, mely kategóriákat engedélyezi.",
        "accept_all": "Összes elfogadása",
        "reject_all": "Összes elutasítása",
        "customize": "Testreszabás",
        "necessary_label": "Szükséges",
        "necessary_description": "A weboldal működéséhez szükséges. Nem tiltható le.",
        "functional_label": "Funkcionális",
        "functional_description": "Megjegyzik beállításait és preferenciáit a látogatások között.",
        "analytics_label": "Analitikai",
        "analytics_description": "Segítenek megérteni, hogyan használják a látogatók a weboldalunkat.",
        "marketing_label": "Marketing",
        "marketing_description": "Releváns hirdetések megjelenítésére szolgálnak más platformokon.",
        "save_preferences": "Beállítások mentése",
        "cookie_settings_link": "Süti beállítások",
        "last_updated": "Utoljára frissítve: {date}"
    },
    "is": {
        "cookie_title": "Við notum vafrakökur",
        "cookie_description": "Við notum vafrakökur og svipaða tækni til að bæta upplifun þína, greina umferð og birta viðeigandi efni. Þú getur valið hvaða flokka þú leyfir.",
        "accept_all": "Samþykkja allt",
        "reject_all": "Hafna öllu",
        "customize": "Sérsníða",
        "necessary_label": "Nauðsynlegar",
        "necessary_description": "Nauðsynlegar fyrir virkni vefsvæðisins. Ekki er hægt að slökkva á þeim.",
        "functional_label": "Virkni",
        "functional_description": "Muna stillingar þínar og kjör milli heimsókna.",
        "analytics_label": "Greining",
        "analytics_description": "Hjálpa okkur að skilja hvernig gestir nota vefsvæðið okkar.",
        "marketing_label": "Markaðssetning",
        "marketing_description": "Notaðar til að sýna þér viðeigandi auglýsingar á öðrum vettvöngum.",
        "save_preferences": "Vista stillingar",
        "cookie_settings_link": "Stillingar vafrakaka",
        "last_updated": "Síðast uppfært: {date}"
    },
    "it": {
        "cookie_title": "Utilizziamo i cookie",
        "cookie_description": "Utilizziamo cookie e tecnologie simili per migliorare la tua esperienza, analizzare il traffico e mostrare contenuti pertinenti. Puoi scegliere quali categorie consentire.",
        "accept_all": "Accetta tutto",
        "reject_all": "Rifiuta tutto",
        "customize": "Personalizza",
        "necessary_label": "Necessari",
        "necessary_description": "Necessari per il funzionamento del sito. Non possono essere disattivati.",
        "functional_label": "Funzionali",
        "functional_description": "Memorizzano le tue preferenze e impostazioni tra una visita e l'altra.",
        "analytics_label": "Analitici",
        "analytics_description": "Ci aiutano a capire come i visitatori utilizzano il nostro sito.",
        "marketing_label": "Marketing",
        "marketing_description": "Utilizzati per mostrarti annunci pertinenti su altre piattaforme.",
        "save_preferences": "Salva preferenze",
        "cookie_settings_link": "Impostazioni cookie",
        "last_updated": "Ultimo aggiornamento: {date}"
    },
    "lb": {
        "cookie_title": "Mir benotzen Cookien",
        "cookie_description": "Mir benotzen Cookien an ähnlech Technologien, fir Är Erfarung ze verbesseren, de Verkéier ze analyséieren a relevant Inhalter ze weisen. Dir kënnt auswielen, wéi eng Kategorien Dir zouloosse wëllt.",
        "accept_all": "All akzeptéieren",
        "reject_all": "All refuséieren",
        "customize": "Personaliséieren",
        "necessary_label": "Néideg",
        "necessary_description": "Néideg fir d'Funktionéiere vun der Websäit. Kënnen net deaktivéiert ginn.",
        "functional_label": "Funktional",
        "functional_description": "Erënnere sech un Är Astellungen a Virléiften iwwer Besichen ewech.",
        "analytics_label": "Analyse",
        "analytics_description": "Hëllefen eis ze verstoen, wéi d'Besicher eis Websäit benotzen.",
        "marketing_label": "Marketing",
        "marketing_description": "Gi benotzt, fir Iech relevant Reklammen op aner Plattformen ze weisen.",
        "save_preferences": "Astellunge späicheren",
        "cookie_settings_link": "Cookien-Astellungen",
        "last_updated": "Lescht Aktualiséierung: {date}"
    },
    "lt": {
        "cookie_title": "Naudojame slapukus",
        "cookie_description": "Naudojame slapukus ir panašias technologijas, kad pagerintume jūsų patirtį, analizuotume srautą ir rodytume aktualų turinį. Galite pasirinkti, kurias kategorijas leisti.",
        "accept_all": "Priimti visus",
        "reject_all": "Atmesti visus",
        "customize": "Tinkinti",
        "necessary_label": "Būtini",
        "necessary_description": "Būtini, kad svetainė veiktų. Jų negalima išjungti.",
        "functional_label": "Funkciniai",
        "functional_description": "Įsimena jūsų nuostatas ir nustatymus tarp apsilankymų.",
        "analytics_label": "Analitiniai",
        "analytics_description": "Padeda mums suprasti, kaip lankytojai naudoja mūsų svetainę.",
        "marketing_label": "Rinkodaros",
        "marketing_description": "Naudojami norint parodyti jums aktualius skelbimus kitose platformose.",
        "save_preferences": "Išsaugoti nuostatas",
        "cookie_settings_link": "Slapukų nustatymai",
        "last_updated": "Paskutinį kartą atnaujinta: {date}"
    },
    "lv": {
        "cookie_title": "Mēs izmantojam sīkdatnes",
        "cookie_description": "Mēs izmantojam sīkdatnes un līdzīgas tehnoloģijas, lai uzlabotu jūsu pieredzi, analizētu datplūsmu un parādītu atbilstošu saturu. Jūs varat izvēlēties, kuras kategorijas atļaut.",
        "accept_all": "Pieņemt visas",
        "reject_all": "Noraidīt visas",
        "customize": "Pielāgot",
        "necessary_label": "Nepieciešamās",
        "necessary_description": "Nepieciešamas, lai vietne darbotos. Nevar atspējot.",
        "functional_label": "Funkcionālās",
        "functional_description": "Atceras jūsu izvēles un iestatījumus starp apmeklējumiem.",
        "analytics_label": "Analītiskās",
        "analytics_description": "Palīdz mums saprast, kā apmeklētāji izmanto mūsu vietni.",
        "marketing_label": "Mārketinga",
        "marketing_description": "Tiek izmantotas, lai rādītu jums atbilstošas reklāmas citās platformās.",
        "save_preferences": "Saglabāt iestatījumus",
        "cookie_settings_link": "Sīkdatņu iestatījumi",
        "last_updated": "Pēdējoreiz atjaunināts: {date}"
    },
    "mk": {
        "cookie_title": "Користиме колачиња",
        "cookie_description": "Користиме колачиња и слични технологии за да го подобриме вашето искуство, да го анализираме сообраќајот и да прикажуваме релевантна содржина. Можете да изберете кои категории да дозволите.",
        "accept_all": "Прифати ги сите",
        "reject_all": "Одбиј ги сите",
        "customize": "Прилагоди",
        "necessary_label": "Неопходни",
        "necessary_description": "Потребни за функционирање на веб-страницата. Не можат да се оневозможат.",
        "functional_label": "Функционални",
        "functional_description": "Ги паметат вашите преференции и поставки помеѓу посетите.",
        "analytics_label": "Аналитички",
        "analytics_description": "Ни помагаат да разбереме како посетителите ја користат нашата веб-страница.",
        "marketing_label": "Маркетинг",
        "marketing_description": "Се користат за прикажување релевантни реклами на други платформи.",
        "save_preferences": "Зачувај преференции",
        "cookie_settings_link": "Поставки за колачиња",
        "last_updated": "Последно ажурирано: {date}"
    },
    "mt": {
        "cookie_title": "Aħna nużaw cookies",
        "cookie_description": "Aħna nużaw cookies u teknoloġiji simili biex intejbu l-esperjenza tiegħek, nanalizzaw it-traffiku u nuru kontenut rilevanti. Tista' tagħżel liema kategoriji tippermetti.",
        "accept_all": "Aċċetta kollox",
        "reject_all": "Irrifjuta kollox",
        "customize": "Personalizza",
        "necessary_label": "Meħtieġa",
        "necessary_description": "Meħtieġa biex il-websajt taħdem. Ma jistgħux jiġu diżattivati.",
        "functional_label": "Funzjonali",
        "functional_description": "Jiftakru l-preferenzi u l-issettjar tiegħek bejn iż-żjarat.",
        "analytics_label": "Analitiċi",
        "analytics_description": "Jgħinuna nifhmu kif il-viżitaturi jużaw il-websajt tagħna.",
        "marketing_label": "Marketing",
        "marketing_description": "Użati biex jurik reklami rilevanti fuq pjattaformi oħra.",
        "save_preferences": "Salva l-preferenzi",
        "cookie_settings_link": "Issettjar tal-cookies",
        "last_updated": "L-aħħar aġġornament: {date}"
    },
    "nl": {
        "cookie_title": "Wij gebruiken cookies",
        "cookie_description": "Wij gebruiken cookies en vergelijkbare technologieën om uw ervaring te verbeteren, verkeer te analyseren en relevante inhoud te tonen. U kunt kiezen welke categorieën u toestaat.",
        "accept_all": "Alles accepteren",
        "reject_all": "Alles weigeren",
        "customize": "Aanpassen",
        "necessary_label": "Noodzakelijk",
        "necessary_description": "Vereist voor het functioneren van de website. Kunnen niet worden uitgeschakeld.",
        "functional_label": "Functioneel",
        "functional_description": "Onthouden uw voorkeuren en instellingen tussen bezoeken.",
        "analytics_label": "Analytisch",
        "analytics_description": "Helpen ons te begrijpen hoe bezoekers onze website gebruiken.",
        "marketing_label": "Marketing",
        "marketing_description": "Worden gebruikt om u relevante advertenties op andere platforms te tonen.",
        "save_preferences": "Voorkeuren opslaan",
        "cookie_settings_link": "Cookie-instellingen",
        "last_updated": "Laatst bijgewerkt: {date}"
    },
    "no": {
        "cookie_title": "Vi bruker informasjonskapsler",
        "cookie_description": "Vi bruker informasjonskapsler og lignende teknologier for å forbedre opplevelsen din, analysere trafikk og vise relevant innhold. Du kan velge hvilke kategorier du vil tillate.",
        "accept_all": "Godta alle",
        "reject_all": "Avvis alle",
        "customize": "Tilpass",
        "necessary_label": "Nødvendige",
        "necessary_description": "Nødvendige for at nettstedet skal fungere. Kan ikke deaktiveres.",
        "functional_label": "Funksjonelle",
        "functional_description": "Husker preferansene og innstillingene dine på tvers av besøk.",
        "analytics_label": "Analyse",
        "analytics_description": "Hjelper oss å forstå hvordan besøkende bruker nettstedet vårt.",
        "marketing_label": "Markedsføring",
        "marketing_description": "Brukes for å vise deg relevante annonser på andre plattformer.",
        "save_preferences": "Lagre preferanser",
        "cookie_settings_link": "Innstillinger for informasjonskapsler",
        "last_updated": "Sist oppdatert: {date}"
    },
    "pl": {
        "cookie_title": "Używamy plików cookie",
        "cookie_description": "Używamy plików cookie i podobnych technologii, aby ulepszać Państwa doświadczenia, analizować ruch oraz wyświetlać odpowiednie treści. Mogą Państwo wybrać, które kategorie zezwolić.",
        "accept_all": "Akceptuj wszystkie",
        "reject_all": "Odrzuć wszystkie",
        "customize": "Dostosuj",
        "necessary_label": "Niezbędne",
        "necessary_description": "Wymagane do działania witryny. Nie można ich wyłączyć.",
        "functional_label": "Funkcjonalne",
        "functional_description": "Zapamiętują Państwa preferencje i ustawienia pomiędzy wizytami.",
        "analytics_label": "Analityczne",
        "analytics_description": "Pomagają nam zrozumieć, w jaki sposób odwiedzający korzystają z naszej witryny.",
        "marketing_label": "Marketingowe",
        "marketing_description": "Służą do wyświetlania Państwu odpowiednich reklam na innych platformach.",
        "save_preferences": "Zapisz preferencje",
        "cookie_settings_link": "Ustawienia plików cookie",
        "last_updated": "Ostatnia aktualizacja: {date}"
    },
    "pt": {
        "cookie_title": "Utilizamos cookies",
        "cookie_description": "Utilizamos cookies e tecnologias similares para melhorar a sua experiência, analisar o tráfego e mostrar conteúdo relevante. Você pode escolher quais categorias permitir.",
        "accept_all": "Aceitar tudo",
        "reject_all": "Rejeitar tudo",
        "customize": "Personalizar",
        "necessary_label": "Necessários",
        "necessary_description": "Necessários para o funcionamento do site. Não podem ser desativados.",
        "functional_label": "Funcionais",
        "functional_description": "Lembram suas preferências e configurações entre visitas.",
        "analytics_label": "Análise",
        "analytics_description": "Nos ajudam a entender como os visitantes usam nosso site.",
        "marketing_label": "Marketing",
        "marketing_description": "Usados para mostrar anúncios relevantes em outras plataformas.",
        "save_preferences": "Salvar preferências",
        "cookie_settings_link": "Configurações de cookies",
        "last_updated": "Última atualização: {date}"
    }
}


def get_database_url() -> str:
    """Get database URL from environment or use default."""
    return os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")


def seed_translations() -> None:
    """Seed all cookie banner translations into the database."""
    engine = create_engine(get_database_url())

    with engine.connect() as conn:
        count = 0
        for lang, translations in TRANSLATIONS.items():
            for key_base, value in translations.items():
                full_key = f"{NAMESPACE}.{key_base}"
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


def flush_redis_cache() -> None:
    """Flush Redis cache for cookie_banner translations."""
    try:
        subprocess.run(
            [
                "docker", "exec", "nevumo-redis", "redis-cli",
                "KEYYS", f"translations:*:{NAMESPACE}"
            ],
            capture_output=True,
            text=True,
            check=False
        )
    except Exception as e:
        print(f"Note: Redis cache flush requires manual command:")
        print('docker exec nevumo-redis redis-cli KEYS "translations:*:cookie_banner" | xargs docker exec -i nevumo-redis redis-cli DEL')


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
    flush_redis_cache()
