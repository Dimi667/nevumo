from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
import os

engine = create_engine(os.environ["DATABASE_URL"], poolclass=NullPool)
with engine.begin() as conn:
    result = conn.execute(text("""
        UPDATE providers
        SET is_claimed = TRUE
        WHERE claim_token = 'e2e-test-claim-2026'
        RETURNING id, business_name, is_claimed, claim_token
    """))
    row = result.fetchone()
    if row:
        print(f"✅ Marked as claimed: {row.business_name}")
        print(f"   id: {row.id}")
        print(f"   is_claimed: {row.is_claimed}")
        print(f"   claim_token: {row.claim_token} (запазен за тест)")
    else:
        print("❌ Provider не е намерен")
