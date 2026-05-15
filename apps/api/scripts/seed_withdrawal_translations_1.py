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
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "bg": {
        "withdrawal.page_title": "Формуляр за отказ",
        "withdrawal.page_description": "Попълнете този формуляр, за да се откажете от договора си с Nevumo",
        "withdrawal.form_service_description_label": "Описание на услугата / договора",
        "withdrawal.form_contract_date_label": "Дата на сключване на договора / Дата на регистрация на акаунта",
    },
    "pl": {
        "withdrawal.page_title": "Formularz odstąpienia od umowy",
        "withdrawal.page_description": "Wypełnij ten formularz, aby odstąpić od umowy z Nevumo",
        "withdrawal.form_service_description_label": "Opis usługi / umowy",
        "withdrawal.form_contract_date_label": "Data zawarcia umowy / Data rejestracji konta",
    },
    "cs": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "da": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "de": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "el": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "es": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "et": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "fi": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "fr": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "ga": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "hr": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "hu": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "is": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "it": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "lb": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "lt": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "lv": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "mk": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "mt": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "nl": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "no": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "pt": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "pt-PT": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "ro": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "ru": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "sk": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "sl": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "sq": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "sr": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "sv": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "tr": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "uk": {
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
}

if __name__ == "__main__":
    main()
