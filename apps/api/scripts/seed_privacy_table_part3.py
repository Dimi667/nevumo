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
    "privacy.t33_request_data": "Request details",
    "privacy.t33_request_purpose": "Client-provider matching",
    "privacy.t33_contact_data": "Contact information",
    "privacy.t33_contact_purpose": "Communication",
    "privacy.t33_status_data": "Lead status history",
    "privacy.t33_status_purpose": "Functionality & disputes",
    "privacy.t34_ip_data": "IP address (hashed)",
    "privacy.t34_ip_purpose": "Security, rate limiting",
    "privacy.t34_agent_data": "User agent",
    "privacy.t34_agent_purpose": "Security & diagnostics",
    "privacy.t34_authlogs_data": "Auth logs",
    "privacy.t34_authlogs_purpose": "Security monitoring",
    "privacy.t5_analytics": "Analytics",
    "privacy.t5_payments": "Payments (BLIK, Przelewy24)",
    "privacy.t5_emails": "Transactional emails",
    "privacy.t5_frontend": "Frontend hosting",
    "privacy.t5_backend": "Backend API hosting",
    "privacy.t5_database": "Database (PostgreSQL)",
    "privacy.t5_redis": "Redis cache",
    "privacy.t5_storage": "File/image storage (R2)",
    "privacy.t5_usa": "USA",
    "privacy.t5_sccs": "SCCs",
    "privacy.t5_sccs_dpf": "SCCs + DPF",
  },
  "bg": {
    "privacy.t33_request_data": "Детайли на заявката",
    "privacy.t33_request_purpose": "Съпоставяне на клиент с доставчик",
    "privacy.t33_contact_data": "Данни за контакт",
    "privacy.t33_contact_purpose": "Комуникация",
    "privacy.t33_status_data": "История на статуса на заявката",
    "privacy.t33_status_purpose": "Функционалност и спорове",
    "privacy.t34_ip_data": "IP адрес (хеширан)",
    "privacy.t34_ip_purpose": "Сигурност, ограничаване на заявки",
    "privacy.t34_agent_data": "User agent",
    "privacy.t34_agent_purpose": "Сигурност и диагностика",
    "privacy.t34_authlogs_data": "Логове за удостоверяване",
    "privacy.t34_authlogs_purpose": "Наблюдение на сигурността",
    "privacy.t5_analytics": "Анализи",
    "privacy.t5_payments": "Плащания (BLIK, Przelewy24)",
    "privacy.t5_emails": "Транзакционни имейли",
    "privacy.t5_frontend": "Хостинг на фронтенд",
    "privacy.t5_backend": "Хостинг на бекенд API",
    "privacy.t5_database": "База данни (PostgreSQL)",
    "privacy.t5_redis": "Redis кеш",
    "privacy.t5_storage": "Съхранение на файлове/изображения (R2)",
    "privacy.t5_usa": "САЩ",
    "privacy.t5_sccs": "СДК",
    "privacy.t5_sccs_dpf": "СДК + DPF",
  },
  "pl": {
    "privacy.t33_request_data": "Szczegóły zapytania",
    "privacy.t33_request_purpose": "Dopasowanie klient–dostawca",
    "privacy.t33_contact_data": "Dane kontaktowe",
    "privacy.t33_contact_purpose": "Komunikacja",
    "privacy.t33_status_data": "Historia statusu zapytania",
    "privacy.t33_status_purpose": "Funkcjonalność i spory",
    "privacy.t34_ip_data": "Adres IP (zahaszowany)",
    "privacy.t34_ip_purpose": "Bezpieczeństwo, ograniczenie żądań",
    "privacy.t34_agent_data": "User agent",
    "privacy.t34_agent_purpose": "Bezpieczeństwo i diagnostyka",
    "privacy.t34_authlogs_data": "Logi uwierzytelniania",
    "privacy.t34_authlogs_purpose": "Monitorowanie bezpieczeństwa",
    "privacy.t5_analytics": "Analityka",
    "privacy.t5_payments": "Płatności (BLIK, Przelewy24)",
    "privacy.t5_emails": "E-maile transakcyjne",
    "privacy.t5_frontend": "Hosting frontendu",
    "privacy.t5_backend": "Hosting backendu API",
    "privacy.t5_database": "Baza danych (PostgreSQL)",
    "privacy.t5_redis": "Cache Redis",
    "privacy.t5_storage": "Przechowywanie plików/obrazów (R2)",
    "privacy.t5_usa": "USA",
    "privacy.t5_sccs": "SCC",
    "privacy.t5_sccs_dpf": "SCC + DPF",
  },
}

if __name__ == "__main__":
    main()
