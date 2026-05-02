#!/usr/bin/env python3
"""Check Norwegian (no) and Oslo data in database."""

import psycopg2
from psycopg2 import sql

# Database connection (PostgreSQL in Docker on port 5433)
DATABASE_URL = "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads"

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
cursor = conn.cursor()

print("=" * 80)
print("1. ПРОВЕРКА НА СХЕМАТА НА TRANSLATIONS ТАБЛИЦА")
print("=" * 80)

query3 = """
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'translations' 
ORDER BY ordinal_position;
"""

cursor.execute(query3)
results = cursor.fetchall()
print("Колони на translations:")
for row in results:
    print(f"  {row[0]}: {row[1]}")

print("\n" + "=" * 80)
print("2. ПРОВЕРКА НА СХЕМАТА НА LOCATION_TRANSLATIONS ТАБЛИЦА")
print("=" * 80)

query4 = """
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'location_translations' 
ORDER BY ordinal_position;
"""

cursor.execute(query4)
results = cursor.fetchall()
print("Колони на location_translations:")
for row in results:
    print(f"  {row[0]}: {row[1]}")

print("\n" + "=" * 80)
print("3. ПРОВЕРКА НА TRANSLATIONS ТАБЛИЦА - faq_cleaning_ ключове за no")
print("=" * 80)

# Use correct column name based on schema (no namespace column)
query1 = """
SELECT key, lang, value 
FROM translations 
WHERE lang = 'no' 
  AND key LIKE 'faq_cleaning_%'
ORDER BY key;
"""

cursor.execute(query1)
results = cursor.fetchall()

if results:
    print(f"Намерени {len(results)} записа:")
    for row in results:
        print(f"  Key: {row[0]}, Lang: {row[1]}")
        print(f"  Value: {row[2][:100] if row[2] else 'NULL'}...")
        print()
else:
    print("Няма намерени записи за faq_cleaning_ с lang='no'")

print("\n" + "=" * 80)
print("4. ПРОВЕРКА НА LOCATION_TRANSLATIONS ТАБЛИЦА - Oslo")
print("=" * 80)

# location_translations has: id, location_id, lang, city_name (no city_slug)
# Need to check city_name instead
query2 = """
SELECT * 
FROM location_translations 
WHERE city_name ILIKE 'oslo' 
  AND lang IN ('no', 'bg', 'en')
ORDER BY lang;
"""

cursor.execute(query2)
results = cursor.fetchall()

if results:
    # Get column names
    col_names = [desc[0] for desc in cursor.description]
    print(f"Колони: {col_names}")
    print(f"\nНамерени {len(results)} записа:")
    for row in results:
        print(f"  {dict(zip(col_names, row))}")
        print()
else:
    print("Няма намерени записи за Oslo с lang IN ('no', 'bg', 'en')")

print("\n" + "=" * 80)
print("5. ВСИЧКИ TRANSLATIONS ЗА NO")
print("=" * 80)

query5 = """
SELECT key, lang, value 
FROM translations 
WHERE lang = 'no' 
ORDER BY key
LIMIT 30;
"""

cursor.execute(query5)
results = cursor.fetchall()
print(f"Първите 30 записа (общо: {len(results)}):")
for row in results:
    print(f"  Key: {row[0]}, Value: {row[2][:80] if row[2] else 'NULL'}...")

print("\n" + "=" * 80)
print("6. ПРОВЕРКА ЗА ТАБЛИЦА CITIES/LOCATIONS")
print("=" * 80)

# Check if there's a cities or locations table
query6 = """
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND (table_name LIKE '%city%' OR table_name LIKE '%location%')
ORDER BY table_name;
"""

cursor.execute(query6)
results = cursor.fetchall()
print("Таблици, свързани с градове/локации:")
for row in results:
    print(f"  {row[0]}")

print("\n" + "=" * 80)
print("7. ПРОВЕРКА НА ВСИЧКИ ЗАПИСИ В LOCATION_TRANSLATIONS")
print("=" * 80)

query7 = """
SELECT COUNT(*) as total, lang 
FROM location_translations 
GROUP BY lang 
ORDER BY lang;
"""

cursor.execute(query7)
results = cursor.fetchall()
print("Брой записи по език в location_translations:")
for row in results:
    print(f"  Lang: {row[1]}, Count: {row[0]}")

print("\n" + "=" * 80)
print("8. ВСИЧКИ ГРАДОВЕ В LOCATION_TRANSLATIONS")
print("=" * 80)

query8 = """
SELECT DISTINCT city_name 
FROM location_translations 
ORDER BY city_name 
LIMIT 20;
"""

cursor.execute(query8)
results = cursor.fetchall()
print(f"Първите 20 уникални града:")
for row in results:
    print(f"  {row[0]}")

print("\n" + "=" * 80)
print("9. ПРОВЕРКА НА LOCATIONS ТАБЛИЦА - Oslo")
print("=" * 80)

# Check schema of locations table
query9_schema = """
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'locations' 
ORDER BY ordinal_position;
"""

cursor.execute(query9_schema)
results = cursor.fetchall()
print("Колони на locations:")
for row in results:
    print(f"  {row[0]}: {row[1]}")

print("\nПроверка за Oslo в locations:")
query9 = """
SELECT * 
FROM locations 
WHERE slug ILIKE 'oslo' 
   OR city ILIKE 'oslo'
   OR city_en ILIKE 'oslo'
LIMIT 5;
"""

cursor.execute(query9)
results = cursor.fetchall()
if results:
    col_names = [desc[0] for desc in cursor.description]
    print(f"Намерени {len(results)} записа:")
    for row in results:
        print(f"  {dict(zip(col_names, row))}")
else:
    print("Няма намерени записи за Oslo в locations таблицата")

print("\n" + "=" * 80)
print("10. ВСИЧКИ ЗАПИСИ В LOCATIONS")
print("=" * 80)

query10 = """
SELECT slug, city, city_en 
FROM locations 
ORDER BY slug;
"""

cursor.execute(query10)
results = cursor.fetchall()
print(f"Всички градове в locations (общо: {len(results)}):")
for row in results:
    print(f"  Slug: {row[0]}, City: {row[1]}, City_EN: {row[2]}")

cursor.close()
conn.close()
print("\n" + "=" * 80)
print("ПРОВЕРКАТА ЗАВЪРШЕНА")
print("=" * 80)
