"""add outreach_sequence_log table

Revision ID: w1x2y3z4a5b6
Revises: v1w2x3y4z5a6
Create Date: 2026-06-22
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

revision = "w1x2y3z4a5b6"
down_revision = "v1w2x3y4z5a6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "outreach_sequence_log",
        sa.Column(
            "id",
            PG_UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("business_name", sa.Text(), nullable=True),
        sa.Column("category", sa.Text(), nullable=True),
        sa.Column("sequence_step", sa.Integer(), nullable=False),
        sa.Column("resend_message_id", sa.Text(), nullable=True),
        sa.Column(
            "sent_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.Column("status", sa.Text(), nullable=False, server_default="sent"),
        sa.UniqueConstraint("email", "sequence_step", name="uq_outreach_seq_email_step"),
    )
    op.create_index("idx_outreach_seq_email", "outreach_sequence_log", ["email"])


def downgrade() -> None:
    op.drop_index("idx_outreach_seq_email", table_name="outreach_sequence_log")
    op.drop_table("outreach_sequence_log")
