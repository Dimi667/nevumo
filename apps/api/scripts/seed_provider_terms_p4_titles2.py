"""
seed_provider_terms_p4_titles2.py  —  Nevumo | namespace: provider_terms
Keys: art5_title, art6_title, art7_title, art8_title  (4 keys x 34 langs = 136 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p4_titles2
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nevumo:nevumo@postgres:5432/nevumo_leads",
)

NAMESPACE = "provider_terms"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "art5_title": {
        "bg":    "5. Класиране и видимост",
        "cs":    "5. Poradi a viditelnost",
        "da":    "5. Rangering og synlighed",
        "de":    "5. Ranking und Sichtbarkeit",
        "el":    "5. Katalaxisi kai Oratikata",
        "en":    "5. Ranking and Visibility",
        "es":    "5. Clasificacion y visibilidad",
        "et":    "5. Edetabel ja nhtavus",
        "fi":    "5. Sijoitus ja nakyvyys",
        "fr":    "5. Classement et visibilite",
        "ga":    "5. Rangú agus Infheictheacht",
        "hr":    "5. Rangiranje i vidljivost",
        "hu":    "5. Rangsor es lathatosag",
        "is":    "5. Rod og sýnileiki",
        "it":    "5. Posizionamento e visibilita",
        "lb":    "5. Ranking a Visibilitéit",
        "lt":    "5. Reitingas ir matomumas",
        "lv":    "5. Rangs un redzamiba",
        "mk":    "5. Rangiranje i vidlivost",
        "mt":    "5. Klassifikazzjoni u Viżibilita",
        "nl":    "5. Rangschikking en zichtbaarheid",
        "no":    "5. Rangering og synlighet",
        "pl":    "5. Ranking i widoczność",
        "pt":    "5. Classificacao e visibilidade",
        "pt-PT": "5. Classificacao e visibilidade",
        "ro":    "5. Clasament si vizibilitate",
        "ru":    "5. Reyting i vidimos",
        "sk":    "5. Poradie a viditelnost",
        "sl":    "5. Uvrstitev in vidnost",
        "sq":    "5. Renditja dhe dukshmeria",
        "sr":    "5. Rangiranje i vidljivost",
        "sv":    "5. Rankning och synlighet",
        "tr":    "5. Siralama ve Gorunurluk",
        "uk":    "5. Reytynh i vydymist",
    },
    "art6_title": {
        "bg":    "6. Комисионна, плащания и ценоразпис",
        "cs":    "6. Provize, platby a cenik",
        "da":    "6. Provision, betalinger og prisliste",
        "de":    "6. Provision, Zahlungen und Preisliste",
        "el":    "6. Provmitheia, Pliromes kai Timokatalogos",
        "en":    "6. Commission, Payments, and Pricing",
        "es":    "6. Comision, pagos y precios",
        "et":    "6. Vahendustasu, maksed ja hinnakiri",
        "fi":    "6. Provisio, maksut ja hinnasto",
        "fr":    "6. Commission, paiements et tarification",
        "ga":    "6. Coimisiun, Iocaiochtai agus Praghsail",
        "hr":    "6. Provizija, placanja i cjenik",
        "hu":    "6. Jutalek, fizetesek es araink",
        "is":    "6. Þoknun, greidslur og verðskra",
        "it":    "6. Commissione, pagamenti e prezzi",
        "lb":    "6. Kommissioun, Bezuelungen a Präislëschte",
        "lt":    "6. Komisiniai, mokejimаi ir kainynas",
        "lv":    "6. Komisija, maksajumi un cenradis",
        "mk":    "6. Provizija, placanja i cenovnik",
        "mt":    "6. Kummissjoni, Pagamenti u Prezz",
        "nl":    "6. Commissie, betalingen en prijzen",
        "no":    "6. Provisjon, betalinger og prisliste",
        "pl":    "6. Prowizje, płatności i cennik",
        "pt":    "6. Comissao, pagamentos e precos",
        "pt-PT": "6. Comissao, pagamentos e precos",
        "ro":    "6. Comision, plati si preturi",
        "ru":    "6. Komissiya, platezhi i tseny",
        "sk":    "6. Proviziya, platby a cennik",
        "sl":    "6. Provizija, placila in cenik",
        "sq":    "6. Komisioni, pagesat dhe cmimi",
        "sr":    "6. Provizija, placanja i cenovnik",
        "sv":    "6. Provision, betalningar och prislista",
        "tr":    "6. Komisyon, Odemeler ve Fiyatlandirma",
        "uk":    "6. Komisiia, platezhi ta tsiny",
    },
    "art7_title": {
        "bg":    "7. Задължения на Доставчика",
        "cs":    "7. Povinnosti poskytovatele",
        "da":    "7. Udbyderens forpligtelser",
        "de":    "7. Pflichten des Dienstleisters",
        "el":    "7. Ypokhreoseis tou Parohou",
        "en":    "7. Provider Obligations",
        "es":    "7. Obligaciones del proveedor",
        "et":    "7. Teenusepakkuja kohustused",
        "fi":    "7. Palveluntarjoajan velvoitteet",
        "fr":    "7. Obligations du prestataire",
        "ga":    "7. Oibleagaidi an tSolathraio",
        "hr":    "7. Obveze pruzatelja usluga",
        "hu":    "7. A szolgaltato kotelezettsegei",
        "is":    "7. Skyldur veituadilans",
        "it":    "7. Obblighi del fornitore",
        "lb":    "7. Obligatiounen vum Presser",
        "lt":    "7. Paslaugu teikeojo pareigos",
        "lv":    "7. Pakalpojumu sniedzeja pienakumi",
        "mk":    "7. Obvrski na davacot na uslugi",
        "mt":    "7. Obbligi tal-Fornitur",
        "nl":    "7. Verplichtingen van de dienstverlener",
        "no":    "7. Leverandorens forpliktelser",
        "pl":    "7. Obowiązki Dostawcy",
        "pt":    "7. Obrigacoes do prestador",
        "pt-PT": "7. Obrigacoes do prestador",
        "ro":    "7. Obligatiile furnizorului",
        "ru":    "7. Obyazannosti postavshchika",
        "sk":    "7. Povinnosti poskytovatel'a",
        "sl":    "7. Obveznosti ponudnika",
        "sq":    "7. Detyrimet e ofruesit",
        "sr":    "7. Obaveze pruzaoca usluga",
        "sv":    "7. Leverantorens skyldigheter",
        "tr":    "7. Saglayici Yukumlulükleri",
        "uk":    "7. Obovyazky postachalnika",
    },
    "art8_title": {
        "bg":    "8. Спиране, ограничаване и прекратяване на акаунт",
        "cs":    "8. Pozastaveni, omezeni a zruseni uctu",
        "da":    "8. Suspension, begraensning og afslutning af konto",
        "de":    "8. Kontosperrung, Einschraenkung und Kuendigung",
        "el":    "8. Anastoli, Periorismós kai Termatismós Logariasmou",
        "en":    "8. Account Suspension, Restriction, and Termination",
        "es":    "8. Suspension, restriccion y cancelacion de cuenta",
        "et":    "8. Konto peatamine, piiramine ja sulgemine",
        "fi":    "8. Tilin jaahdyttaminen, rajoittaminen ja lopettaminen",
        "fr":    "8. Suspension, restriction et resiliation du compte",
        "ga":    "8. Fionraiocht, Srian agus Foirceannadh Cuntais",
        "hr":    "8. Suspenzija, ogranicenje i prekid racuna",
        "hu":    "8. Fiokfelfüggesztes, -korlatozas es -megszüntetes",
        "is":    "8. Fresting, takmarkanir og lok reiknings",
        "it":    "8. Sospensione, restrizione e chiusura dell'account",
        "lb":    "8. Suspendéierung, Aschraenkung a Kuendigung vum Kont",
        "lt":    "8. Paskyros sustabdymas, apribojimas ir nutraukimas",
        "lv":    "8. Konta aptureshana, ierobezojumi un slēgshana",
        "mk":    "8. Suspenzija, ogranichuvanje i prekin na nalog",
        "mt":    "8. Sospensjoni, Restrizzjoni u Terminazzjoni tal-Kont",
        "nl":    "8. Schorsing, beperking en beeindiging van account",
        "no":    "8. Suspensjon, begrensning og avslutning av konto",
        "pl":    "8. Zawieszenie, ograniczenie i zamknięcie konta",
        "pt":    "8. Suspensao, restricao e encerramento de conta",
        "pt-PT": "8. Suspensao, restricao e encerramento de conta",
        "ro":    "8. Suspendarea, restrictionarea si incetarea contului",
        "ru":    "8. Blokirovka, ogranichenie i udalenie uchetnoy zapisi",
        "sk":    "8. Pozastavenie, obmedzenie a zrusenie uctu",
        "sl":    "8. Zaustavitev, omejitev in prenehanje racuna",
        "sq":    "8. Pezullimi, kufizimi dhe mbyllja e llogarise",
        "sr":    "8. Suspenzija, ogranicenje i ukidanje naloga",
        "sv":    "8. Kontoavstangning, begransning och avslutning",
        "tr":    "8. Hesap Askiya Alma, Kisitlama ve Kapatma",
        "uk":    "8. Blokyvannya, obmezhennya ta skasovannya obliokovogo zapysu",
    },
}


def seed() -> None:
    engine = create_engine(DATABASE_URL, echo=False)
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
        print(
            f"✅ seed_provider_terms_p4_titles2: {count} rows upserted "
            f"({NAMESPACE}: art5_title, art6_title, art7_title, art8_title x 34 langs)"
        )

    engine.dispose()


if __name__ == "__main__":
    seed()
