#!/usr/bin/env python3
"""
Seed script for widget.send_request_to translation
Run: python -m apps.api.scripts.seed_widget_send_request_to
"""
import os
import psycopg2

TRANSLATIONS = {
    "bg": {"widget.send_request_to": "Изпратете заявка директно на"},
    "cs": {"widget.send_request_to": "Odešlete žádost přímo na"},
    "da": {"widget.send_request_to": "Send en forespørgsel direkte til"},
    "de": {"widget.send_request_to": "Anfrage direkt senden an"},
    "el": {"widget.send_request_to": "Στείλτε αίτημα απευθείας στον/στην"},
    "en": {"widget.send_request_to": "Send request directly to"},
    "es": {"widget.send_request_to": "Envía una solicitud directamente a"},
    "et": {"widget.send_request_to": "Saada päring otse kasutajale"},
    "fi": {"widget.send_request_to": "Lähetä pyyntö suoraan henkilölle"},
    "fr": {"widget.send_request_to": "Envoyer une demande directement à"},
    "ga": {"widget.send_request_to": "Seol iarratas go díreach chuig"},
    "hr": {"widget.send_request_to": "Pošaljite zahtjev izravno na"},
    "hu": {"widget.send_request_to": "Kérés küldése közvetlenül neki"},
    "is": {"widget.send_request_to": "Sendu beiðni beint til"},
    "it": {"widget.send_request_to": "Invia una richiesta direttamente a"},
    "lb": {"widget.send_request_to": "Schéckt eng Ufro direkt un"},
    "lt": {"widget.send_request_to": "Siųsti užklausą tiesiogiai"},
    "lv": {"widget.send_request_to": "Sūtīt pieprasījumu tieši uz"},
    "mk": {"widget.send_request_to": "Испратете барање директно до"},
    "mt": {"widget.send_request_to": "Ibgħat talba direttament lil"},
    "nl": {"widget.send_request_to": "Stuur een aanvraag direct naar"},
    "no": {"widget.send_request_to": "Send en forespørsel direkte til"},
    "pl": {"widget.send_request_to": "Wyślij zapytanie bezpośrednio do"},
    "pt": {"widget.send_request_to": "Envie uma solicitação diretamente para"},
    "pt-PT": {"widget.send_request_to": "Envie um pedido diretamente para"},
    "ro": {"widget.send_request_to": "Trimite o cerere direct către"},
    "ru": {"widget.send_request_to": "Отправить запрос напрямую"},
    "sk": {"widget.send_request_to": "Odoslať požiadavku priamo na"},
    "sl": {"widget.send_request_to": "Pošljite zahtevo neposredno na"},
    "sq": {"widget.send_request_to": "Dërgo kërkesë drejtpërdrejt tek"},
    "sr": {"widget.send_request_to": "Пошаљите захтев директно на"},
    "sv": {"widget.send_request_to": "Skicka en förfrågan direkt till"},
    "tr": {"widget.send_request_to": "Doğrudan şu kişiye istek gönder:"},
    "uk": {"widget.send_request_to": "Надішліть запит безпосередньо до"},
}


def main() -> None:
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return

    print("Seeding widget.send_request_to translations...")

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    count = 0

    for lang, keys in TRANSLATIONS.items():
        for key, value in keys.items():
            cur.execute("""
                INSERT INTO translations (lang, key, value)
                VALUES (%s, %s, %s)
                ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
            """, (lang, key, value))
            count += 1

    conn.commit()
    cur.close()
    conn.close()

    print(f"Seeded widget.send_request_to translations: {count} rows")


if __name__ == '__main__':
    main()
