#!/usr/bin/env python3
"""Check database for Fixly references in claim translations."""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection string
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")

print("Connecting to database...")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor(cursor_factory=RealDictCursor)

print("\n=== Query 1: Translation keys containing 'fixly' (case-insensitive) ===")
cursor.execute("""
    SELECT lang, key, value
    FROM translations
    WHERE namespace = 'claim'
    AND value ILIKE '%fixly%'
    ORDER BY key, lang;
""")
results = cursor.fetchall()
if results:
    for row in results:
        print(f"Lang: {row['lang']}, Key: {row['key']}, Value: {row['value']}")
else:
    print("No results found")

print("\n=== Query 2: VS section translation keys for Polish (pl) ===")
cursor.execute("""
    SELECT lang, key, value
    FROM translations
    WHERE namespace = 'claim'
    AND key IN ('vs_bad_1', 'vs_bad_2', 'vs_good_1', 'vs_good_2', 'vs_title', 'vs_subtitle', 'vs_header', 'vs_left_title', 'vs_right_title')
    AND lang = 'pl'
    ORDER BY key;
""")
results = cursor.fetchall()
if results:
    for row in results:
        print(f"Lang: {row['lang']}, Key: {row['key']}, Value: {row['value']}")
else:
    print("No results found")

print("\n=== Query 3: All VS section keys across all languages ===")
cursor.execute("""
    SELECT lang, key, value
    FROM translations
    WHERE namespace = 'claim'
    AND key IN ('vs_bad_1', 'vs_bad_2', 'vs_good_1', 'vs_good_2', 'vs_title', 'vs_subtitle', 'vs_header', 'vs_left_title', 'vs_right_title')
    ORDER BY key, lang;
""")
results = cursor.fetchall()
if results:
    for row in results:
        print(f"Lang: {row['lang']}, Key: {row['key']}, Value: {row['value']}")
else:
    print("No results found")

cursor.close()
conn.close()
print("\nDatabase connection closed.")
