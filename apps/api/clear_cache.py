#!/usr/bin/env python3
"""
Script to clear Redis cache for cities after currency updates.
"""

import redis

def clear_cities_cache():
    """Clear Redis cache for all cities."""
    
    try:
        # Connect to Redis (assuming default localhost:6379)
        redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        
        # Test connection
        redis_client.ping()
        print("✅ Connected to Redis")
        
        # Clear cache for BG and RS cities
        deleted_keys = []
        for country in ['BG', 'RS']:
            cache_key = f"cities:{country}"
            if redis_client.delete(cache_key):
                deleted_keys.append(cache_key)
                print(f"🗑️  Cleared cache for {cache_key}")
            else:
                print(f"ℹ️  No cache found for {cache_key}")
        
        if deleted_keys:
            print(f"✅ Cleared {len(deleted_keys)} cache keys")
        else:
            print("ℹ️  No cache keys to clear")
            
    except redis.ConnectionError:
        print("❌ Could not connect to Redis - make sure Redis is running")
    except Exception as e:
        print(f"❌ Error clearing cache: {e}")

if __name__ == "__main__":
    print("🧹 Clearing cities cache...")
    clear_cities_cache()
    print("✨ Done!")
