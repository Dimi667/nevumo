"""
seed_cookies_table_data_p1.py — Nevumo | namespace: cookies
Section 5 (type/retention), Section 7 (roles), Section 8 (safeguards/country) — EN only
Run: docker exec nevumo-api python -m apps.api.scripts.seed_cookies_table_data_p1
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nevumo:nevumo@postgres:5432/nevumo_leads",
)

NAMESPACE = "cookies"

TRANSLATIONS: dict[str, dict[str, str]] = {

    # ── Section 5 · Storage types (shared enum keys) ──────────────────────
    "s5_type_cookie_1p":      {"en": "Cookie (first-party)"},
    "s5_type_cookie_3p":      {"en": "Cookie (third-party)"},
    "s5_type_localstorage":   {"en": "Local Storage"},
    "s5_type_sessionstorage": {"en": "Session Storage"},

    # ── Section 5 · Retention values ──────────────────────────────────────
    "s5_ret_12mo":        {"en": "12 months"},
    "s5_ret_13mo":        {"en": "13 months"},
    "s5_ret_1y":          {"en": "1 year"},
    "s5_ret_30d":         {"en": "30 days"},
    "s5_ret_30min":       {"en": "30 minutes"},
    "s5_ret_sess_30d":    {"en": "Session / 30 days"},
    "s5_ret_cleared":     {"en": "Until cleared"},
    "s5_ret_session":     {"en": "Session"},
    "s5_ret_session_tab": {"en": "Session (tab)"},

    # ── Section 7 · Processor roles ───────────────────────────────────────
    "s7_role_google":     {"en": "Analytics (GA4)"},
    "s7_role_stripe":     {"en": "Payment processing (fraud prevention)"},
    "s7_role_vercel":     {"en": "Frontend hosting"},
    "s7_role_railway":    {"en": "Backend API hosting"},
    "s7_role_neon":       {"en": "PostgreSQL database hosting"},
    "s7_role_upstash":    {"en": "Redis cache hosting"},
    "s7_role_cloudflare": {"en": "Media storage (R2)"},

    # ── Section 8 · Safeguards & country ──────────────────────────────────
    "s8_safeguard_sccs_dpf": {"en": "SCCs + EU-US DPF"},
    "s8_safeguard_sccs":     {"en": "SCCs"},
    "s8_country_usa":        {"en": "USA"},
}


def seed() -> None:
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        count = 0
        for key, lang_values in TRANSLATIONS.items():
            db_key = f"{NAMESPACE}.{key}"
            for lang, value in lang_values.items():
                session.execute(
                    text(
                        "INSERT INTO translations (lang, key, value) "
                        "VALUES (:lang, :key, :value) "
                        "ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value"
                    ),
                    {"lang": lang, "key": db_key, "value": value},
                )
                count += 1
        session.commit()
        print(f"✅ seed_cookies_table_data_p1: {count} rows upserted ({NAMESPACE})")

    engine.dispose()


if __name__ == "__main__":
    seed()
