#!/usr/bin/env python3
"""
Script to fix the password hash for the test provider ET ЛИЛИ.
"""

import bcrypt

from apps.api.dependencies import get_db
from apps.api.models import User

def fix_password():
    """Update the password hash for lili@test.bg with proper bcrypt hash."""
    
    # Generate proper bcrypt hash for password '123456789'
    password = '123456789'
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    print(f"Generated hash: {hashed.decode()}")
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Find the user
        user = db.query(User).filter(User.email == 'lili@test.bg').first()
        if not user:
            print("❌ User lili@test.bg not found")
            return
        
        # Update password hash
        user.password_hash = hashed.decode()
        db.commit()
        
        print("✅ Password updated successfully for lili@test.bg")
        print("   Now you can login with:")
        print("   Email: lili@test.bg")
        print("   Password: 123456789")
        
    except Exception as e:
        print(f"❌ Error updating password: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Fixing password hash for test provider...")
    fix_password()
    print("✨ Done!")
