#!/usr/bin/env python3
"""
Seed script for City Page CTA translations (city namespace)
Keys: city.nav_cta_line1, city.nav_cta_line2
Languages: 34
Run: docker exec nevumo-api python -m apps.api.scripts.seed_city_nav_cta_translations
"""
from sqlalchemy import text
from apps.api.database import SessionLocal

RAW_DATA = {
    "bg": ["Предлагаш услуги в", "Включи се безплатно! "],
    "cs": ["Nabízíš služby v", "Přidej se zdarma! "],
    "da": ["Tilbyder du tjenester i", "Tilmeld dig gratis! "],
    "de": ["Bietest du Dienstleistungen an in", "Kostenlos mitmachen! "],
    "el": ["Προσφέρεις υπηρεσίες σε", "Εγγράψου δωρεάν! "],
    "en": ["Do you offer services in", "Join for free! "],
    "es": ["¿Ofreces servicios en", "¡Únete gratis! "],
    "et": ["Kas pakud teenuseid linnas", "Liitu tasuta! "],
    "fi": ["Tarjoatko palveluita kohteessa", "Liity ilmaiseksi! "],
    "fr": ["Tu proposes des services à", "Rejoins-nous gratuitement ! "],
    "ga": ["An dtairgíonn tú seirbhísí i", "Cláraigh saor in aisce! "],
    "hr": ["Nudiš li usluge u", "Pridruži se besplatno! "],
    "hu": ["Szolgáltatásokat kínálsz itt:", "Csatlakozz ingyen! "],
    "is": ["Býður þú upp á þjónustu í", "Vertu með frítt! "],
    "it": ["Offri servizi a", "Iscriviti gratis! "],
    "lb": ["Pidds du Servicer un an", "Maach gratis mat! "],
    "lt": ["Teiki paslaugas", "Prisijunk nemokamai! "],
    "lv": ["Vai piedāvā pakalpojumus", "Pievienojies bez maksas! "],
    "mk": ["Нудиш услуги во", "Придружи се бесплатно! "],
    "mt": ["Toffri servizzi fi", "Ingħaqad b'xejn! "],
    "nl": ["Bied je diensten aan in", "Doe gratis mee! "],
    "no": ["Tilbyr du tjenester i", "Bli med gratis! "],
    "pl": ["Oferujesz usługi w", "Dołącz za darmo! "],
    "pt": ["Oferece serviços em", "Participe grátis! "],
    "pt-PT": ["Ofereces serviços em", "Adere gratuitamente! "],
    "ro": ["Oferi servicii în", "Alătură-te gratuit! "],
    "ru": ["Предлагаешь услуги в", "Присоединяйся бесплатно! "],
    "sk": ["Ponúkaš služby v", "Pridaj sa zadarmo! "],
    "sl": ["Ponujaš storitve v", "Pridruži se brezplačno! "],
    "sq": ["Ofron shërbime në", "Bashkohu falas! "],
    "sr": ["Nudiš usluge u", "Pridruži se besplatno! "],
    "sv": ["Erbjuder du tjänster i", "Gå med gratis! "],
    "tr": ["Hizmet veriyor musun:", "Ücretsiz katıl! "],
    "uk": ["Пропонуєш послуги в", "Приєднуйся безкоштовно! "],
}

TRANSLATIONS: dict[str, dict[str, str]] = {}
for lang, (line1, line2) in RAW_DATA.items():
    TRANSLATIONS[lang] = {
        "city.nav_cta_line1": line1,
        "city.nav_cta_line2": line2,
    }

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
        WHERE key IN ('city.nav_cta_line1', 'city.nav_cta_line2')
        ORDER BY lang, key
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} = {row[2]}")

if __name__ == "__main__":
    main()
