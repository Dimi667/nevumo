#!/usr/bin/env python3
"""
Temporary script to check database state
"""
import os
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

# Load DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")

print("=" * 60)
print("DATABASE STATE CHECK")
print("=" * 60)
print(f"Connecting to: {DATABASE_URL}")
print()

try:
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # 1. List all tables in public schema
        print("1. TABLES IN PUBLIC SCHEMA:")
        print("-" * 60)
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result.fetchall()]
        
        if tables:
            for table in tables:
                print(f"  - {table}")
        else:
            print("  NO TABLES FOUND")
        print()
        
        # 2. Check if users and providers tables exist and count rows
        print("2. ROW COUNTS:")
        print("-" * 60)
        
        if 'users' in tables:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.fetchone()[0]
            print(f"  users table: {user_count} rows")
        else:
            print("  users table: DOES NOT EXIST")
        
        if 'providers' in tables:
            result = conn.execute(text("SELECT COUNT(*) FROM providers"))
            provider_count = result.fetchone()[0]
            print(f"  providers table: {provider_count} rows")
        else:
            print("  providers table: DOES NOT EXIST")
        print()
        
        # 3. Check for users with role 'client' created in last 1 hour
        print("3. RECENT CLIENT USERS (last 1 hour):")
        print("-" * 60)
        
        if 'users' in tables:
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            result = conn.execute(text("""
                SELECT id, email, role, created_at
                FROM users
                WHERE role = 'client' 
                AND created_at >= :one_hour_ago
                ORDER BY created_at DESC
            """), {"one_hour_ago": one_hour_ago})
            
            recent_clients = result.fetchall()
            if recent_clients:
                for row in recent_clients:
                    print(f"  ID: {row[0]}")
                    print(f"  Email: {row[1]}")
                    print(f"  Role: {row[2]}")
                    print(f"  Created: {row[3]}")
                    print()
            else:
                print("  No client users created in the last 1 hour")
        else:
            print("  Cannot check - users table does not exist")
        print()
        
        # 4. If providers table exists, check for recent providers
        print("4. RECENT PROVIDERS (last 1 hour):")
        print("-" * 60)
        
        if 'providers' in tables:
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            result = conn.execute(text("""
                SELECT id, user_id, business_name, slug, created_at
                FROM providers
                WHERE created_at >= :one_hour_ago
                ORDER BY created_at DESC
            """), {"one_hour_ago": one_hour_ago})
            
            recent_providers = result.fetchall()
            if recent_providers:
                for row in recent_providers:
                    print(f"  ID: {row[0]}")
                    print(f"  User ID: {row[1]}")
                    print(f"  Business Name: {row[2]}")
                    print(f"  Slug: {row[3]}")
                    print(f"  Created: {row[4]}")
                    print()
            else:
                print("  No providers created in the last 1 hour")
        else:
            print("  Cannot check - providers table does not exist")
        print()

    print("=" * 60)
    print("CHECK COMPLETE")
    print("=" * 60)

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
