"""
seed_provider_terms_p7_titles5.py  —  Nevumo | namespace: provider_terms
Keys: art17_title, art18_title  (2 keys x 34 langs = 68 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p7_titles5
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
    "art17_title": {
        "bg":    "17. Приложимо право и юрисдикция",
        "cs":    "17. Rozhodne pravo a jurisdikce",
        "da":    "17. Galdende ret og jurisdiktion",
        "de":    "17. Anwendbares Recht und Gerichtsbarkeit",
        "el":    "17. Efarmosteo Dikaio kai Dikaiodoxia",
        "en":    "17. Governing Law and Jurisdiction",
        "es":    "17. Ley aplicable y jurisdiccion",
        "et":    "17. Kohaldatav oigus ja jurisdiktsioon",
        "fi":    "17. Sovellettava laki ja toimivalta",
        "fr":    "17. Droit applicable et juridiction",
        "ga":    "17. An Dli Rialachan agus Dlhinse",
        "hr":    "17. Mjerodavno pravo i nadleznost",
        "hu":    "17. Iranyadó jog es joghatosag",
        "is":    "17. Gildandi log og logsaga",
        "it":    "17. Legge applicabile e giurisdizione",
        "lb":    "17. Gëltend Recht a Gerichtsbarkeit",
        "lt":    "17. Taikytina teise ir jurisdikcija",
        "lv":    "17. Piemerojamie tiesibas un jurisdikcija",
        "mk":    "17. Merodavno pravo i nadleznost",
        "mt":    "17. Ligi Applikabbli u Gurisdizzjoni",
        "nl":    "17. Toepasselijk recht en jurisdictie",
        "no":    "17. Gjeldende rett og jurisdiksjon",
        "pl":    "17. Prawo właściwe i jurysdykcja",
        "pt":    "17. Lei aplicavel e jurisdicao",
        "pt-PT": "17. Lei aplicavel e jurisdicao",
        "ro":    "17. Legea aplicabila si jurisdictia",
        "ru":    "17. Primenimoe pravo i yurisdikciya",
        "sk":    "17. Rozhodne pravo a jurisdikcia",
        "sl":    "17. Veljavno pravo in pristojnost",
        "sq":    "17. Ligji i zbatueshem dhe juridiksioni",
        "sr":    "17. Merodavno pravo i nadleznost",
        "sv":    "17. Tillamplig lag och jurisdiktion",
        "tr":    "17. Uygulanacak Hukuk ve Yetki Alani",
        "uk":    "17. Zastosvuvane pravo ta yurysdyktsiya",
    },
    "art18_title": {
        "bg":    "18. Заключителни разпоредби",
        "cs":    "18. Zaverecna ustanoveni",
        "da":    "18. Afsluttende bestemmelser",
        "de":    "18. Schlussbestimmungen",
        "el":    "18. Telikes Diataxeis",
        "en":    "18. Final Provisions",
        "es":    "18. Disposiciones finales",
        "et":    "18. Loppsatted",
        "fi":    "18. Loppumaaraykset",
        "fr":    "18. Dispositions finales",
        "ga":    "18. Foralacha Deiridh",
        "hr":    "18. Zavrsne odredbe",
        "hu":    "18. Zarorendelkezesek",
        "is":    "18. Lokaakvaedi",
        "it":    "18. Disposizioni finali",
        "lb":    "18. Schlussbestemmungen",
        "lt":    "18. Baigiamosios nuostatos",
        "lv":    "18. Nobeiguma noteikumi",
        "mk":    "18. Zavrsni odredbi",
        "mt":    "18. Dispozizzjonijiet Finali",
        "nl":    "18. Slotbepalingen",
        "no":    "18. Sluttbestemmelser",
        "pl":    "18. Postanowienia końcowe",
        "pt":    "18. Disposicoes finais",
        "pt-PT": "18. Disposicoes finais",
        "ro":    "18. Dispozitii finale",
        "ru":    "18. Zaklyuchitelnye polozheniya",
        "sk":    "18. Zaverecne ustanovenia",
        "sl":    "18. Koncne dolocbe",
        "sq":    "18. Dispozitat perfundimtare",
        "sr":    "18. Zavrsne odredbe",
        "sv":    "18. Slutbestammelser",
        "tr":    "18. Son Hükümler",
        "uk":    "18. Prykintsevi polozhennya",
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
            f"✅ seed_provider_terms_p7_titles5: {count} rows upserted "
            f"({NAMESPACE}: art17_title, art18_title x 34 langs)"
        )

    engine.dispose()


if __name__ == "__main__":
    seed()
