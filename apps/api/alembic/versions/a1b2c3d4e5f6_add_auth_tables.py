"""add_auth_tables

Revision ID: a1b2c3d4e5f6
Revises: f4f432ebed54
Create Date: 2026-03-24 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'f4f432ebed54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add auth columns to users
    op.add_column('users', sa.Column('password_hash', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False))

    # 2. password_reset_tokens
    op.create_table(
        'password_reset_tokens',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token_hash', sa.String(), nullable=False, unique=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
    )
    op.create_index('idx_reset_tokens_hash', 'password_reset_tokens', ['token_hash'])
    op.create_index('idx_reset_tokens_user', 'password_reset_tokens', ['user_id'])

    # 3. auth_rate_limits
    op.create_table(
        'auth_rate_limits',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('ip', sa.String(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
    )
    op.create_index('idx_auth_rate_limits_ip_action', 'auth_rate_limits', ['ip', 'action'])
    op.create_index('idx_auth_rate_limits_created', 'auth_rate_limits', ['created_at'])


def downgrade() -> None:
    op.drop_table('auth_rate_limits')
    op.drop_table('password_reset_tokens')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'password_hash')
