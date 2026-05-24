#!/usr/bin/env python3
"""
Seed status_cancelled translations.
"""

from sqlalchemy import text
from apps.api.database import engine

LANGS = ['en', 'bg', 'cs', 'da', 'de', 'el', 'es', 'et', 'fi', 'fr', 'ga', 'hr', 'hu', 'is', 'it', 'lb', 'lt', 'lv', 'mk', 'mt', 'nl', 'no', 'pl', 'pt', 'pt-PT', 'ro', 'ru', 'sk', 'sl', 'sq', 'sr', 'sv', 'tr', 'uk']

translations = [
    'Cancelled', 'Отказан', 'Zrušeno', 'Annulleret', 'Storniert', 'Ακυρώθηκε', 'Cancelado', 'Tühistatud',
    'Peruttu', 'Annulé', 'Cealaithe', 'Otkazano', 'Törölve', 'Afturkallað', 'Annullato', 'Ofgesot',
    'Atšaukta', 'Atcelts', 'Откажан', 'Mħassar', 'Geannuleerd', 'Avbrutt', 'Anulowano', 'Cancelado',
    'Cancelado', 'Anulat', 'Отменено', 'Zrušené', 'Preklicano', 'Anuluar', 'Otkazano', 'Avbruten',
    'İptal', 'Скасовано'
]

with engine.begin() as conn:
    for lang, value in zip(LANGS, translations):
        conn.execute(text("""
            INSERT INTO translations (lang, key, value)
            VALUES (:lang, :key, :value)
            ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
        """), {'lang': lang, 'key': 'provider_dashboard.status_cancelled', 'value': value})
    print(f'✅ Inserted {len(translations)} rows for status_cancelled')
