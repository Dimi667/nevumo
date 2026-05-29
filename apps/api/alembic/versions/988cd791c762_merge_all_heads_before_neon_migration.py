"""merge_all_heads_before_neon_migration

Revision ID: 988cd791c762
Revises: add_provider_gallery
Create Date: 2026-05-29 13:01:29.949076

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '988cd791c762'
down_revision: Union[str, Sequence[str], None] = 'add_provider_gallery'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
