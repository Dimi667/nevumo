#!/usr/bin/env python3
"""
Проверка на структурата на translations таблицата
"""

import psycopg2

LOCAL_DB = {
    "host": "localhost",
    "port": 5432,
    "user": "nevumo",
    "password": "nevumo",
    "database": "nevumo_leads"
}

DOCKER_DB = {
    "host": "localhost",
    "port": 5433,
    "user": "nevumo",
    "password": "nevumo",
    "database": "nevumo_leads"
}

def check_translations_structure():
    conn = psycopg2.connect(**LOCAL_DB)
    cursor = conn.cursor()
    
    # Колони
    cursor.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'translations'
        ORDER BY ordinal_position;
    """)
    columns = cursor.fetchall()
    
    print("Структура на translations таблицата:")
    print("=" * 60)
    for col in columns:
        print(f"  {col[0]}: {col[1]}")
    print()
    
    # Примерни записи от локална база
    cursor.execute("SELECT * FROM translations ORDER BY id LIMIT 5;")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    
    print("Примерни записи от ЛОКАЛНА база:")
    print("=" * 60)
    for row in rows:
        print(dict(zip(col_names, row)))
    print()
    
    cursor.close()
    conn.close()
    
    # Примерни записи от Docker база
    conn = psycopg2.connect(**DOCKER_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM translations ORDER BY id LIMIT 5;")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    
    print("Примерни записи от DOCKER база:")
    print("=" * 60)
    for row in rows:
        print(dict(zip(col_names, row)))
    print()
    
    cursor.close()
    conn.close()
    
    # Проверка за ключове с префикси
    conn = psycopg2.connect(**LOCAL_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT key FROM translations WHERE key LIKE '%.%' ORDER BY key LIMIT 20;")
    prefixed_keys = cursor.fetchall()
    
    print("Примерни ключове с префикси (локална):")
    print("=" * 60)
    for key in prefixed_keys:
        print(f"  {key[0]}")
    print()
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    check_translations_structure()
