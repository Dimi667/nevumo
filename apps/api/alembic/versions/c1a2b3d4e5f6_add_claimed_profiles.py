"""Add claimed profiles support to providers

Revision ID: c1a2b3d4e5f6
Revises: 20260406_204817
Create Date: 2026-04-07 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'c1a2b3d4e5f6'
down_revision: Union[str, None] = '20260406_204817'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Make user_id nullable (allow unclaimed profiles)
    op.execute("""
        ALTER TABLE providers ALTER COLUMN user_id DROP NOT NULL;
    """)

    # 2. Add is_claimed column
    op.execute("""
        ALTER TABLE providers 
        ADD COLUMN IF NOT EXISTS is_claimed BOOLEAN NOT NULL DEFAULT TRUE;
    """)

    # 3. Add claim_token column for magic claim links
    op.execute("""
        ALTER TABLE providers 
        ADD COLUMN IF NOT EXISTS claim_token TEXT;
    """)

    # 4. Add data_source column to track origin
    op.execute("""
        ALTER TABLE providers 
        ADD COLUMN IF NOT EXISTS data_source TEXT NOT NULL DEFAULT 'manual';
    """)

    # 5. Create unique index on claim_token (only for non-null values)
    op.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_providers_claim_token 
        ON providers(claim_token) WHERE claim_token IS NOT NULL;
    """)

    # 6. Create index on is_claimed for filtering
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_providers_is_claimed 
        ON providers(is_claimed);
    """)

    # 7. Backfill existing rows (ensure defaults are applied)
    op.execute("""
        UPDATE providers 
        SET is_claimed = TRUE, data_source = 'manual' 
        WHERE is_claimed IS NULL;
    """)


def downgrade() -> None:
    # 1. Drop claim_token index
    op.execute("""
        DROP INDEX IF EXISTS idx_providers_claim_token;
    """)

    # 2. Drop is_claimed index
    op.execute("""
        DROP INDEX IF EXISTS idx_providers_is_claimed;
    """)

    # 3. Drop data_source column
    op.execute("""
        ALTER TABLE providers DROP COLUMN IF EXISTS data_source;
    """)

    # 4. Drop claim_token column
    op.execute("""
        ALTER TABLE providers DROP COLUMN IF EXISTS claim_token;
    """)

    # 5. Drop is_claimed column
    op.execute("""
        ALTER TABLE providers DROP COLUMN IF EXISTS is_claimed;
    """)

    # 6. Restore user_id NOT NULL constraint
    op.execute("""
        ALTER TABLE providers ALTER COLUMN user_id SET NOT NULL;
    """)
