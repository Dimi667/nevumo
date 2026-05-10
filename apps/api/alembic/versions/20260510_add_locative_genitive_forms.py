from alembic import op
revision = '20260510_add_locative_genitive'
down_revision = 'loctrans001'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
        ALTER TABLE location_translations ADD COLUMN IF NOT EXISTS locative_form TEXT;
    """)
    op.execute("""
        ALTER TABLE location_translations ADD COLUMN IF NOT EXISTS genitive_form TEXT;
    """)

def downgrade():
    op.execute("ALTER TABLE location_translations DROP COLUMN IF EXISTS locative_form;")
    op.execute("ALTER TABLE location_translations DROP COLUMN IF EXISTS genitive_form;")
