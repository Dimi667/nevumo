"""
seed_provider_terms_p6_titles4.py  —  Nevumo | namespace: provider_terms
Keys: art13_title, art14_title, art15_title, art16_title  (4 keys x 34 langs = 136 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p6_titles4
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
    "art13_title": {
        "bg":    "13. Медиация",
        "cs":    "13. Mediace",
        "da":    "13. Maegling",
        "de":    "13. Mediation",
        "el":    "13. Mesologia",
        "en":    "13. Mediation",
        "es":    "13. Mediacion",
        "et":    "13. Vahendus",
        "fi":    "13. Sovittelu",
        "fr":    "13. Mediation",
        "ga":    "13. Idirghabhal",
        "hr":    "13. Medijacija",
        "hu":    "13. Mediacio",
        "is":    "13. Milligenga",
        "it":    "13. Mediazione",
        "lb":    "13. Mediatioun",
        "lt":    "13. Mediacija",
        "lv":    "13. Mediacija",
        "mk":    "13. Medijacija",
        "mt":    "13. Medjazzjoni",
        "nl":    "13. Bemiddeling",
        "no":    "13. Mekling",
        "pl":    "13. Mediacja",
        "pt":    "13. Mediacao",
        "pt-PT": "13. Mediacao",
        "ro":    "13. Mediere",
        "ru":    "13. Mediatsiya",
        "sk":    "13. Mediacia",
        "sl":    "13. Mediacija",
        "sq":    "13. Ndermjetesim",
        "sr":    "13. Medijacija",
        "sv":    "13. Medling",
        "tr":    "13. Arabuluculuk",
        "uk":    "13. Mediatsiya",
    },
    "art14_title": {
        "bg":    "14. Ограничаване на отговорността",
        "cs":    "14. Omezeni odpovednosti",
        "da":    "14. Ansvarsbegransning",
        "de":    "14. Haftungsbeschränkung",
        "el":    "14. Periorismós Efthynis",
        "en":    "14. Limitation of Liability",
        "es":    "14. Limitacion de responsabilidad",
        "et":    "14. Vastutuse piiramine",
        "fi":    "14. Vastuun rajoittaminen",
        "fr":    "14. Limitation de responsabilite",
        "ga":    "14. Teorainn ar Dhliteanas",
        "hr":    "14. Ogranicenje odgovornosti",
        "hu":    "14. Felelosseg korlatozasa",
        "is":    "14. Takmarkanir a abyrgd",
        "it":    "14. Limitazione di responsabilita",
        "lb":    "14. Haftungsbeschränkung",
        "lt":    "14. Atsakomybes apribojimas",
        "lv":    "14. Atbildibas ierobezojums",
        "mk":    "14. Ogranichuvanje na odgovornost",
        "mt":    "14. Limitazzjoni tar-Responsabbilita",
        "nl":    "14. Beperking van aansprakelijkheid",
        "no":    "14. Ansvarsbegrensning",
        "pl":    "14. Ograniczenie odpowiedzialnosci",
        "pt":    "14. Limitacao de responsabilidade",
        "pt-PT": "14. Limitacao de responsabilidade",
        "ro":    "14. Limitarea raspunderii",
        "ru":    "14. Ogranichenie otvetstvennosti",
        "sk":    "14. Obmedzenie zodpovednosti",
        "sl":    "14. Omejitev odgovornosti",
        "sq":    "14. Kufizimi i pergjegjsise",
        "sr":    "14. Ogranicenje odgovornosti",
        "sv":    "14. Ansvarsbegransning",
        "tr":    "14. Sorumluluk Sinirlamasi",
        "uk":    "14. Obmezhennya vidpovidalnosti",
    },
    "art15_title": {
        "bg":    "15. Интелектуална собственост",
        "cs":    "15. Dusevni vlastnictvi",
        "da":    "15. Intellektuel ejendomsret",
        "de":    "15. Geistiges Eigentum",
        "el":    "15. Pneumatiki Idioktisia",
        "en":    "15. Intellectual Property",
        "es":    "15. Propiedad intelectual",
        "et":    "15. Intellektuaalomand",
        "fi":    "15. Immateriaalioikeudet",
        "fr":    "15. Propriete intellectuelle",
        "ga":    "15. Maoin Intleachtuil",
        "hr":    "15. Intelektualno vlasnistvo",
        "hu":    "15. Szellemi tulajdon",
        "is":    "15. Hugverkarettur",
        "it":    "15. Proprieta intellettuale",
        "lb":    "15. Intellektuell Eegeschaft",
        "lt":    "15. Intelektine nuosavybe",
        "lv":    "15. Intelektualais ipashums",
        "mk":    "15. Intelektualna sopstvenost",
        "mt":    "15. Proprieta Intellettwali",
        "nl":    "15. Intellectueel eigendom",
        "no":    "15. Intellektuell eiendomsrett",
        "pl":    "15. Wlasnosc intelektualna",
        "pt":    "15. Propriedade intelectual",
        "pt-PT": "15. Propriedade intelectual",
        "ro":    "15. Proprietate intelectuala",
        "ru":    "15. Intellektualnaya sobstvennost",
        "sk":    "15. Dusevne vlastnictvo",
        "sl":    "15. Intelektualna lastnina",
        "sq":    "15. Prona intelektuale",
        "sr":    "15. Intelektualna svojina",
        "sv":    "15. Immateriella rattigheter",
        "tr":    "15. Fikri Mulkiyet",
        "uk":    "15. Intelektualna vlasnist",
    },
    "art16_title": {
        "bg":    "16. Защита на личните данни",
        "cs":    "16. Ochrana osobnich udaju",
        "da":    "16. Beskyttelse af personoplysninger",
        "de":    "16. Datenschutz",
        "el":    "16. Prostasia Prosopikon Dedomenon",
        "en":    "16. Data Protection",
        "es":    "16. Proteccion de datos personales",
        "et":    "16. Isikuandmete kaitse",
        "fi":    "16. Tietosuoja",
        "fr":    "16. Protection des donnees personnelles",
        "ga":    "16. Cosaint Sonrai Pearsanta",
        "hr":    "16. Zastita osobnih podataka",
        "hu":    "16. Adatvedelem",
        "is":    "16. Personuvernd",
        "it":    "16. Protezione dei dati personali",
        "lb":    "16. Dateschutz",
        "lt":    "16. Asmens duomenu apsauga",
        "lv":    "16. Personas datu aizsardziba",
        "mk":    "16. Zastita na lichni podatoci",
        "mt":    "16. Protezzjoni tad-Data Personali",
        "nl":    "16. Gegevensbescherming",
        "no":    "16. Personvern",
        "pl":    "16. Ochrona danych osobowych",
        "pt":    "16. Protecao de dados pessoais",
        "pt-PT": "16. Protecao de dados pessoais",
        "ro":    "16. Protectia datelor cu caracter personal",
        "ru":    "16. Zashchita personalnykh dannykh",
        "sk":    "16. Ochrana osobnych udajov",
        "sl":    "16. Varstvo osebnih podatkov",
        "sq":    "16. Mbrojtja e te dhenave personale",
        "sr":    "16. Zastita licnih podataka",
        "sv":    "16. Dataskydd",
        "tr":    "16. Kisisel Verilerin Korunmasi",
        "uk":    "16. Zakhyst personalnykh danykh",
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
            f"✅ seed_provider_terms_p6_titles4: {count} rows upserted "
            f"({NAMESPACE}: art13_title, art14_title, art15_title, art16_title x 34 langs)"
        )

    engine.dispose()


if __name__ == "__main__":
    seed()
