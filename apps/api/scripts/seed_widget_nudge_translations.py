#!/usr/bin/env python3
"""
Seed script: copy post-lead nudge keys from category namespace into widget namespace.

Run via:
    docker exec nevumo-api python -m apps.api.scripts.seed_widget_nudge_translations

Logic:
    1. Read existing translations where key starts with 'category.' for the target keys.
    2. Insert/upsert the same values under the 'widget.' prefix.
    3. ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value.
"""

import os
import psycopg2


SOURCE_KEYS = (
    "category.success_title",
    "category.success_subtitle",
    "category.success_track_title",
    "category.success_bullet_responses",
    "category.success_bullet_manage",
    "category.success_bullet_notifications",
    "category.success_cta_email",
    "category.success_free_label",
    "category.success_skip_link",
    "category.email_back_link",
    "category.email_label",
    "category.email_placeholder",
    "category.email_cta_continue",
)


def main() -> None:
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return

    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()

    try:
        print("=== Fetching category translations ===")

        cursor.execute(
            """
            SELECT lang, key, value
            FROM translations
            WHERE key = ANY(%s)
            """,
            (list(SOURCE_KEYS),),
        )
        rows = cursor.fetchall()

        if not rows:
            print("WARNING: No matching category translations found.")
            return

        print(f"Found {len(rows)} category rows to copy.")

        # Prepare upsert values: replace "category." prefix with "widget."
        upsert_values = []
        for lang, key, value in rows:
            widget_key = key.replace("category.", "widget.", 1)
            upsert_values.append((lang, widget_key, value))

        print(f"=== Upserting {len(upsert_values)} widget translations ===")

        cursor.executemany(
            """
            INSERT INTO translations (lang, key, value)
            VALUES (%s, %s, %s)
            ON CONFLICT (lang, key)
            DO UPDATE SET value = EXCLUDED.value
            """,
            upsert_values,
        )

        conn.commit()
        print(f"=== Done. Upserted {len(upsert_values)} rows. ===")

    except Exception as e:
        conn.rollback()
        print(f"ERROR: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
