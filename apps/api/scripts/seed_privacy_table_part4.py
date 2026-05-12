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
    "privacy.t4_purpose_consent_record": "Cookie consent record",
    "privacy.t4_purpose_lang_pref": "Language preference",
    "privacy.t4_purpose_ga4": "GA4 analytics",
    "privacy.t4_purpose_stripe_fraud": "Stripe fraud prevention (checkout)",
    "privacy.t4_purpose_auth_jwt": "Auth JWT",
    "privacy.t4_purpose_user_cache": "User info cache",
    "privacy.t4_purpose_phone_autofill": "Phone autofill",
    "privacy.t4_purpose_ux_role": "UX role at login",
    "privacy.t4_purpose_city_pref": "Preferred city",
    "privacy.t4_purpose_email_reg": "Email during registration",
    "privacy.t4_ret_12m": "12 months",
    "privacy.t4_ret_30d": "30 days",
    "privacy.t4_ret_13m": "13 months",
    "privacy.t4_ret_1y": "1 year",
    "privacy.t4_ret_30min": "30 min",
    "privacy.t4_ret_indefinite": "Indefinite",
    "privacy.t4_ret_session": "Session",
    "privacy.t4_ret_session_tab": "Session (tab)",
    "privacy.t4_basis_necessary": "Necessary",
    "privacy.t4_basis_functional": "Functional",
    "privacy.t4_basis_consent": "Consent",
    "privacy.t4_basis_contract": "Contract",
    "privacy.t4_basis_legint": "Legitimate interest",
  },
  "bg": {
    "privacy.t4_purpose_consent_record": "Запис за съгласие с бисквитки",
    "privacy.t4_purpose_lang_pref": "Предпочитан език",
    "privacy.t4_purpose_ga4": "GA4 анализи",
    "privacy.t4_purpose_stripe_fraud": "Защита от измами Stripe (плащане)",
    "privacy.t4_purpose_auth_jwt": "Токен за удостоверяване (JWT)",
    "privacy.t4_purpose_user_cache": "Кеш на потребителска информация",
    "privacy.t4_purpose_phone_autofill": "Автоматично попълване на телефон",
    "privacy.t4_purpose_ux_role": "UX роля при вход",
    "privacy.t4_purpose_city_pref": "Предпочитан град",
    "privacy.t4_purpose_email_reg": "Имейл по време на регистрация",
    "privacy.t4_ret_12m": "12 месеца",
    "privacy.t4_ret_30d": "30 дни",
    "privacy.t4_ret_13m": "13 месеца",
    "privacy.t4_ret_1y": "1 година",
    "privacy.t4_ret_30min": "30 мин",
    "privacy.t4_ret_indefinite": "Неограничено",
    "privacy.t4_ret_session": "Сесия",
    "privacy.t4_ret_session_tab": "Сесия (раздел)",
    "privacy.t4_basis_necessary": "Задължителен",
    "privacy.t4_basis_functional": "Функционален",
    "privacy.t4_basis_consent": "Съгласие",
    "privacy.t4_basis_contract": "Договор",
    "privacy.t4_basis_legint": "Легитимен интерес",
  },
  "pl": {
    "privacy.t4_purpose_consent_record": "Zapis zgody na pliki cookie",
    "privacy.t4_purpose_lang_pref": "Preferencja językowa",
    "privacy.t4_purpose_ga4": "Analityka GA4",
    "privacy.t4_purpose_stripe_fraud": "Zapobieganie oszustwom Stripe (płatność)",
    "privacy.t4_purpose_auth_jwt": "Token uwierzytelniający (JWT)",
    "privacy.t4_purpose_user_cache": "Pamięć podręczna informacji o użytkowniku",
    "privacy.t4_purpose_phone_autofill": "Automatyczne uzupełnianie telefonu",
    "privacy.t4_purpose_ux_role": "Rola UX przy logowaniu",
    "privacy.t4_purpose_city_pref": "Preferowane miasto",
    "privacy.t4_purpose_email_reg": "E-mail podczas rejestracji",
    "privacy.t4_ret_12m": "12 miesięcy",
    "privacy.t4_ret_30d": "30 dni",
    "privacy.t4_ret_13m": "13 miesięcy",
    "privacy.t4_ret_1y": "1 rok",
    "privacy.t4_ret_30min": "30 min",
    "privacy.t4_ret_indefinite": "Bezterminowo",
    "privacy.t4_ret_session": "Sesja",
    "privacy.t4_ret_session_tab": "Sesja (karta)",
    "privacy.t4_basis_necessary": "Niezbędne",
    "privacy.t4_basis_functional": "Funkcjonalne",
    "privacy.t4_basis_consent": "Zgoda",
    "privacy.t4_basis_contract": "Umowa",
    "privacy.t4_basis_legint": "Uzasadniony interes",
  },
}

if __name__ == "__main__":
    main()
