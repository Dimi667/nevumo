import os
import psycopg2

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()
cur.execute("""
    SELECT key, COUNT(DISTINCT lang) as lang_count,
           MAX(CASE WHEN lang='bg' THEN value END) as bg_value,
           MAX(CASE WHEN lang='en' THEN value END) as en_value
    FROM translations
    WHERE key LIKE 'provider_dashboard.gallery%'
    GROUP BY key
    ORDER BY key
""")
rows = cur.fetchall()
print(f'=== GALLERY KEYS IN DB: {len(rows)} ===')
for r in rows:
    print(f'  {r[0]} | langs={r[1]}/34 | bg={r[2]} | en={r[3]}')
if not rows:
    print('NO gallery keys found in DB!')
cur.close()
conn.close()
