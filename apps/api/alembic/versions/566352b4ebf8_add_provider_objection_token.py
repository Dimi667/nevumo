"""add_provider_objection_token

Revision ID: 566352b4ebf8
Revises: 518f47fc537f
Create Date: 2026-07-01 12:51:50.536872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '566352b4ebf8'
down_revision: Union[str, Sequence[str], None] = '518f47fc537f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('providers', sa.Column('objection_token', sa.String(64), nullable=True, unique=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('providers', 'objection_token')
