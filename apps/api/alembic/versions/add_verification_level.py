"""add_verification_level

Revision ID: add_verification_level
Revises: 0535f00974f4
Create Date: 2026-05-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_verification_level'
down_revision: Union[str, Sequence[str], None] = '1433ea08e073'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('providers', sa.Column('verification_level', sa.Integer(), nullable=False, server_default='0'))
    op.create_index('idx_providers_verification_level', 'providers', ['verification_level'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_providers_verification_level', table_name='providers')
    op.drop_column('providers', 'verification_level')
