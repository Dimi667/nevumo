"""add_cancelled_to_lead_matches_status

Revision ID: cdf063316609
Revises: 38c28e2a6c99
Create Date: 2026-04-24 13:58:07.482555

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdf063316609'
down_revision: Union[str, Sequence[str], None] = '38c28e2a6c99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE lead_matches DROP CONSTRAINT IF EXISTS ck_lead_matches_status")
    op.execute("ALTER TABLE lead_matches ADD CONSTRAINT ck_lead_matches_status CHECK (status IN ('invited', 'accepted', 'rejected', 'contacted', 'done', 'cancelled'))")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE lead_matches DROP CONSTRAINT IF EXISTS ck_lead_matches_status")
    op.execute("ALTER TABLE lead_matches ADD CONSTRAINT ck_lead_matches_status CHECK (status IN ('invited', 'accepted', 'rejected'))")
