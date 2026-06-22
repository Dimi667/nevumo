"""merge_all_effective_heads

Revision ID: 83bd0fb9d8ab
Revises: 20260510_add_locative_genitive, 594f989fc403, add_verification_level
Create Date: 2026-06-22 17:17:47.446499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83bd0fb9d8ab'
down_revision: Union[str, Sequence[str], None] = ('20260510_add_locative_genitive', '594f989fc403', 'add_verification_level')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
