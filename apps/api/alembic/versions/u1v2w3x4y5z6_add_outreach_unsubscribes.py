"""add outreach_unsubscribes table

Revision ID: u1v2w3x4y5z6
Revises: t1u2v3w4x5y6
Create Date: 2026-06-22

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "u1v2w3x4y5z6"
down_revision = "t1u2v3w4x5y6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "outreach_unsubscribes",
        sa.Column("email", sa.Text(), primary_key=True, nullable=False),
        sa.Column(
            "unsubscribed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "reason IN ('user_request', 'bounce', 'complaint')",
            name="ck_outreach_unsub_reason",
        ),
    )


def downgrade() -> None:
    op.drop_table("outreach_unsubscribes")
