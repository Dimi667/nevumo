from sqlalchemy import text
from apps.api.database import SessionLocal

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    insert_translations(db, TRANSLATIONS)
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
        SELECT lang, key, value
        FROM translations
        WHERE key IN ('category.nav_cta_line1', 'category.nav_cta_line2')
        ORDER BY lang, key
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} = {row[2]}")

RAW_DATA = {
    "bg": ("Предлагаш", "Включи се безплатно!"),
    "cs": ("Nabízíš", "Přidej se zdarma!"),
    "da": ("Tilbyder du", "Tilmeld dig gratis!"),
    "de": ("Bietest du", "Jetzt kostenlos mitmachen!"),
    "el": ("Προσφέρεις", "Εγγράψου δωρεάν!"),
    "en": ("Do you offer", "Join for free!"),
    "es": ("¿Ofreces", "Únete gratis!"),
    "et": ("Pakud", "Liitu tasuta!"),
    "fi": ("Tarjoatko", "Liity ilmaiseksi!"),
    "fr": ("Vous proposez", "Rejoignez-nous gratuitement!"),
    "ga": ("An dtairgeann tú", "Bí páirteach saor in aisce!"),
    "hr": ("Nudiš", "Pridruži se besplatno!"),
    "hu": ("Kínálsz", "Csatlakozz ingyen!"),
    "is": ("Býður þú upp á", "Skráðu þig ókeypis!"),
    "it": ("Offri", "Unisciti gratis!"),
    "lb": ("Bids du un", "Mach mat, gratis!"),
    "lt": ("Siūlai", "Prisijunk nemokamai!"),
    "lv": ("Piedāvā", "Pievienojies bez maksas!"),
    "mk": ("Нудиш", "Приклучи се бесплатно!"),
    "mt": ("Toffri", "Ingħaqad b'xejn!"),
    "nl": ("Bied jij", "Doe gratis mee!"),
    "no": ("Tilbyr du", "Bli med gratis!"),
    "pl": ("Oferujesz", "Dołącz za darmo!"),
    "pt": ("Você oferece", "Junte-se gratuitamente!"),
    "pt-PT": ("Ofereces", "Junta-te gratuitamente!"),
    "ro": ("Oferi", "Alătură-te gratuit!"),
    "ru": ("Предлагаешь", "Присоединяйся бесплатно!"),
    "sk": ("Ponúkaš", "Pridaj sa zadarmo!"),
    "sl": ("Ponujaš", "Pridruži se brezplačno!"),
    "sq": ("Ofron", "Bashkohu falas!"),
    "sr": ("Нудиш", "Придружи се бесплатно!"),
    "sv": ("Erbjuder du", "Gå med gratis!"),
    "tr": ("Sunuyor musun", "Ücretsiz katıl!"),
    "uk": ("Пропонуєш", "Приєднуйся безкоштовно!"),
}

TRANSLATIONS: dict[str, dict[str, str]] = {}
for lang, (line1, line2) in RAW_DATA.items():
    TRANSLATIONS[lang] = {
        "category.nav_cta_line1": line1,
        "category.nav_cta_line2": line2,
    }

if __name__ == "__main__":
    main()
