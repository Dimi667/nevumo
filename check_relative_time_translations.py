#!/usr/bin/env python3
"""Проверка на новите ключове за относително време в PostgreSQL."""

import psycopg2

DATABASE_URL = "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads"

# Ключове за проверка
TARGET_KEYS = [
    "widget.time_just_now",
    "widget.time_week_ago_many",
    "widget.time_month_ago_many",
]

# Езици за проверка
TARGET_LANGS = ["bg", "en", "sr"]


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    print("=" * 70)
    print("ПРОВЕРКА НА НОВИТЕ КЛЮЧЕ ЗА ОТНОСИТЕЛНО ВРЕМЕ")
    print("=" * 70)

    # 1. Проверка на конкретните ключове за конкретните езици
    print("\n📋 КОНКРЕТНИ ЗАПИСИ ЗА ПРОВЕРКА (bg, en, sr):")
    print("-" * 70)
    
    for key in TARGET_KEYS:
        print(f"\n🔑 Ключ: {key}")
        for lang in TARGET_LANGS:
            cur.execute(
                "SELECT key, lang, value FROM translations WHERE key = %s AND lang = %s",
                (key, lang)
            )
            row = cur.fetchone()
            if row:
                print(f"  ✅ {lang}: {row[2]}")
            else:
                print(f"  ❌ {lang}: ЛИПСВА!")

    # 2. Проверка на всички widget.time_* ключове
    print("\n\n📊 ВСИЧКИ widget.time_* КЛЮЧЕ В БАЗАТА:")
    print("-" * 70)
    
    cur.execute(
        "SELECT key, lang, value FROM translations WHERE key LIKE 'widget.time_%' ORDER BY key, lang"
    )
    rows = cur.fetchall()
    
    if rows:
        # Групиране по ключ
        from collections import defaultdict
        key_langs = defaultdict(list)
        for key, lang, value in rows:
            key_langs[key].append((lang, value))
        
        for key in sorted(key_langs.keys()):
            print(f"\n🔑 {key}")
            for lang, value in sorted(key_langs[key], key=lambda x: x[0]):
                print(f"  {lang}: {value}")
    else:
        print("❌ Няма намерени widget.time_* ключове!")

    # 3. Общ брой записи за widget.time_*
    cur.execute(
        "SELECT COUNT(*) FROM translations WHERE key LIKE 'widget.time_%'"
    )
    count = cur.fetchone()[0]
    
    print("\n\n" + "=" * 70)
    print("ОБОЩЕНИЕ")
    print("=" * 70)
    print(f"Общ брой записи за widget.time_*: {count}")
    print(f"Очакван брой: 272")
    
    if count == 272:
        print("✅ БРОЯТ СЪОТВЕТСТВА НА ОЧАКВАНИЯ!")
    else:
        print(f"⚠️  БРОЯТ НЕ СЪОТВЕТСТВА! Разлика: {272 - count}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
