"""merge_final

Revision ID: 594f989fc403
Revises: 7fdeb3d5efba
Create Date: 2026-06-22 17:15:53.471088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '594f989fc403'
down_revision: Union[str, Sequence[str], None] = '7fdeb3d5efba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
