"""Add magic_link_tokens table

Revision ID: 20260406_204817
Revises: 20260406_204326
Create Date: 2025-04-06 20:48:17.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260406_204817'
down_revision: Union[str, None] = '20260406_204326'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create magic_link_tokens table with idempotent SQL
    op.execute("""
        CREATE TABLE IF NOT EXISTS magic_link_tokens (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email TEXT NOT NULL,
            lead_id UUID REFERENCES leads(id) ON DELETE SET NULL,
            token_hash TEXT NOT NULL UNIQUE,
            expires_at TIMESTAMP NOT NULL,
            used_at TIMESTAMP,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
    """)
    
    # Create indexes with idempotent SQL
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_magic_tokens_hash ON magic_link_tokens(token_hash);
    """)
    
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_magic_tokens_email ON magic_link_tokens(email);
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS magic_link_tokens;")
