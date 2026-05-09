#!/usr/bin/env python3
"""
Script to add a test client to the database for testing purposes.
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import uuid
import bcrypt

from apps.api.dependencies import get_db, get_redis
from apps.api.models import User

def add_test_client():
    """Add test client to the database."""
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Check if client already exists
        existing_user = db.query(User).filter(User.email == 'client@test.bg').first()
        if existing_user:
            print("ℹ️  Client with email client@test.bg already exists")
            print(f"   User ID: {existing_user.id}")
            print(f"   City ID: {existing_user.city_id}")
            return existing_user.id
        
        # Hash the password
        password = '123456789'
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create user WITHOUT city_id (to test redirect logic)
        user = User(
            email='client@test.bg',
            password_hash=password_hash,
            role='client',
            locale='bg',
            country_code='BG',
            city_id=None  # Explicitly null to test redirect to city selection
        )
        db.add(user)
        db.flush()  # Get the user ID
        
        db.commit()
        
        print(f"✅ Successfully added test client")
        print(f"   User ID: {user.id}")
        print(f"   Email: client@test.bg")
        print(f"   Password: 123456789")
        print(f"   City ID: None (for testing redirect)")
        
        # Clear Redis cache if available
        try:
            redis_client = next(get_redis())
            if redis_client:
                redis_client.delete(f"user:{user.id}")
                print("🗑️  Cleared Redis cache")
        except Exception as e:
            print(f"⚠️  Could not clear Redis cache: {e}")
        
    except Exception as e:
        print(f"❌ Error adding test client: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🧑 Adding test client to the database...")
    add_test_client()
    print("✨ Done!")
