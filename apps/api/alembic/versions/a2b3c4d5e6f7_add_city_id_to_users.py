"""Add city_id to users

Revision ID: a2b3c4d5e6f7
Revises: cdf063316609
Create Date: 2026-04-29 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2b3c4d5e6f7'
down_revision: Union[str, None] = 'cdf063316609'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE users ADD COLUMN IF NOT EXISTS city_id INTEGER REFERENCES locations(id);
    """)
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_city_id ON users(city_id);
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_users_city_id;")
    op.execute("ALTER TABLE users DROP COLUMN IF EXISTS city_id;")
