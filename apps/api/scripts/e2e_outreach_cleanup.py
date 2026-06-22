from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
import os

engine = create_engine(os.environ["DATABASE_URL"], poolclass=NullPool)
with engine.begin() as conn:
    result = conn.execute(text("""
        DELETE FROM providers
        WHERE data_source = 'e2e_test'
        RETURNING id, business_name
    """))
    rows = result.fetchall()
    if rows:
        for row in rows:
            print(f"✅ Изтрит: {row.business_name} ({row.id})")
    else:
        print("❌ No e2e_test providers found — already cleaned?")
