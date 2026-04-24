"""merge_heads

Revision ID: 38c28e2a6c99
Revises: 0535f00974f4, ac57f93d96b6
Create Date: 2026-04-24 07:43:22.409968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38c28e2a6c99'
down_revision: Union[str, Sequence[str], None] = ('0535f00974f4', 'ac57f93d96b6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
