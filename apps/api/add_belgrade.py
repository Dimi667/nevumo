#!/usr/bin/env python3
"""
Script to add Belgrade, Serbia to the database for testing Eurozone transition.
This script inserts Belgrade into the locations table with country_code 'RS'.
"""

import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import text

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dependencies import get_db
from models import Location

def add_belgrade():
    """Add Belgrade, Serbia to the locations table."""
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Check if Belgrade already exists
        existing = db.query(Location).filter(
            Location.country_code == 'RS',
            Location.slug == 'belgrade'
        ).first()
        
        if existing:
            print("ℹ️  Belgrade already exists in the database")
            return
        
        # Get the next ID for the locations table
        max_id_result = db.execute(text("SELECT MAX(id) FROM locations"))
        max_id = max_id_result.scalar() or 0
        next_id = max_id + 1
        
        # Insert Belgrade
        belgrade = Location(
            id=next_id,
            country_code='RS',
            city='Belgrade',
            slug='belgrade',
            lat=44.8125,  # Approximate latitude
            lng=20.4375   # Approximate longitude
        )
        
        db.add(belgrade)
        db.commit()
        
        print(f"✅ Successfully added Belgrade to locations table (ID: {next_id})")
        
        # Clear Redis cache for Serbian cities if Redis is available
        try:
            from dependencies import get_redis
            redis_client = next(get_redis())
            if redis_client:
                redis_client.delete("cities:RS")
                print("🗑️  Cleared Redis cache for Serbian cities")
        except Exception as e:
            print(f"⚠️  Could not clear Redis cache: {e}")
        
    except Exception as e:
        print(f"❌ Error adding Belgrade: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🌍 Adding Belgrade, Serbia to the database...")
    add_belgrade()
    print("✨ Done!")
