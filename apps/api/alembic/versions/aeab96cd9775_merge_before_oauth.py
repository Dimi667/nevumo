"""merge before oauth

Revision ID: aeab96cd9775
Revises: 20260508_add_consent_logs, multi_provider_reviews_001
Create Date: 2026-05-09 14:41:33.112033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aeab96cd9775'
down_revision: Union[str, Sequence[str], None] = ('20260508_add_consent_logs', 'multi_provider_reviews_001')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
