#!/usr/bin/env python3
"""
Script to update category.get_offers_btn with translations from category.form_btn
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
    
    # Translation data - copied from category.form_btn
    translations = {
        'category.get_offers_btn': {
            'bg': "Изпрати заявка до всички",
            'cs': "Odeslat žádost všem",
            'da': "Send anmodning til alle",
            'de': "Anfrage an alle senden",
            'el': "Αποστολή αιτήματος σε όλους",
            'en': "Send request to all",
            'es': "Enviar solicitud a todos",
            'et': "Saada päring kõigile",
            'fi': "Lähetä pyyntö kaikille",
            'fr': "Envoyer une demande à tous",
            'ga': "Seol iarratas chuig cách",
            'hr': "Pošalji zahtjev svima",
            'hu': "Kérés küldése mindenkinek",
            'is': "Senda beiðni til allra",
            'it': "Invia richiesta a tutti",
            'lb': "Ufro un all schécken",
            'lt': "Siųsti užklausą visiems",
            'lv': "Nosūtīt pieprasījumu visiem",
            'mk': "Испрати барање до сите",
            'mt': "Ibgħat talba lil kulħadd",
            'nl': "Stuur aanvraag naar iedereen",
            'no': "Send forespørsel til alle",
            'pl': "Wyślij zapytanie do wszystkich",
            'pt': "Enviar solicitação a todos",
            'pt-PT': "Enviar pedido a todos",
            'ro': "Trimite cererea către toți",
            'ru': "Отправить заявку всем",
            'sk': "Odoslať požiadavku všetkým",
            'sl': "Pošlji povpraševanje vsem",
            'sq': "Dërgo kërkesë te të gjithë",
            'sr': "Пошаљите захтев свима",
            'sv': "Skicka förfrågan till alla",
            'tr': "Talebi herkese gönder",
            'uk': "Надіслати заявку всім"
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
