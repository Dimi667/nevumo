#!/usr/bin/env python3
"""
Restore status_label_cancelled_by_provider and status_label_cancelled_by_client 
translations from backup with original values.
"""

from sqlalchemy import text
from apps.api.database import engine

LANGS = ['en', 'bg', 'cs', 'da', 'de', 'el', 'es', 'et', 'fi', 'fr', 'ga', 'hr', 'hu', 'is', 'it', 'lb', 'lt', 'lv', 'mk', 'mt', 'nl', 'no', 'pl', 'pt', 'pt-PT', 'ro', 'ru', 'sk', 'sl', 'sq', 'sr', 'sv', 'tr', 'uk']

provider_cancelled = [
    'Cancelled', 'Отказана', 'Zrušeno', 'Annulleret', 'Storniert', 'Ακυρώθηκε', 'Cancelada', 'Tühistatud',
    'Peruutettu', 'Annulée', 'Cealaithe', 'Otkazano', 'Lemondva', 'Hætt við', 'Annullata', 'Annuléiert',
    'Atšaukta', 'Atcelts', 'Откажана', 'Ikkanċellata', 'Geannuleerd', 'Avbestilt', 'Anulowane', 'Cancelada',
    'Cancelada', 'Anulată', 'Отменена', 'Zrušené', 'Preklicano', 'Anuluar', 'Отказано', 'Avbokad',
    'İptal edildi', 'Скасовано'
]

client_cancelled = [
    'Client cancelled', 'Клиентът отказа', 'Klient zrušil', 'Kunden annullerede', 'Kunde hat storniert', 'Ο πελάτης ακύρωσε', 'El cliente canceló', 'Klient tühistas',
    'Asiakas peruutti', 'Le client a annulé', 'Dhiúltaigh an cliant', 'Klijent je otkazao', 'Az ügyfél lemondta', 'Viðskiptavinurinn hætti við', 'Il cliente ha annullato', 'De Client huet annuléiert',
    'Klientas atšaukė', 'Klients atcēla', 'Клиентот откажа', 'Il-klijent ikkanċella', 'Klant heeft geannuleerd', 'Kunden avbestilte', 'Klient anulował', 'O cliente cancelou',
    'O cliente cancelou', 'Clientul a anulat', 'Клиент отменил', 'Klient zrušil', 'Stranka je preklicala', 'Klienti anuloi', 'Клијент је отказао', 'Kunden avbokade',
    'Müşteri iptal etti', 'Клієнт скасував'
]

with engine.begin() as conn:
    for lang, value in zip(LANGS, provider_cancelled):
        conn.execute(text("""
            INSERT INTO translations (lang, key, value)
            VALUES (:lang, :key, :value)
            ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
        """), {'lang': lang, 'key': 'provider_dashboard.status_label_cancelled_by_provider', 'value': value})
    
    for lang, value in zip(LANGS, client_cancelled):
        conn.execute(text("""
            INSERT INTO translations (lang, key, value)
            VALUES (:lang, :key, :value)
            ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
        """), {'lang': lang, 'key': 'provider_dashboard.status_label_cancelled_by_client', 'value': value})
    
    print(f'✅ Restored {len(LANGS)} rows for status_label_cancelled_by_provider')
    print(f'✅ Restored {len(LANGS)} rows for status_label_cancelled_by_client')
