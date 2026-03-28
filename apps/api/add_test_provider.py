#!/usr/bin/env python3
"""
Script to add a test provider (ET ЛИЛИ) to the database for testing purposes.
"""

import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import uuid

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dependencies import get_db
from models import User, Provider, Service, Location, Category, ProviderCity, ServiceCity

def add_test_provider():
    """Add ET ЛИЛИ test provider to the database."""
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Check if provider already exists
        existing_user = db.query(User).filter(User.email == 'lili@test.bg').first()
        if existing_user:
            print("ℹ️  Provider with email lili@test.bg already exists")
            return existing_user.id
        
        # Get Sofia location (ID: 1) and Massage category (ID: 1)
        sofia_location = db.query(Location).filter(Location.id == 1).first()
        massage_category = db.query(Category).filter(Category.id == 1).first()
        
        if not sofia_location:
            print("❌ Sofia location not found")
            return
        if not massage_category:
            print("❌ Massage category not found")
            return
        
        # Create user
        user = User(
            email='lili@test.bg',
            password_hash='$2b$12$placeholder_hash_for_testing',  # Will be properly hashed
            role='provider',
            locale='bg',
            country_code='BG'
        )
        db.add(user)
        db.flush()  # Get the user ID
        
        # Create provider
        provider = Provider(
            user_id=user.id,
            business_name='ЕТ ЛИЛИ',
            description='Предлагам услугите си в дома ви или където ви е удобно. Всеки ден от 9.00 до 22.00',
            slug='et-lili',  # Auto-generated from business_name
            rating=4.7,  # As requested
            verified=True,
            availability_status='active'
        )
        db.add(provider)
        db.flush()  # Get the provider ID
        
        # Add provider city availability
        provider_city = ProviderCity(
            provider_id=provider.id,
            city_id=sofia_location.id
        )
        db.add(provider_city)
        
        # Create service
        service = Service(
            provider_id=provider.id,
            category_id=massage_category.id,
            title='Маникюр и педикюр на Ваш адрес!',
            description='Предлагам услугите си в дома ви или където ви е удобно. Всеки ден от 9.00 до 22.00',
            price_type='hourly',
            base_price=30.00,
            currency='EUR'
        )
        db.add(service)
        db.flush()  # Get the service ID
        
        # Add service city availability
        service_city = ServiceCity(
            service_id=service.id,
            city_id=sofia_location.id
        )
        db.add(service_city)
        
        # Add 123 completed jobs (simulate through leads with status 'done')
        # We'll create placeholder leads to simulate the completed jobs count
        for i in range(123):
            lead = db.execute(text("""
                INSERT INTO leads (id, client_id, provider_id, category_id, city_id, phone, description, status, created_at)
                VALUES (:id, :client_id, :provider_id, :category_id, :city_id, :phone, :description, :status, :created_at)
            """), {
                'id': str(uuid.uuid4()),
                'client_id': user.id,  # Using same user as client for simplicity
                'provider_id': provider.id,
                'category_id': massage_category.id,
                'city_id': sofia_location.id,
                'phone': f'+359888{i:04d}',
                'description': f'Завършена заявка #{i+1}',
                'status': 'done',
                'created_at': datetime.now()
            })
        
        db.commit()
        
        print(f"✅ Successfully added test provider ET ЛИЛИ")
        print(f"   User ID: {user.id}")
        print(f"   Provider ID: {provider.id}")
        print(f"   Service ID: {service.id}")
        print(f"   Email: lili@test.bg")
        print(f"   Rating: 4.7")
        print(f"   Completed jobs: 123 (simulated)")
        
        # Clear Redis cache if available
        try:
            from dependencies import get_redis
            redis_client = next(get_redis())
            if redis_client:
                redis_client.delete("providers:sofia")
                redis_client.delete("categories:1")
                print("🗑️  Cleared Redis cache")
        except Exception as e:
            print(f"⚠️  Could not clear Redis cache: {e}")
        
    except Exception as e:
        print(f"❌ Error adding test provider: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🧑‍💼 Adding test provider ET ЛИЛИ to the database...")
    add_test_provider()
    print("✨ Done!")
