"""merge_heads

Revision ID: f392cf5231ba
Revises: r2s3t4u5v6w7
Create Date: 2026-04-24 10:38:23.536750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f392cf5231ba'
down_revision: Union[str, Sequence[str], None] = 'r2s3t4u5v6w7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
