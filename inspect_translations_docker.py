#!/usr/bin/env python3
"""
Финална инспекция на translations таблицата в Docker базата
"""

import psycopg2

DOCKER_DB = {
    "host": "localhost",
    "port": 5433,
    "user": "nevumo",
    "password": "nevumo",
    "database": "nevumo_leads"
}


def inspect_translations():
    conn = psycopg2.connect(**DOCKER_DB)
    cursor = conn.cursor()
    
    print("=" * 80)
    print("ФИНАЛНА ИНСПЕКЦИЯ НА TRANSLATIONS В DOCKER БАЗАТА")
    print("=" * 80)
    print()
    
    # 1. 10 произволни записа за lang='bg'
    print("1. 10 произволни записа за lang='bg':")
    print("-" * 80)
    cursor.execute("SELECT id, key, value FROM translations WHERE lang = 'bg' ORDER BY RANDOM() LIMIT 10;")
    rows = cursor.fetchall()
    for row in rows:
        print(f"  ID: {row[0]}, Key: {row[1]}, Value: {row[2]}")
    print()
    
    # 2. Брой записи с точка (.) и без точка в ключа
    print("2. Анализ на формата на ключовете:")
    print("-" * 80)
    cursor.execute("SELECT COUNT(*) FROM translations WHERE key LIKE '%.%';")
    with_dot = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM translations WHERE key NOT LIKE '%.%';")
    without_dot = cursor.fetchone()[0]
    
    total = with_dot + without_dot
    print(f"  Общо записи: {total}")
    print(f"  С точка (.) в ключа (нов формат): {with_dot} ({with_dot/total*100:.1f}%)")
    print(f"  Без точка в ключа (стар формат): {without_dot} ({without_dot/total*100:.1f}%)")
    print()
    
    # 3. Проверка за namespace auth и homepage
    print("3. Анализ на namespace-и:")
    print("-" * 80)
    
    cursor.execute("SELECT COUNT(*) FROM translations WHERE key LIKE 'auth.%';")
    auth_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM translations WHERE key LIKE 'homepage.%';")
    homepage_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM translations WHERE key LIKE 'auth%';")
    auth_total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM translations WHERE key LIKE 'homepage%';")
    homepage_total = cursor.fetchone()[0]
    
    print(f"  auth.* (с префикс): {auth_count}")
    print(f"  auth* (общо): {auth_total}")
    print(f"  homepage.* (с префикс): {homepage_count}")
    print(f"  homepage* (общо): {homepage_total}")
    print()
    
    # 4. Примерни ключове за auth и homepage
    print("4. Примерни ключове за auth namespace:")
    print("-" * 80)
    cursor.execute("SELECT DISTINCT key FROM translations WHERE key LIKE 'auth%' ORDER BY key LIMIT 10;")
    auth_keys = cursor.fetchall()
    for key in auth_keys:
        print(f"  {key[0]}")
    print()
    
    print("5. Примерни ключове за homepage namespace:")
    print("-" * 80)
    cursor.execute("SELECT DISTINCT key FROM translations WHERE key LIKE 'homepage%' ORDER BY key LIMIT 10;")
    homepage_keys = cursor.fetchall()
    for key in homepage_keys:
        print(f"  {key[0]}")
    print()
    
    # 6. Проверка за дубликати - стари vs нови ключове
    print("6. Проверка за дубликати (стар vs нов формат):")
    print("-" * 80)
    
    # auth namespace
    cursor.execute("""
        SELECT key, COUNT(*) as cnt
        FROM translations
        WHERE key LIKE 'auth%' AND lang = 'en'
        GROUP BY key
        HAVING COUNT(*) > 1
        LIMIT 5;
    """)
    auth_duplicates = cursor.fetchall()
    
    if auth_duplicates:
        print("  Дубликати в auth namespace:")
        for dup in auth_duplicates:
            print(f"    {dup[0]}: {dup[1]} записа")
    else:
        print("  Няма дубликати в auth namespace")
    
    # homepage namespace
    cursor.execute("""
        SELECT key, COUNT(*) as cnt
        FROM translations
        WHERE key LIKE 'homepage%' AND lang = 'en'
        GROUP BY key
        HAVING COUNT(*) > 1
        LIMIT 5;
    """)
    homepage_duplicates = cursor.fetchall()
    
    if homepage_duplicates:
        print("  Дубликати в homepage namespace:")
        for dup in homepage_duplicates:
            print(f"    {dup[0]}: {dup[1]} записа")
    else:
        print("  Няма дубликати в homepage namespace")
    
    print()
    
    # 7. Проверка дали новите ключове са активни
    print("7. Проверка дали новата i18n архитектура е активна:")
    print("-" * 80)
    
    cursor.execute("""
        SELECT key, value
        FROM translations
        WHERE key LIKE 'homepage.%' AND lang = 'en'
        LIMIT 5;
    """)
    homepage_samples = cursor.fetchall()
    
    if homepage_samples:
        print("  Новите homepage.* ключове са активни:")
        for sample in homepage_samples:
            print(f"    {sample[0]}: {sample[1]}")
    else:
        print("  Няма homepage.* ключове")
    
    cursor.execute("""
        SELECT key, value
        FROM translations
        WHERE key LIKE 'auth.%' AND lang = 'en'
        LIMIT 5;
    """)
    auth_samples = cursor.fetchall()
    
    if auth_samples:
        print("  Новите auth.* ключове са активни:")
        for sample in auth_samples:
            print(f"    {sample[0]}: {sample[1]}")
    else:
        print("  Няма auth.* ключове")
    
    print()
    
    cursor.close()
    conn.close()
    
    print("=" * 80)
    print("ИНСПЕКЦИЯТА ЗАВЪРШЕНА")
    print("=" * 80)


if __name__ == "__main__":
    inspect_translations()
