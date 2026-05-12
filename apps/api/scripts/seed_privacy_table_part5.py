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
    "privacy.t8_active_account": "Active account",
    "privacy.t8_until_deletion": "Until deletion",
    "privacy.t8_data_after_deletion": "Data after deletion",
    "privacy.t8_ret_30days_backups": "Max 30 days (encrypted backups)",
    "privacy.t8_financial_records": "Financial / Stripe records",
    "privacy.t8_ret_10years": "10 years",
    "privacy.t8_security_logs": "Security logs (hashed IP)",
    "privacy.t8_ret_90days": "90 days",
    "privacy.t8_ga4_analytics": "GA4 analytics",
    "privacy.t8_ret_14months": "14 months",
    "privacy.t8_cookie_consent_records": "Cookie consent records",
    "privacy.t8_ret_24months": "24 months",
    "privacy.t8_marketing_consent": "Marketing consent",
    "privacy.t8_ret_withdrawal_3y": "Until withdrawal + 3 years",
  },
  "bg": {
    "privacy.t8_active_account": "Активен акаунт",
    "privacy.t8_until_deletion": "До изтриване",
    "privacy.t8_data_after_deletion": "Данни след изтриване",
    "privacy.t8_ret_30days_backups": "Макс. 30 дни (криптирани резервни копия)",
    "privacy.t8_financial_records": "Финансови / Stripe записи",
    "privacy.t8_ret_10years": "10 години",
    "privacy.t8_security_logs": "Логове за сигурност (хеширано IP)",
    "privacy.t8_ret_90days": "90 дни",
    "privacy.t8_ga4_analytics": "GA4 анализи",
    "privacy.t8_ret_14months": "14 месеца",
    "privacy.t8_cookie_consent_records": "Записи за съгласие с бисквитки",
    "privacy.t8_ret_24months": "24 месеца",
    "privacy.t8_marketing_consent": "Маркетингово съгласие",
    "privacy.t8_ret_withdrawal_3y": "До оттегляне + 3 години",
  },
  "pl": {
    "privacy.t8_active_account": "Aktywne konto",
    "privacy.t8_until_deletion": "Do usunięcia",
    "privacy.t8_data_after_deletion": "Dane po usunięciu",
    "privacy.t8_ret_30days_backups": "Maks. 30 dni (zaszyfrowane kopie zapasowe)",
    "privacy.t8_financial_records": "Dane finansowe / Stripe",
    "privacy.t8_ret_10years": "10 lat",
    "privacy.t8_security_logs": "Logi bezpieczeństwa (zahaszowane IP)",
    "privacy.t8_ret_90days": "90 dni",
    "privacy.t8_ga4_analytics": "Analityka GA4",
    "privacy.t8_ret_14months": "14 miesięcy",
    "privacy.t8_cookie_consent_records": "Zapisy zgody na pliki cookie",
    "privacy.t8_ret_24months": "24 miesiące",
    "privacy.t8_marketing_consent": "Zgoda marketingowa",
    "privacy.t8_ret_withdrawal_3y": "Do wycofania + 3 lata",
  },
}

if __name__ == "__main__":
    main()
