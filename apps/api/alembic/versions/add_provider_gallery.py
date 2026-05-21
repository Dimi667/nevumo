"""add_provider_gallery

Revision ID: add_provider_gallery
Revises: 
Create Date: 2026-05-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_provider_gallery'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = ('20260510_add_locative_genitive', 'add_verification_level')


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'provider_images',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('provider_id', sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['provider_id'], ['providers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_provider_images_provider_id', 'provider_images', ['provider_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_provider_images_provider_id', table_name='provider_images')
    op.drop_table('provider_images')
