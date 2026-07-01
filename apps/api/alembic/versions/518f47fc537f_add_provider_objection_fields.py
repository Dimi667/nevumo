"""add_provider_objection_fields

Revision ID: 518f47fc537f
Revises: 20260630_add_claimed_at
Create Date: 2026-07-01 12:41:11.905767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '518f47fc537f'
down_revision: Union[str, Sequence[str], None] = '20260630_add_claimed_at'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('providers', sa.Column('objected_at', sa.TIMESTAMP(timezone=True), nullable=True))
    op.add_column('providers', sa.Column('is_hidden', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('providers', 'is_hidden')
    op.drop_column('providers', 'objected_at')
