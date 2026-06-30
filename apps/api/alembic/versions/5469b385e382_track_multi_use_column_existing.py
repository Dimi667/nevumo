"""track_multi_use_column_existing

Revision ID: 5469b385e382
Revises: 2d8e3cfff429
Create Date: 2026-06-30 13:21:10.867914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5469b385e382'
down_revision: Union[str, Sequence[str], None] = '2d8e3cfff429'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema. No-op: multi_use column was already added via direct SQL.
    This migration exists only to mark the alembic_version state correctly."""
    pass


def downgrade() -> None:
    """No-op downgrade."""
    pass
