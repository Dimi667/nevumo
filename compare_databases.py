#!/usr/bin/env python3
"""
Скрипт за сравнение на локална PostgreSQL база и Docker база
"""

import subprocess
import json
from typing import Dict, List, Any
import psycopg2

# Конфигурация
LOCAL_DB = {
    "host": "localhost",
    "port": 5432,
    "user": "nevumo",
    "password": "nevumo",
    "database": "nevumo_leads"
}

DOCKER_CONTAINER = "nevumo-postgres"
DOCKER_DB = {
    "host": "localhost",  # Docker е мапнат на 5432
    "port": 5433,  # Ще използваме различен порт за Docker
    "user": "nevumo",
    "password": "nevumo",
    "database": "nevumo_leads"
}


def execute_psql_local(query: str) -> List[Dict[str, Any]]:
    """Изпълнява SQL заявка към локалната база"""
    try:
        conn = psycopg2.connect(**LOCAL_DB)
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        data = []
        for row in cursor:
            data.append(dict(zip(columns, row)))
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(f"Грешка при локална заявка: {e}")
        return []


def execute_psql_docker(query: str) -> List[Dict[str, Any]]:
    """Изпълнява SQL заявка към Docker базата"""
    try:
        conn = psycopg2.connect(**DOCKER_DB)
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        data = []
        for row in cursor:
            data.append(dict(zip(columns, row)))
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(f"Грешка при Docker заявка: {e}")
        return []


def get_tables(db_type: str) -> List[str]:
    """Връща списък с таблици от базата"""
    if db_type == "local":
        data = execute_psql_local(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;"
        )
    else:
        data = execute_psql_docker(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;"
        )
    
    return [row['tablename'] for row in data]


def get_table_count(db_type: str, table: str) -> int:
    """Връща броя записи в таблица"""
    if db_type == "local":
        data = execute_psql_local(f"SELECT COUNT(*) as count FROM {table};")
    else:
        data = execute_psql_docker(f"SELECT COUNT(*) as count FROM {table};")
    
    if data and data[0].get('count'):
        return int(data[0]['count'])
    return 0


def main():
    print("=" * 80)
    print("СРАВНЕНИЕ НА ЛОКАЛНА И DOCKER POSTGRESQL БАЗА")
    print("=" * 80)
    print()
    
    # Взимане на таблици от двете бази
    print("1. Взимане на списъка с таблици...")
    local_tables = get_tables("local")
    docker_tables = get_tables("docker")
    
    all_tables = sorted(set(local_tables + docker_tables))
    
    print(f"   Локална база: {len(local_tables)} таблици")
    print(f"   Docker база: {len(docker_tables)} таблици")
    print(f"   Общо уникални: {len(all_tables)} таблици")
    print()
    
    # Сравнение на броя записи
    print("2. Сравнение на броя записи по таблици:")
    print()
    print(f"{'Таблица':<40} {'Локална':>12} {'Docker':>12} {'Разлика':>12}")
    print("-" * 80)
    
    comparison = []
    for table in all_tables:
        local_count = get_table_count("local", table) if table in local_tables else 0
        docker_count = get_table_count("docker", table) if table in docker_tables else 0
        diff = local_count - docker_count
        
        comparison.append({
            'table': table,
            'local_count': local_count,
            'docker_count': docker_count,
            'diff': diff,
            'in_local_only': table in local_tables and table not in docker_tables,
            'in_docker_only': table not in local_tables and table in docker_tables
        })
        
        marker = ""
        if table not in local_tables:
            marker = " [само в Docker]"
        elif table not in docker_tables:
            marker = " [само в Локална]"
        elif diff != 0:
            marker = " [разлика]"
        
        print(f"{table:<40} {local_count:>12} {docker_count:>12} {diff:>12}{marker}")
    
    print()
    print("=" * 80)
    print("ОБОБЩЕНИЕ:")
    print("=" * 80)
    
    local_only = [t for t in comparison if t['in_local_only']]
    docker_only = [t for t in comparison if t['in_docker_only']]
    has_diff = [t for t in comparison if t['diff'] != 0 and not t['in_local_only'] and not t['in_docker_only']]
    
    print(f"Таблици само в локална база: {len(local_only)}")
    if local_only:
        for t in local_only:
            print(f"  - {t['table']}: {t['local_count']} записа")
    
    print()
    print(f"Таблици само в Docker база: {len(docker_only)}")
    if docker_only:
        for t in docker_only:
            print(f"  - {t['table']}: {t['docker_count']} записа")
    
    print()
    print(f"Таблици с разлика в броя записи: {len(has_diff)}")
    if has_diff:
        print(f"{'Таблица':<40} {'Локална':>12} {'Docker':>12} {'Разлика':>12}")
        print("-" * 80)
        for t in has_diff:
            print(f"{t['table']:<40} {t['local_count']:>12} {t['docker_count']:>12} {t['diff']:>12}")
    
    # Запазване на резултатите в JSON
    with open('/Users/dimitardimitrov/nevumo/db_comparison.json', 'w', encoding='utf-8') as f:
        json.dump({
            'local_tables': local_tables,
            'docker_tables': docker_tables,
            'all_tables': all_tables,
            'comparison': comparison,
            'summary': {
                'local_only_count': len(local_only),
                'docker_only_count': len(docker_only),
                'has_diff_count': len(has_diff),
                'local_only_tables': local_only,
                'docker_only_tables': docker_only,
                'tables_with_diff': has_diff
            }
        }, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"Детайлни резултати записани в: db_comparison.json")


if __name__ == "__main__":
    main()
