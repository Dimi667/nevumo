#!/usr/bin/env python3
"""
Seed QR slogan translations for all 32 supported languages.
Run this script to add QR slogan translations to the database.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import from the app
sys.path.append(str(Path(__file__).parent))

from sqlalchemy.orm import Session
from database import SessionLocal
from i18n import upsert_translation_values

# QR slogan translations for all 32 supported languages
QR_SLOGAN_TRANSLATIONS = {
    "bg": "Пусни заявка за 30 сек!",
    "en": "Send a request in 30 sec!",
    "de": "Anfrage in 30 Sek senden!",
    "fr": "Envoyez une demande en 30 s !",
    "es": "Envía una solicitud en 30 s!",
    "it": "Invia una richiesta in 30 sec!",
    "pt": "Envie um pedido em 30 seg!",
    "pt-PT": "Envie um pedido em 30 seg!",
    "sv": "Skicka en förfrågan på 30 sek!",
    "no": "Send en forespørsel på 30 sek!",
    "da": "Send en anmodning på 30 sek!",
    "fi": "Lähetä pyyntö 30 sekunnissa!",
    "et": "Saada päring 30 sek!",
    "lt": "Pateik užklausą per 30 sek!",
    "lv": "Nosūti pieprasījumu 30 sek!",
    "cs": "Odešli žádost do 30 sek!",
    "sk": "Odošli žiadosť do 30 sek!",
    "pl": "Wyślij zapytanie w 30 sek!",
    "hu": "Küldj kérést 30 mp alatt!",
    "ro": "Trimite cererea în 30 sec!",
    "hr": "Pošalji zahtjev u 30 sek!",
    "sl": "Pošlji zahtevo v 30 sek!",
    "sr": "Pošalji zahtev u 30 sek!",
    "mk": "Испрати барање за 30 сек!",
    "el": "Στείλτε αίτημα σε 30 δευτ!",
    "tr": "30 saniyede talep gönder!",
    "sq": "Dërgo kërkesë në 30 sek!",
    "ga": "Seol iarratas i 30 soic!",
    "mt": "Ibgħat talba fi 30 sek!",
    "nl": "Stuur een aanvraag in 30 sec!"
}


def seed_qr_slogan_translations():
    """Seed QR slogan translations to the database."""
    db = SessionLocal()
    try:
        print("Seeding QR slogan translations...")
        
        # Insert QR slogan translations
        upsert_translation_values(
            db, 
            key="qr_slogan_submit_request", 
            translations=QR_SLOGAN_TRANSLATIONS
        )
        
        db.commit()
        print(f"✅ Successfully seeded {len(QR_SLOGAN_TRANSLATIONS)} QR slogan translations")
        print("📝 Translation key: qr_slogan_submit_request")
        
        # Print sample translations for verification
        print("\n📋 Sample translations:")
        sample_langs = ["bg", "en", "de", "fr", "es"]
        for lang in sample_langs:
            print(f"  {lang}: {QR_SLOGAN_TRANSLATIONS[lang]}")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding translations: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_qr_slogan_translations()
