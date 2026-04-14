#!/usr/bin/env python3
"""
Дебъгване на FK грешки при category_translations и page_events
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

def debug_category_translations():
    print("=== category_translations ===")
    local_conn = psycopg2.connect(**LOCAL_DB)
    docker_conn = psycopg2.connect(**DOCKER_DB)
    
    local_cursor = local_conn.cursor()
    docker_cursor = docker_conn.cursor()
    
    # Взимаме ID-та от Docker
    docker_cursor.execute("SELECT id FROM category_translations;")
    docker_ids = set(row[0] for row in docker_cursor.fetchall())
    
    # Взимаме първия запис от локална база, който липсва в Docker
    local_cursor.execute("SELECT * FROM category_translations ORDER BY id;")
    columns = [desc[0] for desc in local_cursor.description]
    
    for record in local_cursor.fetchall():
        record_dict = dict(zip(columns, record))
        record_id = record_dict['id']
        if record_id not in docker_ids:
            print(f"Опит за вмъкване на ID {record_id}: {record_dict}")
            try:
                insert_query = f"""
                    INSERT INTO category_translations ({', '.join(columns)})
                    VALUES ({', '.join(['%s'] * len(columns))})
                """
                docker_cursor.execute(insert_query, record)
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
    print()


def debug_page_events():
    print("=== page_events ===")
    local_conn = psycopg2.connect(**LOCAL_DB)
    docker_conn = psycopg2.connect(**DOCKER_DB)
    
    local_cursor = local_conn.cursor()
    docker_cursor = docker_conn.cursor()
    
    # Взимаме ID-та от Docker
    docker_cursor.execute("SELECT id FROM page_events;")
    docker_ids = set(row[0] for row in docker_cursor.fetchall())
    
    # Взимаме първия запис от локална база, който липсва в Docker
    local_cursor.execute("SELECT * FROM page_events ORDER BY id LIMIT 1;")
    columns = [desc[0] for desc in local_cursor.description]
    
    for record in local_cursor.fetchall():
        record_dict = dict(zip(columns, record))
        record_id = record_dict['id']
        if record_id not in docker_ids:
            print(f"Опит за вмъкване на ID {record_id}: {record_dict}")
            try:
                insert_query = f"""
                    INSERT INTO page_events ({', '.join(columns)})
                    VALUES ({', '.join(['%s'] * len(columns))})
                """
                docker_cursor.execute(insert_query, record)
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
    print()


if __name__ == "__main__":
    debug_category_translations()
    debug_page_events()
