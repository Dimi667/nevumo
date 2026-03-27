#!/usr/bin/env python3
"""Fix provider slug from 'devs-1' to 'devs' in the database."""

import sys
import os

# Add the api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'apps', 'api'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def fix_provider_slug():
    """Update the provider slug from devs-1 to devs."""
    # Get database URL from environment or use default
    database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/nevumo_leads')
    
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        # Check if devs-1 exists
        result = db.execute(
            text("SELECT id, business_name, slug FROM providers WHERE slug = 'devs-1'")
        ).fetchone()
        
        if not result:
            print("No provider found with slug 'devs-1'")
            # Check if devs already exists
            result_devs = db.execute(
                text("SELECT id, business_name, slug FROM providers WHERE slug = 'devs'")
            ).fetchone()
            if result_devs:
                print(f"Provider with slug 'devs' already exists: {result_devs}")
            return
        
        provider_id, business_name, old_slug = result
        print(f"Found provider: id={provider_id}, business_name={business_name}, slug={old_slug}")
        
        # Check if 'devs' slug is already taken by another provider
        conflict = db.execute(
            text("SELECT id FROM providers WHERE slug = 'devs' AND id != :provider_id"),
            {"provider_id": provider_id}
        ).fetchone()
        
        if conflict:
            print(f"ERROR: Cannot update slug - 'devs' is already taken by provider {conflict[0]}")
            return
        
        # Update the slug
        db.execute(
            text("UPDATE providers SET slug = 'devs' WHERE id = :provider_id"),
            {"provider_id": provider_id}
        )
        db.commit()
        
        print(f"✓ Successfully updated provider slug from 'devs-1' to 'devs'")
        
        # Also check for other providers with numeric suffixes
        print("\nChecking for other providers with numeric suffixes...")
        others = db.execute(
            text("SELECT id, business_name, slug FROM providers WHERE slug ~ '-[0-9]+$")
        ).fetchall()
        
        if others:
            print(f"Found {len(others)} provider(s) with numeric suffixes:")
            for row in others:
                print(f"  - id={row[0]}, business_name='{row[1]}', slug='{row[2]}'")
        else:
            print("No other providers with numeric suffixes found.")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_provider_slug()
