from alembic import op
revision = 'loctrans001'
down_revision = '20260406_204817'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
        ALTER TABLE locations ADD COLUMN IF NOT EXISTS city_en TEXT;
    """)
    op.execute("""
        UPDATE locations SET city_en = 'Sofia' WHERE slug = 'sofia';
        UPDATE locations SET city_en = 'Belgrade' WHERE slug = 'belgrade';
        UPDATE locations SET city_en = 'Warsaw' WHERE slug = 'warszawa';
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS location_translations (
            id SERIAL PRIMARY KEY,
            location_id INTEGER NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
            lang TEXT NOT NULL,
            city_name TEXT NOT NULL,
            UNIQUE(location_id, lang)
        );
        CREATE INDEX IF NOT EXISTS idx_location_translations_location ON location_translations(location_id);
        CREATE INDEX IF NOT EXISTS idx_location_translations_lang ON location_translations(lang);
    """)

def downgrade():
    op.execute("DROP TABLE IF EXISTS location_translations;")
    op.execute("ALTER TABLE locations DROP COLUMN IF EXISTS city_en;")
