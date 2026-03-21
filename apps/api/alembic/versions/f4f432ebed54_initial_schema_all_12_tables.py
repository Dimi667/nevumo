"""initial_schema_all_12_tables

Revision ID: f4f432ebed54
Revises:
Create Date: 2026-03-21 12:29:27.424137

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'f4f432ebed54'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('locale', sa.String(), server_default='en'),
        sa.Column('country_code', sa.String(2), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
        sa.CheckConstraint("role IN ('client', 'provider')", name='ck_users_role'),
    )
    op.create_index('idx_users_role', 'users', ['role'])

    # 2. providers
    op.create_table(
        'providers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False),
        sa.Column('business_name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('slug', sa.String(), nullable=False, unique=True),
        sa.Column('rating', sa.Numeric(2, 1), server_default='0'),
        sa.Column('verified', sa.Boolean(), server_default='false'),
        sa.Column('availability_status', sa.String(), server_default='active'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
    )
    op.create_index('idx_providers_rating', 'providers', ['rating'])
    op.create_index('idx_providers_status', 'providers', ['availability_status'])

    # 3. locations
    op.create_table(
        'locations',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('country_code', sa.String(2), nullable=False),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('lat', sa.Numeric(), nullable=True),
        sa.Column('lng', sa.Numeric(), nullable=True),
        sa.UniqueConstraint('country_code', 'slug'),
    )
    op.create_index('idx_locations_country', 'locations', ['country_code'])

    # 4. provider_cities
    op.create_table(
        'provider_cities',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('provider_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('providers.id', ondelete='CASCADE'), nullable=False),
        sa.Column('city_id', sa.Integer(), sa.ForeignKey('locations.id'), nullable=False),
        sa.UniqueConstraint('provider_id', 'city_id'),
    )
    op.create_index('idx_provider_cities_city', 'provider_cities', ['city_id'])

    # 5. categories
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('slug', sa.String(), nullable=False, unique=True),
        sa.Column('parent_id', sa.Integer(), sa.ForeignKey('categories.id'), nullable=True),
    )

    # 6. category_translations
    op.create_table(
        'category_translations',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False),
        sa.Column('lang', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.UniqueConstraint('category_id', 'lang'),
    )

    # 7. services
    op.create_table(
        'services',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('provider_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('providers.id', ondelete='CASCADE'), nullable=False),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id'), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price_type', sa.String(), nullable=True),
        sa.Column('base_price', sa.Numeric(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
        sa.CheckConstraint("price_type IN ('fixed', 'hourly', 'request')", name='ck_services_price_type'),
    )
    op.create_index('idx_services_category', 'services', ['category_id'])
    op.create_index('idx_services_provider', 'services', ['provider_id'])

    # 8. leads
    op.create_table(
        'leads',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('provider_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('providers.id'), nullable=True),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id'), nullable=False),
        sa.Column('city_id', sa.Integer(), sa.ForeignKey('locations.id'), nullable=False),
        sa.Column('phone', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('budget', sa.Numeric(), nullable=True),
        sa.Column('source', sa.String(), nullable=True),
        sa.Column('utm_source', sa.String(), nullable=True),
        sa.Column('utm_campaign', sa.String(), nullable=True),
        sa.Column('landing_page', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='created'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
    )
    op.create_index('idx_leads_category', 'leads', ['category_id'])
    op.create_index('idx_leads_city', 'leads', ['city_id'])
    op.create_index('idx_leads_provider', 'leads', ['provider_id'])
    op.create_index('idx_leads_status', 'leads', ['status'])
    op.create_index('idx_leads_created_at', 'leads', ['created_at'])

    # 9. lead_matches
    op.create_table(
        'lead_matches',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('lead_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('leads.id', ondelete='CASCADE'), nullable=False),
        sa.Column('provider_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('providers.id'), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
        sa.UniqueConstraint('lead_id', 'provider_id'),
        sa.CheckConstraint("status IN ('invited', 'accepted', 'rejected')", name='ck_lead_matches_status'),
    )
    op.create_index('idx_lead_matches_lead', 'lead_matches', ['lead_id'])

    # 10. messages
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('lead_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('leads.id', ondelete='CASCADE'), nullable=False),
        sa.Column('sender_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
    )
    op.create_index('idx_messages_lead', 'messages', ['lead_id'])

    # 11. lead_events
    op.create_table(
        'lead_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('lead_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('leads.id', ondelete='CASCADE'), nullable=False),
        sa.Column('event_type', sa.String(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
    )
    op.create_index('idx_lead_events_lead', 'lead_events', ['lead_id'])

    # 12. lead_rate_limits
    op.create_table(
        'lead_rate_limits',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('ip', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
    )
    op.create_index('idx_rate_limits_ip', 'lead_rate_limits', ['ip'])

    # 13. translations (i18n)
    op.create_table(
        'translations',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('lang', sa.String(), nullable=False),
        sa.Column('key', sa.String(), nullable=False),
        sa.Column('value', sa.String(), nullable=True),
        sa.UniqueConstraint('lang', 'key'),
    )
    op.create_index('idx_translations_lang', 'translations', ['lang'])
    op.create_index('idx_translations_key', 'translations', ['key'])


def downgrade() -> None:
    op.drop_table('translations')
    op.drop_table('lead_rate_limits')
    op.drop_table('lead_events')
    op.drop_table('messages')
    op.drop_table('lead_matches')
    op.drop_table('leads')
    op.drop_table('services')
    op.drop_table('category_translations')
    op.drop_table('categories')
    op.drop_table('provider_cities')
    op.drop_table('locations')
    op.drop_table('providers')
    op.drop_table('users')
