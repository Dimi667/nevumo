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
        WHERE key LIKE 'withdrawal.%' OR key LIKE 'withdrawal_%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "bg": {
        "withdrawal.form_consumer_name_label": "Име(на) на потребителя(-ите)",
        "withdrawal.form_consumer_address_label": "Адрес на потребителя(-ите)",
        "withdrawal.form_account_id_label": "Идентификатор на акаунт в Nevumo (ако е приложимо)",
        "withdrawal.form_email_label": "Имейл адрес, регистриран в Nevumo",
    },
    "pl": {
        "withdrawal.form_consumer_name_label": "Imię i nazwisko konsumenta(-ów)",
        "withdrawal.form_consumer_address_label": "Adres konsumenta(-ów)",
        "withdrawal.form_account_id_label": "Numer konta w serwisie Nevumo (jeżeli posiada)",
        "withdrawal.form_email_label": "Adres e-mail zarejestrowany w serwisie Nevumo",
    },
    "cs": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "da": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "de": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "el": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "es": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "et": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "fi": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "fr": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "ga": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "hr": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "hu": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "is": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "it": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "lb": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "lt": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "lv": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "mk": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "mt": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "nl": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "no": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "pt": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "pt-PT": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "ro": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "ru": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "sk": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "sl": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "sq": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "sr": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "sv": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "tr": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
    "uk": {
        "withdrawal.form_consumer_name_label": "Name of consumer(s)",
        "withdrawal.form_consumer_address_label": "Address of consumer(s)",
        "withdrawal.form_account_id_label": "Nevumo account ID (if applicable)",
        "withdrawal.form_email_label": "Email address registered with Nevumo",
    },
}

if __name__ == "__main__":
    main()
