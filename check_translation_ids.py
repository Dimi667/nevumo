#!/usr/bin/env python3
"""
Проверка защо translations не се вмъкнаха
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

def check_translation_ids():
    local_conn = psycopg2.connect(**LOCAL_DB)
    docker_conn = psycopg2.connect(**DOCKER_DB)
    
    local_cursor = local_conn.cursor()
    docker_cursor = docker_conn.cursor()
    
    # ID-та в локална база
    local_cursor.execute("SELECT id FROM translations ORDER BY id;")
    local_ids = set(row[0] for row in local_cursor.fetchall())
    
    # ID-та в Docker база
    docker_cursor.execute("SELECT id FROM translations ORDER BY id;")
    docker_ids = set(row[0] for row in docker_cursor.fetchall())
    
    print(f"Локална база: {len(local_ids)} translations")
    print(f"Docker база: {len(docker_ids)} translations")
    print()
    
    # Пресечни точки
    common_ids = local_ids & docker_ids
    only_local = local_ids - docker_ids
    only_docker = docker_ids - local_ids
    
    print(f"Общи ID-та: {len(common_ids)}")
    print(f"Само в локална: {len(only_local)}")
    print(f"Само в Docker: {len(only_docker)}")
    print()
    
    if only_local:
        print(f"Пример ID-та само в локална: {list(only_local)[:5]}")
    if only_docker:
        print(f"Пример ID-та само в Docker: {list(only_docker)[:5]}")
    
    # Проверка за конфликти по (lang, key)
    local_cursor.execute("SELECT lang, key FROM translations;")
    local_lang_keys = set((row[0], row[1]) for row in local_cursor.fetchall())
    
    docker_cursor.execute("SELECT lang, key FROM translations;")
    docker_lang_keys = set((row[0], row[1]) for row in docker_cursor.fetchall())
    
    print()
    print(f"Уникални (lang, key) в локална: {len(local_lang_keys)}")
    print(f"Уникални (lang, key) в Docker: {len(docker_lang_keys)}")
    
    common_lang_keys = local_lang_keys & docker_lang_keys
    only_local_lang_keys = local_lang_keys - docker_lang_keys
    only_docker_lang_keys = docker_lang_keys - local_lang_keys
    
    print(f"Общи (lang, key): {len(common_lang_keys)}")
    print(f"Само в локална: {len(only_local_lang_keys)}")
    print(f"Само в Docker: {len(only_docker_lang_keys)}")
    
    local_cursor.close()
    docker_cursor.close()
    local_conn.close()
    docker_conn.close()

if __name__ == "__main__":
    check_translation_ids()
