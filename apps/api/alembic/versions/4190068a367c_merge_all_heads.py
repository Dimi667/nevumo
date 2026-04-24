"""merge_all_heads

Revision ID: 4190068a367c
Revises: f392cf5231ba
Create Date: 2026-04-24 10:38:44.767586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4190068a367c'
down_revision: Union[str, Sequence[str], None] = 'f392cf5231ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
