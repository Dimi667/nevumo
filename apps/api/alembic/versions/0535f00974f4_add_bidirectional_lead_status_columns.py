"""add_bidirectional_lead_status_columns

Revision ID: 0535f00974f4
Revises: 4190068a367c
Create Date: 2026-04-24 10:39:08.228873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0535f00974f4'
down_revision: Union[str, Sequence[str], None] = '4190068a367c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('leads', sa.Column('cancelled_by', sa.Text(), nullable=True))
    op.add_column('leads', sa.Column('status_changed_by', sa.Text(), server_default='system', nullable=False))
    op.add_column('leads', sa.Column('status_changed_at', sa.DateTime(), nullable=True))

    op.create_check_constraint(
        'ck_leads_cancelled_by',
        'leads',
        "cancelled_by IN ('client', 'provider')"
    )
    op.create_check_constraint(
        'ck_leads_status_changed_by',
        'leads',
        "status_changed_by IN ('system', 'client', 'provider')"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('ck_leads_status_changed_by', 'leads', type_='check')
    op.drop_constraint('ck_leads_cancelled_by', 'leads', type_='check')
    op.drop_column('leads', 'status_changed_at')
    op.drop_column('leads', 'status_changed_by')
    op.drop_column('leads', 'cancelled_by')
