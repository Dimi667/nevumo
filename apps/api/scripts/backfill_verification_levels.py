"""Backfill verification_level for all existing providers."""
from apps.api.database import SessionLocal
from apps.api.models import Provider
from apps.api.services.provider_service import calculate_verification_level

def run():
    db = SessionLocal()
    try:
        providers = db.query(Provider).all()
        updated = 0
        for p in providers:
            level = calculate_verification_level(p, db)
            if p.verification_level != level:
                p.verification_level = level
                updated += 1
        db.commit()
        print(f"Backfilled {updated} providers.")
    finally:
        db.close()

if __name__ == "__main__":
    run()
