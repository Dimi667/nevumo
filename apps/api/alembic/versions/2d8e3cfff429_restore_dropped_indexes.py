"""restore_dropped_indexes

Revision ID: 2d8e3cfff429
Revises: ff8bc78d912a
Create Date: 2026-06-29 22:30:19.889686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d8e3cfff429'
down_revision: Union[str, Sequence[str], None] = 'ff8bc78d912a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index('idx_provider_images_provider_id', 'provider_images', ['provider_id'])
    op.create_index('idx_providers_verification_level', 'providers', ['verification_level'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_provider_images_provider_id', table_name='provider_images')
    op.drop_index('idx_providers_verification_level', table_name='providers')
