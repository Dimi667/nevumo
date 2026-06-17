from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
import os

engine = create_engine(os.environ["DATABASE_URL"], poolclass=NullPool)
with engine.begin() as conn:
    result = conn.execute(text("""
        DELETE FROM providers
        WHERE slug = 'test-hydraulik-testowski-e2e'
        RETURNING id, business_name
    """))
    row = result.fetchone()
    if row:
        print(f"✅ Изтрит: {row.business_name} ({row.id})")
    else:
        print("❌ Provider не е намерен — вече изтрит?")
