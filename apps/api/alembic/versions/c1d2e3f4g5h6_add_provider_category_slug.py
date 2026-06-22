"""add category_slug to providers

Revision ID: c1d2e3f4g5h6
Revises: b1c2d3e4f5g6
Create Date: 2026-06-23
"""
from alembic import op
import sqlalchemy as sa

revision = 'c1d2e3f4g5h6'
down_revision = 'b1c2d3e4f5g6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'providers',
        sa.Column('category_slug', sa.String(50), nullable=True)
    )
    op.create_index(
        'idx_providers_category_slug',
        'providers',
        ['category_slug']
    )


def downgrade() -> None:
    op.drop_index('idx_providers_category_slug', table_name='providers')
    op.drop_column('providers', 'category_slug')
