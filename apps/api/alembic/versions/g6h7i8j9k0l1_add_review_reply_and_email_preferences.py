"""add_review_reply_and_email_preferences

Revision ID: g6h7i8j9k0l1
Revises: e4f5g6h7i8j9
Create Date: 2026-04-02

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "g6h7i8j9k0l1"
down_revision = "e4f5g6h7i8j9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add provider reply fields to reviews table
    op.add_column(
        'reviews',
        sa.Column('provider_reply', sa.Text(), nullable=True)
    )
    op.add_column(
        'reviews',
        sa.Column('provider_reply_at', sa.DateTime(), nullable=True)
    )
    op.add_column(
        'reviews',
        sa.Column('provider_reply_edited_at', sa.DateTime(), nullable=True)
    )
    op.add_column(
        'reviews',
        sa.Column('provider_reply_edit_count', sa.Integer(), server_default='0', nullable=False)
    )
    
    # Add index for provider_reply_at for sorting conversations by latest activity
    op.create_index(
        'idx_reviews_provider_reply_at',
        'reviews',
        ['provider_reply_at']
    )
    
    # Add email notification flag to users table (default True = opted in)
    op.add_column(
        'users',
        sa.Column('review_reply_email_enabled', sa.Boolean(), server_default='true', nullable=False)
    )
    
    # Add index for efficient lookup
    op.create_index(
        'idx_users_review_reply_email',
        'users',
        ['review_reply_email_enabled']
    )


def downgrade() -> None:
    # Remove indexes
    op.drop_index('idx_reviews_provider_reply_at', table_name='reviews')
    op.drop_index('idx_users_review_reply_email', table_name='users')
    
    # Remove columns from reviews
    op.drop_column('reviews', 'provider_reply')
    op.drop_column('reviews', 'provider_reply_at')
    op.drop_column('reviews', 'provider_reply_edited_at')
    op.drop_column('reviews', 'provider_reply_edit_count')
    
    # Remove column from users
    op.drop_column('users', 'review_reply_email_enabled')
