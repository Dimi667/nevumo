# -*- coding: utf-8 -*-
"""
Idempotent seed script to fix category.how_step_2 translations.

Updates the translation key for all 34 supported languages to correctly
convey: "The specialists contact you / reach out to you" - emphasizing that
providers actively reach out to the client.

Run: python -m apps.api.scripts.fix_how_step_2_translations
"""

from sqlalchemy import text

from apps.api.database import SessionLocal


def main() -> None:
    translations = [
        ("bg", "category.how_step_2", "Специалистите се свързват с теб"),
        ("cs", "category.how_step_2", "Specialisté vás kontaktují"),
        ("da", "category.how_step_2", "Specialisterne kontakter dig"),
        ("de", "category.how_step_2", "Die Spezialisten melden sich bei Ihnen"),
        ("el", "category.how_step_2", "Οι ειδικοί επικοινωνούν μαζί σας"),
        ("en", "category.how_step_2", "Specialists reach out to you"),
        ("es", "category.how_step_2", "Los especialistas se ponen en contacto contigo"),
        ("et", "category.how_step_2", "Spetsialistid võtavad teiega ühendust"),
        ("fi", "category.how_step_2", "Asiantuntijat ottavat sinuun yhteyttä"),
        ("fr", "category.how_step_2", "Les spécialistes vous contactent"),
        ("ga", "category.how_step_2", "Déanann na speisialtóirí teagmháil leat"),
        ("hr", "category.how_step_2", "Stručnjaci vas kontaktiraju"),
        ("hu", "category.how_step_2", "A szakemberek felveszik Önnel a kapcsolatot"),
        ("is", "category.how_step_2", "Sérfræðingarnir hafa samband við þig"),
        ("it", "category.how_step_2", "Gli specialisti ti contattano"),
        ("lb", "category.how_step_2", "D'Spezialiste mellen sech bei Iech"),
        ("lt", "category.how_step_2", "Specialistai susisiekia su jumis"),
        ("lv", "category.how_step_2", "Speciālisti sazinās ar jums"),
        ("mk", "category.how_step_2", "Специјалистите се поврзуваат со вас"),
        ("mt", "category.how_step_2", "L-ispeċjalisti jikkuntattjawk"),
        ("nl", "category.how_step_2", "De specialisten nemen contact met u op"),
        ("no", "category.how_step_2", "Spesialistene kontakter deg"),
        ("pl", "category.how_step_2", "Specjaliści kontaktują się z Tobą"),
        ("pt", "category.how_step_2", "Os especialistas entram em contato com você"),
        ("pt-PT", "category.how_step_2", "Os especialistas contactam-no"),
        ("ro", "category.how_step_2", "Specialiștii vă contactează"),
        ("ru", "category.how_step_2", "Специалисты связываются с вами"),
        ("sk", "category.how_step_2", "Odborníci vás kontaktujú"),
        ("sl", "category.how_step_2", "Strokovnjaki stopijo v stik z vami"),
        ("sq", "category.how_step_2", "Specialistët ju kontaktojnë"),
        ("sr", "category.how_step_2", "Стручњаци вас контактирају"),
        ("sv", "category.how_step_2", "Specialisterna kontaktar dig"),
        ("tr", "category.how_step_2", "Uzmanlar sizinle iletişime geçer"),
        ("uk", "category.how_step_2", "Фахівці зв'язуються з вами"),
    ]

    db = SessionLocal()
    try:
        upsert_query = text("""
            INSERT INTO translations (lang, key, value)
            VALUES (:lang, :key, :value)
            ON CONFLICT (lang, key) DO UPDATE
            SET value = EXCLUDED.value
        """)

        updated_count = 0
        for lang, key, value in translations:
            result = db.execute(upsert_query, {"lang": lang, "key": key, "value": value})
            updated_count += result.rowcount

        db.commit()
        print(f"Updated {updated_count} rows for category.how_step_2")
    finally:
        db.close()


if __name__ == "__main__":
    main()
