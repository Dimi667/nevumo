"""add_slug_history_and_redirects

Revision ID: f5g6h7i8j9k0
Revises: e4f5g6h7i8j9
Create Date: 2026-03-27

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "f5g6h7i8j9k0"
down_revision = "e4f5g6h7i8j9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "providers",
        sa.Column("slug_change_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
    )

    op.create_table(
        "provider_slug_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("provider_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("providers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("old_slug", sa.String(length=255), nullable=False),
        sa.Column("new_slug", sa.String(length=255), nullable=False),
        sa.Column("changed_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("ip_address", postgresql.INET(), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
    )
    op.create_index(
        "idx_provider_slug_history_provider_changed",
        "provider_slug_history",
        ["provider_id", "changed_at"],
    )
    op.create_index(
        "idx_provider_slug_history_old_slug",
        "provider_slug_history",
        ["old_slug"],
    )

    op.create_table(
        "url_redirects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("provider_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("providers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("old_slug", sa.String(length=255), nullable=False),
        sa.Column("new_slug", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("TRUE")),
        sa.UniqueConstraint("provider_id", "old_slug", name="uq_url_redirects_provider_old_slug"),
    )
    op.create_index(
        "idx_url_redirects_old_slug_active",
        "url_redirects",
        ["old_slug", "active"],
    )

    op.alter_column("providers", "slug_change_count", server_default=None)


def downgrade() -> None:
    op.drop_index("idx_url_redirects_old_slug_active", table_name="url_redirects")
    op.drop_table("url_redirects")

    op.drop_index("idx_provider_slug_history_old_slug", table_name="provider_slug_history")
    op.drop_index("idx_provider_slug_history_provider_changed", table_name="provider_slug_history")
    op.drop_table("provider_slug_history")

    op.drop_column("providers", "slug_change_count")
