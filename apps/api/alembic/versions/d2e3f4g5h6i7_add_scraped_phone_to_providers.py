"""add scraped_phone to providers

Revision ID: d2e3f4g5h6i7
Revises: c1d2e3f4g5h6
Create Date: 2026-06-26
"""
from alembic import op
import sqlalchemy as sa

revision = 'd2e3f4g5h6i7'
down_revision = 'c1d2e3f4g5h6'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('providers',
        sa.Column('scraped_phone', sa.Text(), nullable=True)
    )

def downgrade() -> None:
    op.drop_column('providers', 'scraped_phone')
