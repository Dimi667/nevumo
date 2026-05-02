#!/usr/bin/env python3
"""
Fix hardcoded Warsaw city names in translations table.
Replaces 'Warszawa', 'Варшава', and 'Warsaw' with {city} placeholder.
Database: PostgreSQL on port 5433
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Connect to database on port 5433
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads",
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c client_encoding=utf8"},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def main():
    db = SessionLocal()
    
    try:
        print("=== Fix Warsaw Placeholders Script ===\n")
        
        total_updated = 0
        patterns = [
            ("Warszawa", "{city}"),
            ("Варшава", "{city}"),
            ("Warsaw", "{city}"),
        ]
        
        for search_term, replacement in patterns:
            # Find records containing the search term
            find_query = text("""
                SELECT id, lang, key, value 
                FROM translations 
                WHERE value LIKE :pattern
            """)
            
            result = db.execute(find_query, {"pattern": f"%{search_term}%"}).fetchall()
            
            if result:
                print(f"Found {len(result)} records containing '{search_term}':")
                for row in result:
                    print(f"  - [{row.lang}] {row.key}: {row.value[:80]}...")
                
                # Update records
                update_query = text("""
                    UPDATE translations 
                    SET value = REPLACE(value, :search, :replace)
                    WHERE value LIKE :pattern
                """)
                
                update_result = db.execute(update_query, {
                    "search": search_term,
                    "replace": replacement,
                    "pattern": f"%{search_term}%"
                })
                
                updated_count = update_result.rowcount
                total_updated += updated_count
                print(f"  ✓ Updated {updated_count} records\n")
            else:
                print(f"No records found containing '{search_term}'\n")
        
        db.commit()
        
        print("=== Summary ===")
        print(f"Total records updated: {total_updated}")
        print("\n=== Script completed ===")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
