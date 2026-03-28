#!/usr/bin/env python3
"""
Script to add 5 new leads for testing status changes from New to Done.
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
from models import User, Provider, Location, Category

def add_test_leads():
    """Add 5 new leads for testing."""
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Get ET ЛИЛИ provider
        provider = db.query(Provider).filter(Provider.business_name == 'ЕТ ЛИЛИ').first()
        if not provider:
            print("❌ Provider ET ЛИЛИ not found")
            return
        
        # Get Sofia location and Massage category
        sofia_location = db.query(Location).filter(Location.id == 1).first()
        massage_category = db.query(Category).filter(Category.id == 1).first()
        
        # Create a test client
        client = User(
            email=f'test_client_{datetime.now().strftime("%Y%m%d%H%M%S")}@test.bg',
            role='client',
            locale='bg',
            country_code='BG'
        )
        db.add(client)
        db.flush()
        
        # Add 5 new leads
        for i in range(1, 6):
            lead = db.execute(text("""
                INSERT INTO leads (id, client_id, provider_id, category_id, city_id, phone, description, status, created_at)
                VALUES (:id, :client_id, :provider_id, :category_id, :city_id, :phone, :description, :status, :created_at)
            """), {
                'id': str(uuid.uuid4()),
                'client_id': client.id,
                'provider_id': provider.id,
                'category_id': massage_category.id,
                'city_id': sofia_location.id,
                'phone': f'+359888{1000 + i}',
                'description': f'Тест заявка #{i} за маникюр и педикюр',
                'status': 'created',  # New status
                'created_at': datetime.now()
            })
            
            print(f"✅ Lead #{i} created with status 'created'")
        
        db.commit()
        
        print(f"✅ Successfully created 5 new leads")
        print(f"   Client ID: {client.id}")
        print(f"   Provider: ET ЛИЛИ ({provider.id})")
        print(f"   All leads have status 'created' and ready for testing")
        
    except Exception as e:
        print(f"❌ Error adding leads: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("📝 Adding 5 new test leads...")
    add_test_leads()
    print("✨ Done!")
