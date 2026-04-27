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
        SELECT lang, value
        FROM translations
        WHERE key = 'provider_dashboard.qr_slogan_submit_request'
        ORDER BY lang
    """))
    rows = result.fetchall()
    print(f"\nVerification: {len(rows)} languages seeded")
    for row in rows:
        print(f"  {row[0]}: {row[1]}")


ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {"provider_dashboard.qr_slogan_submit_request": "Send a request in 30 sec!"},
    "bg": {"provider_dashboard.qr_slogan_submit_request": "Пусни заявка за 30 сек!"},
    "pl": {"provider_dashboard.qr_slogan_submit_request": "Wyślij zapytanie w 30 sek!"},
    "de": {"provider_dashboard.qr_slogan_submit_request": "Anfrage in 30 Sek. senden!"},
    "fr": {"provider_dashboard.qr_slogan_submit_request": "Envoyez une demande en 30 sec!"},
    "es": {"provider_dashboard.qr_slogan_submit_request": "¡Envía una solicitud en 30 seg!"},
    "it": {"provider_dashboard.qr_slogan_submit_request": "Invia una richiesta in 30 sec!"},
    "pt": {"provider_dashboard.qr_slogan_submit_request": "Envie uma solicitação em 30 seg!"},
    "pt-PT": {"provider_dashboard.qr_slogan_submit_request": "Envie um pedido em 30 seg!"},
    "nl": {"provider_dashboard.qr_slogan_submit_request": "Stuur een aanvraag in 30 sec!"},
    "cs": {"provider_dashboard.qr_slogan_submit_request": "Pošlete požadavek za 30 sec!"},
    "sk": {"provider_dashboard.qr_slogan_submit_request": "Pošlite požiadavku za 30 sek!"},
    "hu": {"provider_dashboard.qr_slogan_submit_request": "Küldj kérést 30 mp alatt!"},
    "ro": {"provider_dashboard.qr_slogan_submit_request": "Trimite o cerere în 30 sec!"},
    "hr": {"provider_dashboard.qr_slogan_submit_request": "Pošaljite zahtjev za 30 sek!"},
    "sl": {"provider_dashboard.qr_slogan_submit_request": "Pošlji zahtevo v 30 sek!"},
    "sr": {"provider_dashboard.qr_slogan_submit_request": "Pošalji zahtev za 30 sek!"},
    "mk": {"provider_dashboard.qr_slogan_submit_request": "Испрати барање за 30 сек!"},
    "sq": {"provider_dashboard.qr_slogan_submit_request": "Dërgo një kërkesë në 30 sek!"},
    "el": {"provider_dashboard.qr_slogan_submit_request": "Στείλε αίτημα σε 30 δευτ.!"},
    "ru": {"provider_dashboard.qr_slogan_submit_request": "Отправь заявку за 30 сек!"},
    "uk": {"provider_dashboard.qr_slogan_submit_request": "Надішли запит за 30 сек!"},
    "tr": {"provider_dashboard.qr_slogan_submit_request": "30 saniyede istek gönder!"},
    "da": {"provider_dashboard.qr_slogan_submit_request": "Send en anmodning på 30 sek!"},
    "sv": {"provider_dashboard.qr_slogan_submit_request": "Skicka en förfrågan på 30 sek!"},
    "no": {"provider_dashboard.qr_slogan_submit_request": "Send en forespørsel på 30 sek!"},
    "fi": {"provider_dashboard.qr_slogan_submit_request": "Lähetä pyyntö 30 sekunnissa!"},
    "et": {"provider_dashboard.qr_slogan_submit_request": "Saada päring 30 sekundiga!"},
    "lv": {"provider_dashboard.qr_slogan_submit_request": "Nosūti pieprasījumu 30 sek!"},
    "lt": {"provider_dashboard.qr_slogan_submit_request": "Siųsk užklausą per 30 sek!"},
    "ga": {"provider_dashboard.qr_slogan_submit_request": "Seol iarratas in 30 soic!"},
    "is": {"provider_dashboard.qr_slogan_submit_request": "Sendu beiðni á 30 sek!"},
    "lb": {"provider_dashboard.qr_slogan_submit_request": "Schéck eng Ufro a 30 Sek!"},
    "mt": {"provider_dashboard.qr_slogan_submit_request": "Ibgħat talba f'30 sekondi!"},
}


if __name__ == "__main__":
    main()
