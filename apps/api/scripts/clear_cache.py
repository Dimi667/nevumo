#!/usr/bin/env python3
"""
Clear Redis cache for translations.
Run: python -m apps.api.scripts.clear_cache
"""

import redis

def clear_translation_cache():
    """Clear all translation cache from Redis."""
    
    try:
        # Connect to Redis (assuming default localhost:6379)
        redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        
        # Test connection
        redis_client.ping()
        print("✅ Connected to Redis")
        
        # Get all keys matching trans:* pattern
        cache_keys = redis_client.keys("trans:*")
        
        if cache_keys:
            deleted_count = redis_client.delete(*cache_keys)
            print(f"🗑️  Cleared {deleted_count} translation cache keys")
            print(f"✅ Cache cleared successfully")
        else:
            print("ℹ️  No translation cache keys found")
            
    except redis.ConnectionError:
        print("❌ Could not connect to Redis - make sure Redis is running")
    except Exception as e:
        print(f"❌ Error clearing cache: {e}")

if __name__ == "__main__":
    print("🧹 Clearing translation cache...")
    clear_translation_cache()
    print("✨ Done!")
