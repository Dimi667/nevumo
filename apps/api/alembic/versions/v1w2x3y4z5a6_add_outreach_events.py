"""add outreach_events table

Revision ID: v1w2x3y4z5a6
Revises: u1v2w3x4y5z6
Create Date: 2026-06-22
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

revision = "v1w2x3y4z5a6"
down_revision = "u1v2w3x4y5z6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "outreach_events",
        sa.Column(
            "id",
            PG_UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("resend_message_id", sa.Text(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )
    op.create_index("idx_outreach_events_email", "outreach_events", ["email"])
    op.create_index("idx_outreach_events_type", "outreach_events", ["event_type"])
    op.create_index("idx_outreach_events_occurred", "outreach_events", ["occurred_at"])


def downgrade() -> None:
    op.drop_index("idx_outreach_events_occurred", table_name="outreach_events")
    op.drop_index("idx_outreach_events_type", table_name="outreach_events")
    op.drop_index("idx_outreach_events_email", table_name="outreach_events")
    op.drop_table("outreach_events")
