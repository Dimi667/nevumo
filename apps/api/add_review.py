#!/usr/bin/env python3
"""
Add a single review with rating 5 for ET LILI provider.
"""

import sys
import os
from datetime import datetime
import uuid

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dependencies import get_db
from models import Review

def add_review():
    """Add a review with rating 5 for ET LILI provider."""
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # ET LILI provider ID from the API response
        provider_id = 'e725ef65-e0dc-48a4-9ae1-80ed1f82a32f'
        # Use the correct user ID as client
        client_id = 'a3e26995-c7f6-42ce-99d1-68dfad57d581'  # This is the user_id from the provider
        
        # Create a review with rating 5
        review = Review(
            id=str(uuid.uuid4()),
            provider_id=provider_id,
            client_id=client_id,
            lead_id='385668f1-a9d8-43c2-9d41-cd4eb74d6b35',  # Use existing lead ID
            rating=5,
            comment='Excellent service! Very professional and punctual.',
            created_at=datetime.now()
        )
        
        db.add(review)
        db.commit()
        
        print(f"✅ Successfully added review with rating 5 for ET LILI")
        print(f"   Review ID: {review.id}")
        print(f"   Rating: {review.rating}")
        print(f"   Comment: {review.comment}")
        
    except Exception as e:
        print(f"❌ Error adding review: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("📝 Adding review for ET LILI...")
    add_review()
    print("✨ Done!")
