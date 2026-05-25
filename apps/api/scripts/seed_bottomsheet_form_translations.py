#!/usr/bin/env python3
"""
Seed script to add form_submit translation key to provider_page namespace for all 34 languages.
"""

import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@nevumo-postgres:5432/nevumo_leads")

TRANSLATIONS = [
    ("bg", "provider_page.form_submit", "Изпрати заявката"),
    ("cs", "provider_page.form_submit", "Odeslat žádost"),
    ("da", "provider_page.form_submit", "Send anmodningen"),
    ("de", "provider_page.form_submit", "Anfrage senden"),
    ("el", "provider_page.form_submit", "Αποστολή αιτήματος"),
    ("en", "provider_page.form_submit", "Submit request"),
    ("es", "provider_page.form_submit", "Enviar solicitud"),
    ("et", "provider_page.form_submit", "Saada taotlus"),
    ("fi", "provider_page.form_submit", "Lähetä pyyntö"),
    ("fr", "provider_page.form_submit", "Envoyer la demande"),
    ("ga", "provider_page.form_submit", "Seol an t-iarratas"),
    ("hr", "provider_page.form_submit", "Pošalji zahtjev"),
    ("hu", "provider_page.form_submit", "Kérelem elküldése"),
    ("is", "provider_page.form_submit", "Senda beiðni"),
    ("it", "provider_page.form_submit", "Invia richiesta"),
    ("lb", "provider_page.form_submit", "Ufro schécken"),
    ("lt", "provider_page.form_submit", "Siųsti užklausą"),
    ("lv", "provider_page.form_submit", "Nosūtīt pieprasījumu"),
    ("mk", "provider_page.form_submit", "Испрати барање"),
    ("mt", "provider_page.form_submit", "Ibgħat it-talba"),
    ("nl", "provider_page.form_submit", "Aanvraag versturen"),
    ("no", "provider_page.form_submit", "Send forespørsel"),
    ("pl", "provider_page.form_submit", "Wyślij zapytanie"),
    ("pt", "provider_page.form_submit", "Enviar solicitação"),
    ("pt-PT", "provider_page.form_submit", "Enviar pedido"),
    ("ro", "provider_page.form_submit", "Trimite cererea"),
    ("ru", "provider_page.form_submit", "Отправить заявку"),
    ("sk", "provider_page.form_submit", "Odoslať žiadosť"),
    ("sl", "provider_page.form_submit", "Pošlji zahtevo"),
    ("sq", "provider_page.form_submit", "Dërgo kërkesën"),
    ("sr", "provider_page.form_submit", "Pošalji zahtev"),
    ("sv", "provider_page.form_submit", "Skicka förfrågan"),
    ("tr", "provider_page.form_submit", "Talebi gönder"),
    ("uk", "provider_page.form_submit", "Надіслати заявку")
]

def seed_form_submit_translations():
    """Insert form_submit translations for all languages."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    for lang, key, value in TRANSLATIONS:
        cursor.execute("""
            INSERT INTO translations (lang, key, value)
            VALUES (%s, %s, %s)
            ON CONFLICT (lang, key) 
            DO UPDATE SET value = EXCLUDED.value
        """, (lang, key, value))
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✓ Added form_submit translations for {len(TRANSLATIONS)} languages")

if __name__ == "__main__":
    seed_form_submit_translations()
