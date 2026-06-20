"""Add city_category_search_volume table with Warsaw data

Revision ID: 20260620_add_city_category_search_volume
Revises: c1a2b3d4e5f6
Create Date: 2026-06-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '20260620_add_city_category_search_volume'
down_revision: Union[str, None] = 'c1a2b3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create city_category_search_volume table
    op.execute("""
        CREATE TABLE IF NOT EXISTS city_category_search_volume (
            city_slug TEXT NOT NULL,
            category_slug TEXT NOT NULL,
            search_volume INTEGER NOT NULL,
            PRIMARY KEY (city_slug, category_slug)
        );
    """)

    # 2. Seed Warsaw data with INSERT ... ON CONFLICT for idempotency
    op.execute("""
        INSERT INTO city_category_search_volume (city_slug, category_slug, search_volume)
        VALUES 
            ('warsaw', 'cleaning', 7000),
            ('warsaw', 'plumbing', 5400),
            ('warsaw', 'massage', 6900)
        ON CONFLICT (city_slug, category_slug) 
        DO UPDATE SET search_volume = EXCLUDED.search_volume;
    """)


def downgrade() -> None:
    # Drop the table
    op.execute("""
        DROP TABLE IF EXISTS city_category_search_volume;
    """)
