#!/usr/bin/env python3
"""
Update status_cancelled translations with user-provided values.
"""

from sqlalchemy import text
from apps.api.database import engine

LANGS = ['en', 'bg', 'cs', 'da', 'de', 'el', 'es', 'et', 'fi', 'fr', 'ga', 'hr', 'hu', 'is', 'it', 'lb', 'lt', 'lv', 'mk', 'mt', 'nl', 'no', 'pl', 'pt', 'pt-PT', 'ro', 'ru', 'sk', 'sl', 'sq', 'sr', 'sv', 'tr', 'uk']

translations = [
    'Rejected', 'Отказана', 'Odmítnuto', 'Afvist', 'Abgelehnt', 'Απορρίφθηκε', 'Rechazada', 'Tagasi lükatud',
    'Hylätty', 'Refusée', 'Diúltaithe', 'Odbijeno', 'Elutasítva', 'Hafnað', 'Rifiutata', 'Ofgeleent',
    'Atmesta', 'Noraidīts', 'Одбиена', 'Miċħud', 'Afgewezen', 'Avvist', 'Odrzucona', 'Rejeitada',
    'Rejeitada', 'Respinsă', 'Отклонена', 'Zamietnuté', 'Zavrnjeno', 'Refuzuar', 'Odbijena', 'Avvisad',
    'Reddedildi', 'Відхилена'
]

with engine.begin() as conn:
    for lang, value in zip(LANGS, translations):
        conn.execute(text("""
            INSERT INTO translations (lang, key, value)
            VALUES (:lang, :key, :value)
            ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
        """), {'lang': lang, 'key': 'provider_dashboard.status_cancelled', 'value': value})
    print(f'✅ Updated {len(translations)} rows for status_cancelled')
