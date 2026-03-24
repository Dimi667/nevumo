"""update status check constraints

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-03-24

"""
from alembic import op

revision = "c3d4e5f6a7b8"
down_revision = "b2c3d4e5f6a7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # lead_matches: expand status to include contacted, done
    # Use raw SQL with IF EXISTS to avoid transaction abort on missing constraint
    op.execute("ALTER TABLE lead_matches DROP CONSTRAINT IF EXISTS ck_lead_matches_status")
    op.create_check_constraint(
        "ck_lead_matches_status",
        "lead_matches",
        "status IN ('invited', 'contacted', 'done', 'rejected')",
    )

    # leads: add status CHECK constraint (none existed before)
    op.execute("ALTER TABLE leads DROP CONSTRAINT IF EXISTS ck_leads_status")
    op.create_check_constraint(
        "ck_leads_status",
        "leads",
        "status IN ('created', 'pending_match', 'matched', 'contacted', 'done', 'expired', 'cancelled', 'rejected')",
    )


def downgrade() -> None:
    op.execute("ALTER TABLE leads DROP CONSTRAINT IF EXISTS ck_leads_status")
    op.execute("ALTER TABLE lead_matches DROP CONSTRAINT IF EXISTS ck_lead_matches_status")
    op.create_check_constraint(
        "ck_lead_matches_status",
        "lead_matches",
        "status IN ('invited', 'accepted', 'rejected')",
    )
