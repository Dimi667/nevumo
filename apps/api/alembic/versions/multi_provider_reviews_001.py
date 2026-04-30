"""multi_provider_reviews

Revision ID: multi_provider_reviews_001
Revises: 0535f00974f4
Create Date: 2026-04-30 17:31:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'multi_provider_reviews_001'
down_revision = 'a2b3c4d5e6f7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Drop constraint UNIQUE(lead_id) on reviews table
    # Using SQL directly for IF EXISTS support in PostgreSQL
    op.execute('ALTER TABLE reviews DROP CONSTRAINT IF EXISTS uq_reviews_lead')
    
    # 2. Add constraint UNIQUE(lead_id, provider_id) on reviews table
    # Using SQL directly for IF NOT EXISTS support (PostgreSQL 9.5+)
    # Note: For constraints, we usually check if it exists first or just try to create it.
    # PostgreSQL doesn't have 'ADD CONSTRAINT IF NOT EXISTS', so we use a subquery check or just standard Alembic with error handling if we wanted, 
    # but here we can just check existence.
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint WHERE conname = 'uq_reviews_lead_provider'
            ) THEN
                ALTER TABLE reviews ADD CONSTRAINT uq_reviews_lead_provider UNIQUE (lead_id, provider_id);
            END IF;
        END $$;
    """)


def downgrade() -> None:
    op.execute('ALTER TABLE reviews DROP CONSTRAINT IF EXISTS uq_reviews_lead_provider')
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint WHERE conname = 'uq_reviews_lead'
            ) THEN
                ALTER TABLE reviews ADD CONSTRAINT uq_reviews_lead UNIQUE (lead_id);
            END IF;
        END $$;
    """)
