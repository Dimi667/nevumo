#!/usr/bin/env python3
"""
Script to upsert translation keys for category.send_request_to_provider
"""

import os
import psycopg2
from psycopg2 import sql

def main():
    # Database connection
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return
    
    # Translation data
    translations = {
        'category.send_request_to_provider': {
            "bg": "Изпрати заявка до",
            "cs": "Odeslat žádost pro",
            "da": "Send anmodning til",
            "de": "Anfrage senden an",
            "el": "Αποστολή αιτήματος σε",
            "en": "Send request to",
            "es": "Enviar solicitud a",
            "et": "Saada taotlus:",
            "fi": "Lähetä pyyntö:",
            "fr": "Envoyer une demande à",
            "ga": "Seol iarratas chuig",
            "hr": "Pošalji zahtjev za",
            "hu": "Kérelem küldése:",
            "is": "Senda beiðni til",
            "it": "Invia richiesta a",
            "lb": "Ufro schécken un",
            "lt": "Siųsti užklausą:",
            "lv": "Nosūtīt pieprasījumu:",
            "mk": "Испрати барање до",
            "mt": "Ibgħat talba lil",
            "nl": "Aanvraag sturen naar",
            "no": "Send forespørsel til",
            "pl": "Wyślij zapytanie do",
            "pt": "Enviar solicitação para",
            "pt-PT": "Enviar pedido para",
            "ro": "Trimite cererea către",
            "ru": "Отправить заявку:",
            "sk": "Odoslať žiadosť pre",
            "sl": "Pošlji zahtevo za",
            "sq": "Dërgo kërkesë tek",
            "sr": "Pošalji zahtev za",
            "sv": "Skicka förfrågan till",
            "tr": "Talep gönder:",
            "uk": "Надіслати заявку:"
        }
    }
    
    try:
        # Connect to database
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # Prepare upsert query
        upsert_query = sql.SQL("""
            INSERT INTO translations (lang, key, value)
            VALUES (%s, %s, %s)
            ON CONFLICT (lang, key) 
            DO UPDATE SET 
                value = EXCLUDED.value
        """)
        
        rows_upserted = 0
        
        # Execute upserts
        for key, lang_values in translations.items():
            for lang, value in lang_values.items():
                cursor.execute(upsert_query, (lang, key, value))
                rows_upserted += 1
        
        # Commit transaction
        conn.commit()
        
        print(f"Successfully upserted {rows_upserted} translation rows")
        
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
