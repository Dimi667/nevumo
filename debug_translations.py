#!/usr/bin/env python3
"""
Дебъгване на translations грешки
"""

import psycopg2

DOCKER_DB = {
    "host": "localhost",
    "port": 5433,
    "user": "nevumo",
    "password": "nevumo",
    "database": "nevumo_leads"
}

LOCAL_DB = {
    "host": "localhost",
    "port": 5432,
    "user": "nevumo",
    "password": "nevumo",
    "database": "nevumo_leads"
}

def debug_first_error():
    local_conn = psycopg2.connect(**LOCAL_DB)
    docker_conn = psycopg2.connect(**DOCKER_DB)
    
    local_cursor = local_conn.cursor()
    docker_cursor = docker_conn.cursor()
    
    # Взимаме всички (lang, key) от Docker
    docker_cursor.execute("SELECT lang, key FROM translations;")
    docker_lang_keys = set((row[0], row[1]) for row in docker_cursor.fetchall())
    
    # Взимаме първия запис от локална база, който липсва в Docker по (lang, key)
    local_cursor.execute("SELECT id, lang, key, value FROM translations ORDER BY id;")
    for record in local_cursor.fetchall():
        record_id, lang, key, value = record
        if (lang, key) not in docker_lang_keys:
            print(f"Опит за вмъкване на ID {record_id}: lang={lang}, key={key}")
            try:
                insert_query = """
                    INSERT INTO translations (id, lang, key, value)
                    VALUES (%s, %s, %s, %s)
                """
                docker_cursor.execute(insert_query, (record_id, lang, key, value))
                docker_conn.commit()
                print(f"Успех!")
                break
            except Exception as e:
                print(f"Грешка: {e}")
                break
    
    local_cursor.close()
    local_conn.close()
    docker_cursor.close()
    docker_conn.close()

if __name__ == "__main__":
    debug_first_error()
