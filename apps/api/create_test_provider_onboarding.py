#!/usr/bin/env python3
"""
Script to create a test provider for onboarding diagnostics.
Creates a provider with incomplete profile to trigger onboarding wizard.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from sqlalchemy.orm import Session
from datetime import datetime
import secrets

from apps.api.dependencies import get_db
from apps.api.models import User, Provider
from apps.api.services.auth_service import hash_password

def create_test_provider():
    """Create a test provider for onboarding diagnostics."""
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Check if provider already exists
        existing_user = db.query(User).filter(User.email == 'onboarding@test.bg').first()
        if existing_user:
            print("ℹ️  Provider with email onboarding@test.bg already exists")
            print("   Deleting existing provider...")
            # Delete existing provider if any
            existing_provider = db.query(Provider).filter(Provider.user_id == existing_user.id).first()
            if existing_provider:
                db.delete(existing_provider)
            db.delete(existing_user)
            db.commit()
        
        # Create user with provider role
        password = 'Test123456'
        user = User(
            email='onboarding@test.bg',
            password_hash=hash_password(password),
            role='provider',
            is_active=True,
            locale='bg',
            country_code='BG'
        )
        db.add(user)
        db.flush()  # Get the user ID
        
        # Create provider with draft slug (incomplete profile for onboarding)
        draft_slug = f"draft{secrets.token_hex(6)}"
        provider = Provider(
            user_id=user.id,
            business_name='onboarding@test.bg',  # Email as placeholder to trigger onboarding
            slug=draft_slug,
            rating=0,
            verified=False,
            availability_status='active',
        )
        db.add(provider)
        db.flush()
        
        db.commit()
        
        print(f"✅ Successfully created test provider for onboarding diagnostics")
        print(f"   User ID: {user.id}")
        print(f"   Provider ID: {provider.id}")
        print(f"   Email: onboarding@test.bg")
        print(f"   Password: {password}")
        print(f"   Slug: {draft_slug} (draft, will trigger onboarding)")
        
    except Exception as e:
        print(f"❌ Error creating test provider: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🧑‍💼 Creating test provider for onboarding diagnostics...")
    create_test_provider()
    print("✨ Done!")
