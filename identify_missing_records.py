#!/usr/bin/env python3
"""
Скрипт за идентифициране на липсващите записи в Docker базата
"""

import psycopg2
from typing import Dict, List, Any, Tuple

# Конфигурация
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
    return "id"  # fallback


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


def get_missing_records(table: str, pk: str) -> Tuple[List[Any], List[Any]]:
    """Връща ID-тата на записите, които липсват в Docker базата"""
    missing_in_docker = []
    missing_in_local = []
    
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
        
        # Намираме разликите
        missing_in_docker = list(local_ids - docker_ids)
        missing_in_local = list(docker_ids - local_ids)
        
    except Exception as e:
        print(f"Грешка при таблица {table}: {e}")
    
    return missing_in_docker, missing_in_local


def main():
    print("=" * 80)
    print("ИДЕНТИФИКАЦИЯ НА ЛИПСВАЩИ ЗАПИСИ В DOCKER БАЗАТА")
    print("=" * 80)
    print()
    
    # Таблици с разлики от предишния анализ
    tables_with_diff = [
        "alembic_version",
        "auth_rate_limits",
        "lead_matches",
        "lead_rate_limits",
        "leads",
        "magic_link_tokens",
        "page_events",
        "password_reset_tokens",
        "pending_lead_claims",
        "provider_cities",
        "provider_slug_history",
        "provider_translations",
        "providers",
        "reviews",
        "service_cities",
        "services",
        "translations",
        "url_redirects",
        "users"
    ]
    
    results = {}
    
    for table in tables_with_diff:
        print(f"Анализиране на {table}...")
        
        # Взимане на първичния ключ
        try:
            conn = psycopg2.connect(**LOCAL_DB)
            pk = get_primary_key(conn, table)
            conn.close()
        except:
            pk = "id"
        
        missing_in_docker, missing_in_local = get_missing_records(table, pk)
        
        results[table] = {
            'primary_key': pk,
            'missing_in_docker_count': len(missing_in_docker),
            'missing_in_local_count': len(missing_in_local),
            'missing_in_docker_ids': missing_in_docker[:10],  # Първите 10 за преглед
            'missing_in_local_ids': missing_in_local[:10]
        }
        
        print(f"  Първичен ключ: {pk}")
        print(f"  Липсват в Docker: {len(missing_in_docker)} записа")
        if missing_in_docker:
            print(f"    Пример ID-та: {missing_in_docker[:5]}")
        print(f"  Липсват в Локална: {len(missing_in_local)} записа")
        if missing_in_local:
            print(f"    Пример ID-та: {missing_in_local[:5]}")
        print()
    
    # Запазване на резултатите
    import json
    with open('/Users/dimitardimitrov/nevumo/missing_records_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("=" * 80)
    print("ОБОБЩЕНИЕ:")
    print("=" * 80)
    
    total_missing_in_docker = sum(r['missing_in_docker_count'] for r in results.values())
    total_missing_in_local = sum(r['missing_in_local_count'] for r in results.values())
    
    print(f"Общо записи, липсващи в Docker: {total_missing_in_docker}")
    print(f"Общо записи, липсващи в Локална: {total_missing_in_local}")
    print()
    print("Детайлни резултати записани в: missing_records_analysis.json")


if __name__ == "__main__":
    main()
