#!/usr/bin/env python3
import redis
import os

def clear_translation_cache():
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    print(f"🧹 Connecting to Redis at {redis_host}...")
    
    try:
        redis_client = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)
        redis_client.ping()
        print("✅ Connected to Redis")
        
        # Clear all translation keys
        keys = redis_client.keys("trans:*")
        if keys:
            print(f"🗑️  Deleting {len(keys)} translation cache keys...")
            redis_client.delete(*keys)
            print("✅ Translation cache cleared")
        else:
            print("ℹ️  No translation cache keys found")
            
        # Also clear city-related keys if any
        city_keys = redis_client.keys("city:*")
        if city_keys:
            print(f"🗑️  Deleting {len(city_keys)} city cache keys...")
            redis_client.delete(*city_keys)
            print("✅ City cache cleared")
            
    except redis.ConnectionError:
        print(f"❌ Could not connect to Redis at {redis_host}")
    except Exception as e:
        print(f"❌ Error clearing cache: {e}")

if __name__ == "__main__":
    clear_translation_cache()
    print("✨ Done!")
