"""merge_all_heads_blocker5

Revision ID: 94e74d75faee
Revises: 20260607_add_push_subscriptions, 20260620_add_city_category_search_volume, 988cd791c762, w1x2y3z4a5b6
Create Date: 2026-06-22 17:11:31.267389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94e74d75faee'
down_revision: Union[str, Sequence[str], None] = ('20260607_add_push_subscriptions', '20260620_add_city_category_search_volume', '988cd791c762', 'w1x2y3z4a5b6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
