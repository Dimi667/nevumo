#!/usr/bin/env python3
"""
Скрипт за интелигентно сливане на локална база в Docker база
"""

import psycopg2
from typing import List, Dict, Any
import json

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


def get_primary_key(conn, table: str) -> str:
    """Връща името на първичния ключ на таблицата"""
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT a.attname
        FROM pg_index i
        JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
        WHERE i.indrelid = '{table}'::regclass
        AND i.indisprimary;
    """)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return "id"


def get_table_columns(conn, table: str) -> List[str]:
    """Връща списък с колоните на таблицата"""
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{table}'
        ORDER BY ordinal_position;
    """)
    columns = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return columns


def get_missing_ids(table: str, pk: str) -> List[Any]:
    """Връща ID-тата на записите, които липсват в Docker базата"""
    try:
        # Локална база
        local_conn = psycopg2.connect(**LOCAL_DB)
        local_cursor = local_conn.cursor()
        local_cursor.execute(f"SELECT {pk} FROM {table} ORDER BY {pk};")
        local_ids = set(row[0] for row in local_cursor.fetchall())
        local_cursor.close()
        local_conn.close()
        
        # Docker база
        docker_conn = psycopg2.connect(**DOCKER_DB)
        docker_cursor = docker_conn.cursor()
        docker_cursor.execute(f"SELECT {pk} FROM {table} ORDER BY {pk};")
        docker_ids = set(row[0] for row in docker_cursor.fetchall())
        docker_cursor.close()
        docker_conn.close()
        
        # ID-та, които са в локална но липсват в Docker
        missing_in_docker = list(local_ids - docker_ids)
        return missing_in_docker
        
    except Exception as e:
        print(f"Грешка при таблица {table}: {e}")
        return []


def copy_records_to_docker(table: str, pk: str, missing_ids: List[Any]) -> int:
    """Копира липсващите записи от локална в Docker база"""
    if not missing_ids:
        return 0
    
    try:
        # Специална обработка за category_translations
        if table == "category_translations":
            return copy_category_translations(missing_ids)
        
        # Специална обработка за page_events
        if table == "page_events":
            return copy_page_events(missing_ids)
        
        # Взимане на колоните
        local_conn = psycopg2.connect(**LOCAL_DB)
        columns = get_table_columns(local_conn, table)
        local_conn.close()
        
        if not columns:
            return 0
        
        # Взимане на данните от локална база
        local_conn = psycopg2.connect(**LOCAL_DB)
        local_cursor = local_conn.cursor()
        
        placeholders = ', '.join(['%s'] * len(missing_ids))
        query = f"SELECT {', '.join(columns)} FROM {table} WHERE {pk} IN ({placeholders})"
        local_cursor.execute(query, missing_ids)
        rows = local_cursor.fetchall()
        local_cursor.close()
        local_conn.close()
        
        if not rows:
            return 0
        
        # Вмъкване в Docker база - отделна транзакция за всеки запис
        insert_query = f"""
            INSERT INTO {table} ({', '.join(columns)})
            VALUES ({', '.join(['%s'] * len(columns))})
        """
        
        inserted_count = 0
        error_count = 0
        
        for row in rows:
            try:
                docker_conn = psycopg2.connect(**DOCKER_DB)
                docker_cursor = docker_conn.cursor()
                docker_cursor.execute(insert_query, row)
                docker_conn.commit()
                docker_cursor.close()
                docker_conn.close()
                inserted_count += 1
            except Exception as e:
                error_count += 1
                # Не печатаме всяка грешка, само обобщение накрая
                pass
        
        if error_count > 0:
            print(f"  Успешно вмъкнати: {inserted_count}, Грешки: {error_count}")
        else:
            print(f"  Успешно вмъкнати: {inserted_count}")
        
        return inserted_count
        
    except Exception as e:
        print(f"Грешка при копиране на записи за {table}: {e}")
        return 0


def copy_category_translations(missing_ids: List[Any]) -> int:
    """Специална обработка за category_translations - проверка за уникален constraint"""
    import json
    
    try:
        local_conn = psycopg2.connect(**LOCAL_DB)
        docker_conn = psycopg2.connect(**DOCKER_DB)
        
        local_cursor = local_conn.cursor()
        docker_cursor = docker_conn.cursor()
        
        # Взимаме всички (category_id, lang) от Docker
        docker_cursor.execute("SELECT category_id, lang FROM category_translations;")
        docker_category_langs = set((row[0], row[1]) for row in docker_cursor.fetchall())
        
        # Взимане на данните от локална база
        placeholders = ', '.join(['%s'] * len(missing_ids))
        query = f"SELECT id, category_id, lang, name FROM category_translations WHERE id IN ({placeholders})"
        local_cursor.execute(query, missing_ids)
        rows = local_cursor.fetchall()
        
        insert_query = """
            INSERT INTO category_translations (id, category_id, lang, name)
            VALUES (%s, %s, %s, %s)
        """
        
        inserted_count = 0
        skipped_count = 0
        error_count = 0
        
        for row in rows:
            record_id, category_id, lang, name = row
            
            # Пропускаме, ако (category_id, lang) вече съществува в Docker
            if (category_id, lang) in docker_category_langs:
                skipped_count += 1
                continue
            
            try:
                temp_conn = psycopg2.connect(**DOCKER_DB)
                temp_cursor = temp_conn.cursor()
                temp_cursor.execute(insert_query, (record_id, category_id, lang, name))
                temp_conn.commit()
                temp_cursor.close()
                temp_conn.close()
                inserted_count += 1
            except Exception as e:
                error_count += 1
                pass
        
        local_cursor.close()
        local_conn.close()
        docker_cursor.close()
        docker_conn.close()
        
        print(f"  Успешно вмъкнати: {inserted_count}, Пропуснати: {skipped_count}, Грешки: {error_count}")
        return inserted_count
        
    except Exception as e:
        print(f"Грешка при копиране на category_translations: {e}")
        return 0


def copy_page_events(missing_ids: List[Any]) -> int:
    """Специална обработка за page_events - JSON сериализация на metadata"""
    import json
    
    try:
        local_conn = psycopg2.connect(**LOCAL_DB)
        local_cursor = local_conn.cursor()
        
        # Взимане на данните от локална база
        placeholders = ', '.join(['%s'] * len(missing_ids))
        query = f"SELECT id, event_type, page, metadata, ip, user_agent, created_at FROM page_events WHERE id IN ({placeholders})"
        local_cursor.execute(query, missing_ids)
        rows = local_cursor.fetchall()
        local_cursor.close()
        local_conn.close()
        
        if not rows:
            return 0
        
        insert_query = """
            INSERT INTO page_events (id, event_type, page, metadata, ip, user_agent, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        inserted_count = 0
        error_count = 0
        
        for row in rows:
            record_id, event_type, page, metadata, ip, user_agent, created_at = row
            
            # Сериализираме metadata като JSON
            if isinstance(metadata, dict):
                metadata = json.dumps(metadata)
            
            try:
                docker_conn = psycopg2.connect(**DOCKER_DB)
                docker_cursor = docker_conn.cursor()
                docker_cursor.execute(insert_query, (record_id, event_type, page, metadata, ip, user_agent, created_at))
                docker_conn.commit()
                docker_cursor.close()
                docker_conn.close()
                inserted_count += 1
            except Exception as e:
                error_count += 1
                pass
        
        print(f"  Успешно вмъкнати: {inserted_count}, Грешки: {error_count}")
        return inserted_count
        
    except Exception as e:
        print(f"Грешка при копиране на page_events: {e}")
        return 0


def merge_translations_safely() -> int:
    """Специална логика за translations таблицата - вмъква само липсващите по (lang, key) без ID"""
    try:
        local_conn = psycopg2.connect(**LOCAL_DB)
        docker_conn = psycopg2.connect(**DOCKER_DB)
        
        local_cursor = local_conn.cursor()
        docker_cursor = docker_conn.cursor()
        
        # Взимаме всички (lang, key) от Docker
        docker_cursor.execute("SELECT lang, key FROM translations;")
        docker_lang_keys = set((row[0], row[1]) for row in docker_cursor.fetchall())
        
        # Взимаме всички записи от локална база
        local_cursor.execute("SELECT id, lang, key, value FROM translations ORDER BY id;")
        local_records = local_cursor.fetchall()
        
        insert_query = """
            INSERT INTO translations (lang, key, value)
            VALUES (%s, %s, %s)
        """
        
        inserted_count = 0
        skipped_count = 0
        error_count = 0
        
        for record in local_records:
            record_id, lang, key, value = record
            
            # Пропускаме, ако (lang, key) вече съществува в Docker
            if (lang, key) in docker_lang_keys:
                skipped_count += 1
                continue
            
            # Вмъкваме записа с отделна транзакция (без ID)
            try:
                temp_conn = psycopg2.connect(**DOCKER_DB)
                temp_cursor = temp_conn.cursor()
                temp_cursor.execute(insert_query, (lang, key, value))
                temp_conn.commit()
                temp_cursor.close()
                temp_conn.close()
                inserted_count += 1
            except Exception as e:
                error_count += 1
                pass
        
        local_cursor.close()
        local_conn.close()
        docker_cursor.close()
        docker_conn.close()
        
        print(f"  Translations: Вмъкнати {inserted_count}, Пропуснати {skipped_count}, Грешки {error_count}")
        return inserted_count
        
    except Exception as e:
        print(f"Грешка при сливане на translations: {e}")
        return 0


def main():
    print("=" * 80)
    print("ИНТЕЛИГЕНТНО СЛИВАНЕ НА ЛОКАЛНА БАЗА В DOCKER БАЗА")
    print("=" * 80)
    print()
    
    # Таблици за сливане в правилния ред (първо родителски, после детски)
    tables_to_merge = [
        # Първо основни таблици без FK
        "users",
        "providers",
        "services",
        "leads",
        "reviews",
        "categories",
        "locations",
        # После зависими таблици
        "provider_translations",
        "provider_cities",
        "provider_slug_history",
        "service_cities",
        "category_translations",
        "location_translations",
        "lead_matches",
        "lead_rate_limits",
        "lead_events",
        "url_redirects",
        # Rate limits и tokens
        "auth_rate_limits",
        "magic_link_tokens",
        "password_reset_tokens",
        "pending_lead_claims",
        # Events
        "page_events",
        "messages",
        # Alembic накрая
        "alembic_version"
    ]
    
    results = {}
    
    # Сливане на обикновените таблици
    for table in tables_to_merge:
        print(f"Обработване на {table}...")
        
        try:
            conn = psycopg2.connect(**LOCAL_DB)
            pk = get_primary_key(conn, table)
            conn.close()
        except:
            pk = "id"
        
        missing_ids = get_missing_ids(table, pk)
        print(f"  Липсващи записи: {len(missing_ids)}")
        
        if missing_ids:
            inserted = copy_records_to_docker(table, pk, missing_ids)
            print(f"  Вмъкнати записи: {inserted}")
            results[table] = {
                'missing_count': len(missing_ids),
                'inserted_count': inserted
            }
        else:
            print(f"  Няма липсващи записи")
            results[table] = {
                'missing_count': 0,
                'inserted_count': 0
            }
        print()
    
    # Специално сливане на translations
    print("Обработване на translations (специална логика)...")
    translations_inserted = merge_translations_safely()
    results['translations'] = {
        'inserted_count': translations_inserted
    }
    print()
    
    # Запазване на резултатите
    with open('/Users/dimitardimitrov/nevumo/merge_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("=" * 80)
    print("ОБОБЩЕНИЕ НА СЛИВАНЕТО:")
    print("=" * 80)
    
    total_inserted = sum(r.get('inserted_count', 0) for r in results.values())
    print(f"Общо вмъкнати записи в Docker: {total_inserted}")
    print()
    print("Детайлни резултати записани в: merge_results.json")


if __name__ == "__main__":
    main()
