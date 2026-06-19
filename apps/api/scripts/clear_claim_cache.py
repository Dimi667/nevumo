"""
One-time utility: clears Redis cache for claim namespace across all languages.
Run: railway run python3.13 -m apps.api.scripts.clear_claim_cache
"""

import os

def main() -> None:
    try:
        import redis
        redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB", 0)),
            decode_responses=True,
        )
        redis_client.ping()
        
        keys = redis_client.keys("translations:*:claim")
        if keys:
            redis_client.delete(*keys)
            print(f"✅ Cleared {len(keys)} claim cache keys")
        else:
            print("ℹ️ No claim cache keys found (already expired or never cached)")
    except ImportError:
        print("⚠️ Redis module not available")
    except Exception as e:
        print(f"⚠️ Error clearing cache: {e}")

if __name__ == "__main__":
    main()
