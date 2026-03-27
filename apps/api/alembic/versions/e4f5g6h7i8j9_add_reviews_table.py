"""add_reviews_table

Revision ID: e4f5g6h7i8j9
Revises: d4e5f6a7b8c9
Create Date: 2026-03-26

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "e4f5g6h7i8j9"
down_revision = "d4e5f6a7b8c9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'reviews',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('provider_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('providers.id', ondelete='CASCADE'), nullable=False),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('lead_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('leads.id', ondelete='SET NULL'), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
        sa.CheckConstraint('rating >= 1 AND rating <= 5', name='ck_reviews_rating_range'),
    )
    op.create_index('idx_reviews_provider', 'reviews', ['provider_id'])
    op.create_index('idx_reviews_client', 'reviews', ['client_id'])
    op.create_unique_constraint('uq_reviews_lead', 'reviews', ['lead_id'])


def downgrade() -> None:
    op.drop_table('reviews')
