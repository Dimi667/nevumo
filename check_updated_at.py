#!/usr/bin/env python3
"""
Проверка за updated_at колони в таблиците
"""

import psycopg2

LOCAL_DB = {
    "host": "localhost",
    "port": 5432,
    "user": "nevumo",
    "password": "nevumo",
    "database": "nevumo_leads"
}

tables_to_check = [
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

def check_columns(table: str):
    conn = psycopg2.connect(**LOCAL_DB)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = '{table}'
        ORDER BY ordinal_position;
    """)
    columns = cursor.fetchall()
    cursor.close()
    conn.close()
    
    has_updated_at = any(col[0] == 'updated_at' for col in columns)
    has_created_at = any(col[0] == 'created_at' for col in columns)
    
    return has_updated_at, has_created_at, columns

print("Проверка за updated_at и created_at колони:")
print("=" * 80)
print(f"{'Таблица':<30} {'updated_at':<12} {'created_at':<12}")
print("-" * 80)

for table in tables_to_check:
    has_updated, has_created, columns = check_columns(table)
    print(f"{table:<30} {'✓' if has_updated else '✗':<12} {'✓' if has_created else '✗':<12}")
