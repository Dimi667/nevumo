"""merge provider translations with main

Revision ID: 902751cf3c7d
Revises: c1a2b3d4e5f6, t1u2v3w4x5y6
Create Date: 2026-04-07 15:53:52.298402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '902751cf3c7d'
down_revision: Union[str, Sequence[str], None] = ('c1a2b3d4e5f6', 't1u2v3w4x5y6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
