#!/usr/bin/env python3
"""
Execute SQL script to rename translation keys in the database
Uses the same database configuration as apps/api/database.py
"""
import os
import sys
from sqlalchemy import create_engine, text

# Use the same database URL as apps/api/database.py
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads",
)

print(f"Connecting to database...")

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c client_encoding=utf8"},
)

# Read SQL script
with open('rename_translation_keys.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

print(f"Read SQL script with {len(sql_content.split(';'))-1} statements")

# Execute SQL statements
with engine.begin() as conn:
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
    
    for i, stmt in enumerate(statements, 1):
        if not stmt.startswith('--'):
            try:
                conn.execute(text(stmt))
                print(f"✓ Executed statement {i}/{len(statements)}")
            except Exception as e:
                print(f"✗ Failed statement {i}/{len(statements)}: {e}")
                print(f"  Statement: {stmt[:100]}...")
                # Continue with other statements even if one fails
                continue

print("\nSQL execution complete!")
