import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from apps.api.database import engine

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT key, COUNT(DISTINCT lang) as lang_count,
               MAX(CASE WHEN lang='bg' THEN value END) as bg_value,
               MAX(CASE WHEN lang='en' THEN value END) as en_value
        FROM translations
        WHERE key LIKE 'provider_dashboard.gallery%'
        GROUP BY key
        ORDER BY key
    """))
    rows = result.fetchall()
    print(f'=== GALLERY KEYS IN DB: {len(rows)} ===')
    for r in rows:
        print(f'  {r[0]} | langs={r[1]}/34 | bg={r[2]} | en={r[3]}')
    if not rows:
        print('NO gallery keys found in DB!')
