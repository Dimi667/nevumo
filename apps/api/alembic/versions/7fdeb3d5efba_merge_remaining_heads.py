"""merge_remaining_heads

Revision ID: 7fdeb3d5efba
Revises: 94e74d75faee
Create Date: 2026-06-22 17:14:43.726468

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fdeb3d5efba'
down_revision: Union[str, Sequence[str], None] = '94e74d75faee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
