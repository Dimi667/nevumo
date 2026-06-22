"""add scraped_email and pending_claim_verifications

Revision ID: b1c2d3e4f5g6
Revises: 83bd0fb9d8ab
Create Date: 2026-06-22
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = 'b1c2d3e4f5g6'
down_revision = '83bd0fb9d8ab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add scraped_email to providers
    op.add_column(
        'providers',
        sa.Column('scraped_email', sa.Text(), nullable=True)
    )

    # 2. Create pending_claim_verifications table
    op.create_table(
        'pending_claim_verifications',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('claim_token', sa.Text(), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
        sa.Column('code', sa.Text(), nullable=False),
        sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('used', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('idx_pending_claim_verif_token', 'pending_claim_verifications', ['claim_token'])
    op.create_index('idx_pending_claim_verif_user', 'pending_claim_verifications', ['user_id'])
    op.create_index('idx_pending_claim_verif_expires', 'pending_claim_verifications', ['expires_at'])


def downgrade() -> None:
    op.drop_table('pending_claim_verifications')
    op.drop_column('providers', 'scraped_email')
