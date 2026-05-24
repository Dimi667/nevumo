#!/usr/bin/env python3
"""
Seed status_label_cancelled_by_client and status_label_cancelled_by_provider translations.
"""

from sqlalchemy import text
from apps.api.database import engine

LANGS = ['en', 'bg', 'cs', 'da', 'de', 'el', 'es', 'et', 'fi', 'fr', 'ga', 'hr', 'hu', 'is', 'it', 'lb', 'lt', 'lv', 'mk', 'mt', 'nl', 'no', 'pl', 'pt', 'pt-PT', 'ro', 'ru', 'sk', 'sl', 'sq', 'sr', 'sv', 'tr', 'uk']

client_cancelled = [
    'Client cancelled', 'Отказан от клиента', 'Zrušeno klientem', 'Annulleret af kunden', 'Vom Kunden storniert', 'Ακυρώθηκε από τον πελάτη', 'Cancelado por el cliente', 'Kliendi poolt tühistatud',
    'Asiakkaan peruma', 'Annulé par le client', 'Cealaithe ag an cliant', 'Otkazano od strane klijenta', 'Ügyfél által törölve', 'Afturkallað af viðskiptavini', 'Annullato dal cliente', 'Vum Client ofgesot',
    'Atšaukta kliento', 'Atcelts no klienta', 'Откажан од клиентот', 'Mħassar mill-klijent', 'Geannuleerd door klant', 'Avbrutt av kunde', 'Anulowane przez klienta', 'Cancelado pelo cliente',
    'Cancelado pelo cliente', 'Anulat de client', 'Отменено клиентом', 'Zrušené klientom', 'Preklicano od stranke', 'Anuluar nga klienti', 'Otkazano od strane klijenta', 'Avbruten av kund',
    'Müşteri tarafından iptal', 'Скасовано клієнтом'
]

provider_cancelled = [
    'Cancelled', 'Отказан', 'Zrušeno', 'Annulleret', 'Storniert', 'Ακυρώθηκε', 'Cancelado', 'Tühistatud',
    'Peruttu', 'Annulé', 'Cealaithe', 'Otkazano', 'Törölve', 'Afturkallað', 'Annullato', 'Ofgesot',
    'Atšaukta', 'Atcelts', 'Откажан', 'Mħassar', 'Geannuleerd', 'Avbrutt', 'Anulowano', 'Cancelado',
    'Cancelado', 'Anulat', 'Отменено', 'Zrušené', 'Preklicano', 'Anuluar', 'Otkazano', 'Avbruten',
    'İptal', 'Скасовано'
]

with engine.begin() as conn:
    for lang, value in zip(LANGS, client_cancelled):
        conn.execute(text("""
            INSERT INTO translations (lang, key, value)
            VALUES (:lang, :key, :value)
            ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
        """), {'lang': lang, 'key': 'provider_dashboard.status_label_cancelled_by_client', 'value': value})
    
    for lang, value in zip(LANGS, provider_cancelled):
        conn.execute(text("""
            INSERT INTO translations (lang, key, value)
            VALUES (:lang, :key, :value)
            ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
        """), {'lang': lang, 'key': 'provider_dashboard.status_label_cancelled_by_provider', 'value': value})
    
    print(f'✅ Inserted {len(LANGS)} rows for status_label_cancelled_by_client')
    print(f'✅ Inserted {len(LANGS)} rows for status_label_cancelled_by_provider')
