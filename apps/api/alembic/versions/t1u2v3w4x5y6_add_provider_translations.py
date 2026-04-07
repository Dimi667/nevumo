"""Add provider translations table

Revision ID: t1u2v3w4x5y6
Revises: p1q2r3s4t5u6
Create Date: 2026-04-07
"""

revision = 't1u2v3w4x5y6'
down_revision = 'p1q2r3s4t5u6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("""
        CREATE TABLE IF NOT EXISTS provider_translations (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            provider_id UUID NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
            field TEXT NOT NULL,
            lang TEXT NOT NULL,
            value TEXT NOT NULL,
            auto_translated BOOLEAN NOT NULL DEFAULT TRUE,
            source_lang TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(provider_id, field, lang)
        );
    """)
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_provider_translations_provider ON provider_translations(provider_id);
    """)
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_provider_translations_lang ON provider_translations(lang);
    """)
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_provider_translations_auto ON provider_translations(auto_translated);
    """)


def downgrade():
    op.execute("DROP TABLE IF EXISTS provider_translations;")
