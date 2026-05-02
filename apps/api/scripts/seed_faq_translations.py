from sqlalchemy import text
from apps.api.database import SessionLocal

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    categories = ['cleaning', 'massage', 'plumbing']
    languages = ["en", "pl", "bg", "de", "fr", "es", "it", "nl", "cs", "ro", "tr", "ru", "uk", "el", "sv", "no", "da", "fi", "hu", "sk", "hr", "sr", "sl", "et", "lv", "lt", "mt", "is", "ga", "sq", "mk", "bs", "me", "hy"]
    
    # English values from CATEGORY_CONTENT
    faq_data_en = {
        'cleaning': [
            ('How to find a cleaning company in {city}?', 'On Nevumo you can send a free request to trusted cleaning companies in {city} and quickly receive responses from available specialists.'),
            ('How much does cleaning cost in {city}?', 'The price for cleaning in {city} ranges from {min_price} to {max_price} {currency} depending on the size of the area and the scope of work.'),
            ('Is the request free?', 'Yes, sending a request through Nevumo is completely free and without obligation.')
        ],
        'massage': [
            ('How to find a massage specialist in {city}?', 'On Nevumo you can send a free request to trusted massage specialists in {city} and receive a response in as little as 30 minutes.'),
            ('How much does massage cost in {city}?', 'The price for a massage in {city} starts from {min_price} {currency}.'),
            ('Is the request free?', 'Yes, sending a request through Nevumo is completely free and without obligation.')
        ],
        'plumbing': [
            ('How to find a plumber in {city}?', 'On Nevumo you can send a free request to trusted plumbers in {city} and receive a response quickly.'),
            ('How much does a plumber cost in {city}?', 'The price for plumbing services in {city} ranges from {min_price} to {max_price} {currency} depending on the complexity of the task.'),
            ('Is the request free?', 'Yes, sending a request through Nevumo is completely free and without obligation.')
        ]
    }

    # Bulgarian values
    faq_data_bg = {
        'cleaning': [
            ('Как да намеря фирма за почистване в {city}?', 'В Nevumo можете да изпратите безплатно запитване до доверени фирми за почистване в {city} и бързо да получите оферти от свободни специалисти.'),
            ('Колко струва почистването в {city}?', 'Цената за почистване в {city} варира от {min_price} до {max_price} {currency} в зависимост от големината на обекта и обема на работа.'),
            ('Безплатно ли е запитването?', 'Да, изпращането на запитване чрез Nevumo е напълно безплатно и без ангажименти.')
        ],
        'massage': [
            ('Как да намеря масажист в {city}?', 'В Nevumo можете да изпратите безплатно запитване до доверени специалисти по масаж в {city} и да получите отговор до 30 минути.'),
            ('Колко струва масажът в {city}?', 'Цената за масаж в {city} започва от {min_price} {currency}.'),
            ('Безплатно ли е запитването?', 'Да, изпращането на запитване чрез Nevumo е напълно безплатно и без ангажименти.')
        ],
        'plumbing': [
            ('Как да намеря водопроводчик в {city}?', 'В Nevumo можете да изпратите безплатно запитване до доверени водопроводчици в {city} и бързо да получите отговор.'),
            ('Колко струват водопроводните услуги в {city}?', 'Цената за водопроводни услуги в {city} варира от {min_price} до {max_price} {currency} в зависимост от сложността на задачата.'),
            ('Безплатно ли е запитването?', 'Да, изпращането на запитване чрез Nevumo е напълно безплатно и без ангажименти.')
        ]
    }

    count = 0
    for lang in languages:
        data = faq_data_bg if lang == 'bg' else faq_data_en
        
        # Add general FAQ title
        faq_title = "Често задавани въпроси" if lang == 'bg' else "Frequently Asked Questions"
        db.execute(
            text("""
                INSERT INTO translations (lang, key, value)
                VALUES (:lang, :key, :value)
                ON CONFLICT (lang, key)
                DO UPDATE SET value = EXCLUDED.value
            """),
            {"lang": lang, "key": "category.faq_title", "value": faq_title}
        )
        count += 1

        for cat, faqs in data.items():
            for i, (q, a) in enumerate(faqs, 1):
                keys = [
                    (f"category.faq_{cat}_q{i}", q),
                    (f"category.faq_{cat}_a{i}", a)
                ]
                for key, value in keys:
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
    print(f"Inserted/updated {count} FAQ translation rows")

if __name__ == "__main__":
    main()
