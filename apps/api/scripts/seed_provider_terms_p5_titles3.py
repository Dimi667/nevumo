"""
seed_provider_terms_p5_titles3.py  —  Nevumo | namespace: provider_terms
Keys: art9_title, art10_title, art11_title, art12_title  (4 keys x 34 langs = 136 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p5_titles3
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
    "art9_title": {
        "bg":    "9. Верификация и декларация за търговец",
        "cs":    "9. KYC a prohlaseni o podnikateli",
        "da":    "9. KYC og erhvervsdrivende-erklaering",
        "de":    "9. KYC und Händlererklärung",
        "el":    "9. KYC kai Dilossi Emporos",
        "en":    "9. KYC and Trader Declaration",
        "es":    "9. KYC y declaracion de comerciante",
        "et":    "9. KYC ja kaupmehe deklaratsioon",
        "fi":    "9. KYC ja kauppiasilmoitus",
        "fr":    "9. KYC et declaration de commercant",
        "ga":    "9. KYC agus Dearbhu Tradeara",
        "hr":    "9. KYC i izjava trgovca",
        "hu":    "9. KYC es kereskedelmi nyilatkozat",
        "is":    "9. KYC og kaupmannsyfirlysing",
        "it":    "9. KYC e dichiarazione di operatore commerciale",
        "lb":    "9. KYC an Händlererklärung",
        "lt":    "9. KYC ir prekeivio deklaracija",
        "lv":    "9. KYC un tirgotaja deklaracija",
        "mk":    "9. KYC i deklaracija na trgovets",
        "mt":    "9. KYC u Dikjarazzjoni ta Negozjant",
        "nl":    "9. KYC en handelsverklaring",
        "no":    "9. KYC og naeringsdrivendeerklaring",
        "pl":    "9. KYC i oswiadczenie przedsiebiorcy",
        "pt":    "9. KYC e declaracao de comerciante",
        "pt-PT": "9. KYC e declaracao de comerciante",
        "ro":    "9. KYC si declaratia de comerciant",
        "ru":    "9. KYC i deklaratsiya predprinimatelya",
        "sk":    "9. KYC a vyhlasenie obchodnika",
        "sl":    "9. KYC in izjava trgovca",
        "sq":    "9. KYC dhe deklarata e tregtarit",
        "sr":    "9. KYC i izjava trgovca",
        "sv":    "9. KYC och náringsidkardeklaration",
        "tr":    "9. KYC ve Tacir Beyani",
        "uk":    "9. KYC ta deklaratsiya pidpryyemtsya",
    },
    "art10_title": {
        "bg":    "10. Изменения на Условията за Доставчици",
        "cs":    "10. Zmeny podminek poskytovatele",
        "da":    "10. Aendringer af udbydervilkår",
        "de":    "10. Änderungen der Dienstleisterbedingungen",
        "el":    "10. Tropopoiiseis ton Oron Parohou",
        "en":    "10. Amendments to These Terms",
        "es":    "10. Modificaciones de los presentes terminos",
        "et":    "10. Teenusepakkuja tingimuste muutmine",
        "fi":    "10. Muutokset naihin ehtoihin",
        "fr":    "10. Modifications des presentes conditions",
        "ga":    "10. Leasuithe ar na Tearmai seo",
        "hr":    "10. Izmjene uvjeta pruzatelja",
        "hu":    "10. A jelen feltetelek modositasa",
        "is":    "10. Breytingar a thessum skilmalum",
        "it":    "10. Modifiche alle presenti condizioni",
        "lb":    "10. Ännerungen vun desen Bedingungen",
        "lt":    "10. Siu salygu pakeitimai",
        "lv":    "10. So noteikumu grozijumi",
        "mk":    "10. Izmeni na ovie Uslovi",
        "mt":    "10. Emendi ghal dawn it-Termini",
        "nl":    "10. Wijzigingen van deze voorwaarden",
        "no":    "10. Endringer i disse vilkarene",
        "pl":    "10. Zmiany Regulaminu Dostawcow",
        "pt":    "10. Alteracoes a estes termos",
        "pt-PT": "10. Alteracoes a estes termos",
        "ro":    "10. Modificari ale prezentilor termeni",
        "ru":    "10. Izmeneniya nastoyashchikh Usloviy",
        "sk":    "10. Zmeny tychto podmienok",
        "sl":    "10. Spremembe teh pogojev",
        "sq":    "10. Ndryshime ne keto Kushte",
        "sr":    "10. Izmene ovih Uslova",
        "sv":    "10. Andringar av dessa villkor",
        "tr":    "10. Bu Kosullarda Degisiklikler",
        "uk":    "10. Zminy do tsykh Umov",
    },
    "art11_title": {
        "bg":    "11. Достъп до данните на Доставчика",
        "cs":    "11. Pristup k datum poskytovatele",
        "da":    "11. Adgang til udbyderens data",
        "de":    "11. Zugang zu Ihren Daten",
        "el":    "11. Prosbasimokata sta Dedomena tou Parohou",
        "en":    "11. Access to Your Data",
        "es":    "11. Acceso a sus datos",
        "et":    "11. Juurdepäas oma andmetele",
        "fi":    "11. Paasy omiin tietoihin",
        "fr":    "11. Acces a vos donnees",
        "ga":    "11. Rochtain ar Do Shonrai",
        "hr":    "11. Pristup vasim podacima",
        "hu":    "11. Hozzaferes az On adataihoz",
        "is":    "11. Adgangur ad gognum thinum",
        "it":    "11. Accesso ai tuoi dati",
        "lb":    "11. Zougang zu Ären Daten",
        "lt":    "11. Prieiga prie jusu duomenu",
        "lv":    "11. Piekluve saviem datiem",
        "mk":    "11. Pristap do vashite podatoci",
        "mt":    "11. Access ghad-Data Tieghek",
        "nl":    "11. Toegang tot uw gegevens",
        "no":    "11. Tilgang til dine data",
        "pl":    "11. Dostep do danych Dostawcy",
        "pt":    "11. Acesso aos seus dados",
        "pt-PT": "11. Acesso aos seus dados",
        "ro":    "11. Acces la datele dvs.",
        "ru":    "11. Dostup k vashim dannym",
        "sk":    "11. Pristup k vasim udajom",
        "sl":    "11. Dostop do vasih podatkov",
        "sq":    "11. Qasja ne te dhenat tuaja",
        "sr":    "11. Pristup vasim podacima",
        "sv":    "11. Tillgang till dina uppgifter",
        "tr":    "11. Verilerinize Erisim",
        "uk":    "11. Dostup do vashykh danykh",
    },
    "art12_title": {
        "bg":    "12. Вътрешна система за разглеждане на жалби",
        "cs":    "12. Interni system pro vyrizovani stiznosti",
        "da":    "12. Internt klagehåndteringssystem",
        "de":    "12. Internes Beschwerdemanagementsystem",
        "el":    "12. Esoterika Systima Diacheirisis Parapponton",
        "en":    "12. Internal Complaint-Handling System",
        "es":    "12. Sistema interno de gestion de reclamaciones",
        "et":    "12. Sisemine kaebuste lahendamise susteem",
        "fi":    "12. Sisainen valitusten kasittelyjarjestelma",
        "fr":    "12. Systeme interne de traitement des plaintes",
        "ga":    "12. Corais Inmheanach um Phrosail Gearran",
        "hr":    "12. Interni sustav rjesavanja prituzbi",
        "hu":    "12. Belso panaszkezelo rendszer",
        "is":    "12. Innra kvortunarkerfid",
        "it":    "12. Sistema interno di gestione dei reclami",
        "lb":    "12. Internt Beschwerdemanagementsystem",
        "lt":    "12. Vidaus skundu nagrinejimo sistema",
        "lv":    "12. Iekšeja sudzibu izskatishanas sistema",
        "mk":    "12. Vnatreshen sistem za razgleduvanje na prigovori",
        "mt":    "12. Sistema Interna ta Trattament tal-Ilmenti",
        "nl":    "12. Intern klachtenbehandelingssysteem",
        "no":    "12. Internt klagebehandlingssystem",
        "pl":    "12. Wewnetrzny system rozpatrywania skarg",
        "pt":    "12. Sistema interno de tratamento de reclamacoes",
        "pt-PT": "12. Sistema interno de tratamento de reclamacoes",
        "ro":    "12. Sistemul intern de solutionare a reclamatiilor",
        "ru":    "12. Vnutrennyaya sistema raboty s zhalobami",
        "sk":    "12. Interni system vybavovania staznosti",
        "sl":    "12. Notranji sistem obravnavanja pritozb",
        "sq":    "12. Sistemi i brendshem i trajtimit te ankesave",
        "sr":    "12. Interni sistem za razmatranje prigovora",
        "sv":    "12. Internt klagomalshanteringssystem",
        "tr":    "12. Dahili Sikayet Yonetim Sistemi",
        "uk":    "12. Vnutrishnya systema rozglyadu skarh",
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
            f"✅ seed_provider_terms_p5_titles3: {count} rows upserted "
            f"({NAMESPACE}: art9_title, art10_title, art11_title, art12_title x 34 langs)"
        )

    engine.dispose()


if __name__ == "__main__":
    seed()
