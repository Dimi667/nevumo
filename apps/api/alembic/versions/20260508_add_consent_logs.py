"""Add consent_logs table for GDPR compliance

Revision ID: 20260508_add_consent_logs
Revises: 20260406_204817
Create Date: 2026-05-08 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260508_add_consent_logs'
down_revision: Union[str, None] = '20260406_204817'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create consent_logs table with idempotent SQL
    op.execute("""
        CREATE TABLE IF NOT EXISTS consent_logs (
            id SERIAL PRIMARY KEY,
            user_id UUID REFERENCES users(id) ON DELETE SET NULL,
            session_hash VARCHAR(64) NOT NULL,
            ip_hash VARCHAR(64) NOT NULL,
            categories JSONB NOT NULL,
            policy_version VARCHAR(20) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """)
    
    # Create indexes with idempotent SQL
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_consent_logs_user_id ON consent_logs(user_id);
    """)
    
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_consent_logs_created_at ON consent_logs(created_at);
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS consent_logs;")
