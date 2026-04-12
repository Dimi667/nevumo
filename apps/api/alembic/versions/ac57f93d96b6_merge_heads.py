"""merge heads

Revision ID: ac57f93d96b6
Revises: 902751cf3c7d, loctrans001
Create Date: 2026-04-12 12:32:57.734228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac57f93d96b6'
down_revision: Union[str, Sequence[str], None] = ('902751cf3c7d', 'loctrans001')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
