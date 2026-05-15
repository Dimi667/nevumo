from sqlalchemy import text
from apps.api.database import SessionLocal

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    insert_translations(db, ALL_TRANSLATIONS)
    verify(db)

def insert_translations(db, data: dict[str, dict[str, str]]) -> None:
    count = 0
    for lang, keys in data.items():
        for key, value in keys.items():
            db.execute(
                text("""
                    INSERT INTO translations (lang, key, value)
                    VALUES (:lang, :key, :value)
                    ON CONFLICT (lang, key)
                    DO UPDATE SET value = EXCLUDED.value
                """),
                {"lang": lang, "key": key, "value": value}
            )
            count += 1
    db.commit()
    print(f"Inserted/updated {count} translation rows")

def verify(db) -> None:
    result = db.execute(text("""
        SELECT lang, COUNT(*) as keys
        FROM translations
        WHERE key LIKE 'pdf.footer_%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "trading as Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "Email: legal@nevumo.com",
    },
    "bg": {
        "pdf.footer_company_name": "\"ФИЛИПС ЦЕНТЪР БЪЛГАРИЯ\" ООД",
        "pdf.footer_company_info": "с търговска марка Nevumo",
        "pdf.footer_address": "бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България",
        "pdf.footer_email": "Имейл: legal@nevumo.com",
    },
    "pl": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "działająca jako Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-mail: legal@nevumo.com",
    },
    "cs": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "obchodní název Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-mail: legal@nevumo.com",
    },
    "da": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "handlende som Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-mail: legal@nevumo.com",
    },
    "de": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "handelnd als Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-Mail: legal@nevumo.com",
    },
    "el": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "που λειτουργεί ως Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "Ηλεκτρονικό ταχυδρομείο: legal@nevumo.com",
    },
    "es": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "operando como Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "Correo electrónico: legal@nevumo.com",
    },
    "et": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "kes tegutseb kui Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-post: legal@nevumo.com",
    },
    "fi": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "toimii nimellä Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "Sähköposti: legal@nevumo.com",
    },
    "fr": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "opérant sous le nom Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-mail : legal@nevumo.com",
    },
    "ga": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "ag feidhmiú mar Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "Ríomhphost: legal@nevumo.com",
    },
    "hr": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "posluje kao Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-pošta: legal@nevumo.com",
    },
    "hu": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "Nevumo néven működik",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-mail: legal@nevumo.com",
    },
    "is": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "starfar sem Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "Netfang: legal@nevumo.com",
    },
    "it": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "operante come Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-mail: legal@nevumo.com",
    },
    "lb": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "handelt als Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-Mail: legal@nevumo.com",
    },
    "lt": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "veikia kaip Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "El. paštas: legal@nevumo.com",
    },
    "lv": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "darbojas kā Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-pasts: legal@nevumo.com",
    },
    "mk": {
        "pdf.footer_company_name": "\"ФИЛИПС ЦЕНТАР България\" ООД",
        "pdf.footer_company_info": "работи како Nevumo",
        "pdf.footer_address": "бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България",
        "pdf.footer_email": "Е-пошта: legal@nevumo.com",
    },
    "mt": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "operat bħala Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-mail: legal@nevumo.com",
    },
    "nl": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "handelend als Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-mail: legal@nevumo.com",
    },
    "no": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "opererer som Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-post: legal@nevumo.com",
    },
    "pt": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "operando como Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-mail: legal@nevumo.com",
    },
    "pt-PT": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "operando como Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-mail: legal@nevumo.com",
    },
    "ro": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "operând ca Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-mail: legal@nevumo.com",
    },
    "ru": {
        "pdf.footer_company_name": "\"ФИЛИПС ЦЕНТР БОЛГАРИЯ\" ООО",
        "pdf.footer_company_info": "работает как Nevumo",
        "pdf.footer_address": "бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България",
        "pdf.footer_email": "Электронная почта: legal@nevumo.com",
    },
    "sk": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "pôsobiaca ako Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-mail: legal@nevumo.com",
    },
    "sl": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "posluje kot Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-pošta: legal@nevumo.com",
    },
    "sq": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "që operon si Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "Email: legal@nevumo.com",
    },
    "sr": {
        "pdf.footer_company_name": "\"ФИЛИПС ЦЕНТАР БУЛГАРИЈА\" ООД",
        "pdf.footer_company_info": "послује као Nevumo",
        "pdf.footer_address": "бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България",
        "pdf.footer_email": "Е-пошта: legal@nevumo.com",
    },
    "sv": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "verksam som Nevumo",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-post: legal@nevumo.com",
    },
    "tr": {
        "pdf.footer_company_name": "\"PHILIPS CENTER BULGARIA\" OOD",
        "pdf.footer_company_info": "Nevumo adıyla faaliyet gösteren",
        "pdf.footer_address": "bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria",
        "pdf.footer_email": "E-posta: legal@nevumo.com",
    },
    "uk": {
        "pdf.footer_company_name": "\"ФІЛІПС ЦЕНТР БОЛГАРІЯ\" ТОВ",
        "pdf.footer_company_info": "працює як Nevumo",
        "pdf.footer_address": "бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадиця, п.к. 1408, гр. Софія, Болгарія",
        "pdf.footer_email": "Електронна пошта: legal@nevumo.com",
    },
}

if __name__ == "__main__":
    main()
