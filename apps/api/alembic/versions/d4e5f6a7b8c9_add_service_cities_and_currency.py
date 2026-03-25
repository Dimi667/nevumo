"""add service_cities table and currency column to services

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-03-25

"""
from alembic import op

revision = "d4e5f6a7b8c9"
down_revision = "c3d4e5f6a7b8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Drop price_type CHECK constraint — validation is in Pydantic; per_sqm is now valid.
    op.execute("ALTER TABLE services DROP CONSTRAINT IF EXISTS ck_services_price_type")

    # 2. Add currency column (idempotent: skip if already present)
    op.execute("""
        ALTER TABLE services
        ADD COLUMN IF NOT EXISTS currency TEXT NOT NULL DEFAULT 'EUR'
    """)

    # 3. Create service_cities junction table (idempotent)
    op.execute("""
        CREATE TABLE IF NOT EXISTS service_cities (
            id SERIAL PRIMARY KEY,
            service_id UUID NOT NULL REFERENCES services(id) ON DELETE CASCADE,
            city_id INT NOT NULL REFERENCES locations(id),
            CONSTRAINT uq_service_cities UNIQUE (service_id, city_id)
        )
    """)

    # 4. Indexes (idempotent)
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_service_cities_service ON service_cities(service_id)
    """)
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_service_cities_city ON service_cities(city_id)
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_service_cities_city")
    op.execute("DROP INDEX IF EXISTS idx_service_cities_service")
    op.execute("DROP TABLE IF EXISTS service_cities")
    op.execute("ALTER TABLE services DROP COLUMN IF EXISTS currency")
    op.execute("""
        ALTER TABLE services
        ADD CONSTRAINT ck_services_price_type
        CHECK (price_type IN ('fixed', 'hourly', 'request'))
    """)
