"""
Seed script: adds claim.vs_competitor_label translation key in all 34 languages.
Run: railway run python3.13 -m apps.api.scripts.seed_claim_vs_competitor_label
"""

import os
import psycopg2
from psycopg2.extras import execute_values

DATABASE_URL = os.environ["DATABASE_URL"]

TRANSLATIONS = [
    ("bg",    "Традиционни платформи"),
    ("cs",    "Tradiční platformy"),
    ("da",    "Traditionelle platforme"),
    ("de",    "Traditionelle Plattformen"),
    ("el",    "Παραδοσιακές πλατφόρμες"),
    ("en",    "Traditional platforms"),
    ("es",    "Plataformas tradicionales"),
    ("et",    "Traditsioonilised platvormid"),
    ("fi",    "Perinteiset alustat"),
    ("fr",    "Plateformes traditionnelles"),
    ("ga",    "Ardáin traidisiúnta"),
    ("hr",    "Tradicionalne platforme"),
    ("hu",    "Hagyományos platformok"),
    ("is",    "Hefðbundnar vettvangur"),
    ("it",    "Piattaforme tradizionali"),
    ("lb",    "Traditionell Plattformen"),
    ("lt",    "Tradicinės platformos"),
    ("lv",    "Tradicionālās platformas"),
    ("mk",    "Традиционални платформи"),
    ("mt",    "Pjattaformi tradizzjonali"),
    ("nl",    "Traditionele platforms"),
    ("no",    "Tradisjonelle plattformer"),
    ("pl",    "Tradycyjne platformy"),
    ("pt",    "Plataformas tradicionais"),
    ("pt-PT", "Plataformas tradicionais"),
    ("ro",    "Platforme tradiționale"),
    ("ru",    "Традиционные платформы"),
    ("sk",    "Tradičné platformy"),
    ("sl",    "Tradicionalne platforme"),
    ("sq",    "Platformat tradicionale"),
    ("sr",    "Традиционалне платформе"),
    ("sv",    "Traditionella plattformar"),
    ("tr",    "Geleneksel platformlar"),
    ("uk",    "Традиційні платформи"),
]

def main() -> None:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    rows_to_upsert = []
    for lang, value in TRANSLATIONS:
        full_key = "claim.vs_competitor_label"
        rows_to_upsert.append((lang, full_key, value))

    execute_values(
        cur,
        """
        INSERT INTO translations (lang, key, value)
        VALUES %s
        ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
        """,
        rows_to_upsert,
        template="(%s, %s, %s)",
    )

    conn.commit()
    cur.execute(
        "SELECT COUNT(*) FROM translations WHERE key = 'claim.vs_competitor_label'"
    )
    count = cur.fetchone()[0]
    print(f"✅ vs_competitor_label seeded: {count}/34 languages")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
