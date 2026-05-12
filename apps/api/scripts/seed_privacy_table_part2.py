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
        WHERE key LIKE 'privacy.%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
  "en": {
    "privacy.t31_email_data": "Email address",
    "privacy.t31_email_purpose": "Account creation, login",
    "privacy.t31_password_data": "Password (bcrypt hash)",
    "privacy.t31_password_purpose": "Account security",
    "privacy.t31_role_data": "Role (client / provider)",
    "privacy.t31_role_purpose": "Platform functionality",
    "privacy.t31_age_data": "Age confirmation (18+)",
    "privacy.t31_age_purpose": "Legal requirement",
    "privacy.t32_name_data": "Name, description, category",
    "privacy.t32_name_purpose": "Public profile",
    "privacy.t32_photo_data": "Profile photo (optional)",
    "privacy.t32_photo_purpose": "Public display",
    "privacy.t32_phone_data": "Phone number",
    "privacy.t32_phone_purpose": "Lead delivery, communication",
    "privacy.t32_location_data": "Location / city",
    "privacy.t32_location_purpose": "Service area matching",
    "privacy.t32_services_data": "Services and prices",
    "privacy.t32_services_purpose": "Marketplace listing",
  },
  "bg": {
    "privacy.t31_email_data": "Имейл адрес",
    "privacy.t31_email_purpose": "Създаване на акаунт, вход",
    "privacy.t31_password_data": "Парола (bcrypt хеш)",
    "privacy.t31_password_purpose": "Сигурност на акаунта",
    "privacy.t31_role_data": "Роля (клиент / доставчик)",
    "privacy.t31_role_purpose": "Функционалност на платформата",
    "privacy.t31_age_data": "Потвърждение за възраст (18+)",
    "privacy.t31_age_purpose": "Законово изискване",
    "privacy.t32_name_data": "Име, описание, категория",
    "privacy.t32_name_purpose": "Публичен профил",
    "privacy.t32_photo_data": "Снимка на профила (незадължително)",
    "privacy.t32_photo_purpose": "Публично показване",
    "privacy.t32_phone_data": "Телефонен номер",
    "privacy.t32_phone_purpose": "Доставка на заявки, комуникация",
    "privacy.t32_location_data": "Местоположение / град",
    "privacy.t32_location_purpose": "Съпоставяне на зона на обслужване",
    "privacy.t32_services_data": "Услуги и цени",
    "privacy.t32_services_purpose": "Обява в платформата",
  },
  "pl": {
    "privacy.t31_email_data": "Adres e-mail",
    "privacy.t31_email_purpose": "Rejestracja konta, logowanie",
    "privacy.t31_password_data": "Hasło (hash bcrypt)",
    "privacy.t31_password_purpose": "Bezpieczeństwo konta",
    "privacy.t31_role_data": "Rola (klient / dostawca)",
    "privacy.t31_role_purpose": "Funkcjonalność platformy",
    "privacy.t31_age_data": "Potwierdzenie wieku (18+)",
    "privacy.t31_age_purpose": "Wymóg prawny",
    "privacy.t32_name_data": "Imię/nazwa, opis, kategoria",
    "privacy.t32_name_purpose": "Profil publiczny",
    "privacy.t32_photo_data": "Zdjęcie profilowe (opcjonalne)",
    "privacy.t32_photo_purpose": "Wyświetlanie publiczne",
    "privacy.t32_phone_data": "Numer telefonu",
    "privacy.t32_phone_purpose": "Przekazywanie zapytań, komunikacja",
    "privacy.t32_location_data": "Lokalizacja / miasto",
    "privacy.t32_location_purpose": "Dopasowanie obszaru usług",
    "privacy.t32_services_data": "Usługi i ceny",
    "privacy.t32_services_purpose": "Ogłoszenie na platformie",
  },
}

if __name__ == "__main__":
    main()
