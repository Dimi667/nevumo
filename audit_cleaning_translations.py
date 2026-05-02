#!/usr/bin/env python3
"""
Глобален одит на преводите за категория cleaning за всички 34 езика.
Само четене - без промени по базата данни.
"""

import psycopg2
import json
from collections import defaultdict
from typing import Set, Dict, List, Tuple

# Database connection settings
DB_HOST = "localhost"
DB_PORT = 5433
DB_NAME = "nevumo_leads"
DB_USER = "nevumo"
DB_PASSWORD = "nevumo"

def get_connection():
    """Създава връзка с PostgreSQL"""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def get_all_languages(conn) -> List[str]:
    """Извлича всички езикови кодове от базата"""
    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT lang FROM translations ORDER BY lang;")
        return [row[0] for row in cur.fetchall()]

def get_cleaning_keys_for_lang(conn, lang: str) -> Set[str]:
    """Извлича всички ключове за категория cleaning за даден език"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT key FROM translations 
            WHERE lang = %s 
            AND (key LIKE %s OR key LIKE %s OR key LIKE %s)
            ORDER BY key;
        """, (lang, 'cleaning%', '%cleaning%', '%_cleaning_%'))
        return {row[0] for row in cur.fetchall()}

def get_translation_value(conn, lang: str, key: str) -> str:
    """Извлича стойността на превод за даден език и ключ"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT value FROM translations 
            WHERE lang = %s AND key = %s;
        """, (lang, key))
        row = cur.fetchone()
        return row[0] if row else None

def check_english_in_non_english(value: str, lang: str) -> bool:
    """Проверява дали текстът е на английски в не-английски език"""
    if not value or lang == 'en':
        return False
    
    # Списък с английски думи, които не трябва да се появяват в преводите
    english_indicators = [
        'Cleaning', 'cleaning',
        'Frequently Asked Questions', 'FAQ',
        'Price on request', 'price on request',
        'Professional', 'professional',
        'Services', 'services',
        'Home', 'home',
        'Office', 'office',
        'Contact', 'contact',
        'About', 'about',
    ]
    
    for indicator in english_indicators:
        if indicator in value:
            return True
    
    return False

def check_ui_keys(conn, lang: str) -> Dict[str, bool]:
    """Проверява наличността на UI ключове за даден език"""
    ui_keys = ['faq_title', 'price_on_request', 'nav_link']
    result = {}
    
    for key in ui_keys:
        # Проверяваме ключове, свързани с cleaning
        with conn.cursor() as cur:
            cur.execute("""
                SELECT EXISTS(
                    SELECT 1 FROM translations 
                    WHERE lang = %s 
                    AND (key LIKE %s OR key LIKE %s OR key LIKE %s)
                );
            """, (lang, f'%{key}%', f'cleaning%{key}%', f'%{key}%cleaning%'))
            result[key] = cur.fetchone()[0]
    
    return result

def main():
    print("=== Глобален одит на преводите за категория cleaning ===\n")
    
    conn = get_connection()
    
    try:
        # Стъпка 1: Извличане на всички езици
        print("Стъпка 1: Извличане на всички езици...")
        languages = get_all_languages(conn)
        print(f"Намерени {len(languages)} езика: {languages}\n")
        
        # Стъпка 2: Извличане на референтните ключове от en и bg
        print("Стъпка 2: Извличане на референтни ключове от en и bg...")
        en_keys = get_cleaning_keys_for_lang(conn, 'en')
        bg_keys = get_cleaning_keys_for_lang(conn, 'bg')
        reference_keys = en_keys | bg_keys  # Обединение
        
        print(f"EN ключове: {len(en_keys)}")
        print(f"BG ключове: {len(bg_keys)}")
        print(f"Общо референтни ключове: {len(reference_keys)}\n")
        
        # Стъпка 3: Матричен анализ за всеки език
        print("Стъпка 3: Матричен анализ за всички езици...")
        print("-" * 80)
        
        audit_results = {}
        
        for lang in languages:
            if lang in ['en', 'bg']:
                continue
                
            lang_keys = get_cleaning_keys_for_lang(conn, lang)
            missing_keys = reference_keys - lang_keys
            
            # Проверка за кухи преводи (английски текст)
            empty_translations = []
            for key in lang_keys:
                value = get_translation_value(conn, lang, key)
                if check_english_in_non_english(value, lang):
                    empty_translations.append(key)
            
            # Проверка на UI ключове
            ui_keys_status = check_ui_keys(conn, lang)
            
            audit_results[lang] = {
                'total_keys': len(lang_keys),
                'missing_keys': sorted(list(missing_keys)),
                'missing_count': len(missing_keys),
                'empty_translations': empty_translations,
                'ui_keys': ui_keys_status
            }
            
            status = "ПЪЛЕН" if len(missing_keys) == 0 and len(empty_translations) == 0 else "НЕПЪЛЕН"
            print(f"{lang.upper():10} - {status:10} - Липсващи: {len(missing_keys):3d} - Кухи: {len(empty_translations):3d}")
        
        print("-" * 80 + "\n")
        
        # Стъпка 4: Детайлен отчет
        print("Стъпка 4: Детайлен отчет\n")
        
        for lang in sorted(audit_results.keys()):
            result = audit_results[lang]
            
            if result['missing_count'] == 0 and len(result['empty_translations']) == 0:
                print(f"✓ {lang.upper()} - Пълен")
            else:
                print(f"✗ {lang.upper()} - Непълен")
                
                if result['missing_count'] > 0:
                    print(f"  Липсващи ключове ({result['missing_count']}):")
                    for key in result['missing_keys'][:10]:  # Показваме първите 10
                        print(f"    - {key}")
                    if result['missing_count'] > 10:
                        print(f"    ... и още {result['missing_count'] - 10}")
                
                if len(result['empty_translations']) > 0:
                    print(f"  Кухи преводи (английски текст) ({len(result['empty_translations'])}):")
                    for key in result['empty_translations']:
                        print(f"    - {key}")
                
                # UI ключове статус
                ui_missing = [k for k, v in result['ui_keys'].items() if not v]
                if ui_missing:
                    print(f"  Липсващи UI ключове: {ui_missing}")
            
            print()
        
        # Стъпка 5: Обобщение
        print("=" * 80)
        print("ОБОБЩЕНИЕ")
        print("=" * 80)
        
        complete_languages = []
        incomplete_languages = []
        
        for lang, result in audit_results.items():
            if result['missing_count'] == 0 and len(result['empty_translations']) == 0:
                complete_languages.append(lang)
            else:
                incomplete_languages.append(lang)
        
        print(f"Пълни езици: {len(complete_languages)}/{len(audit_results)}")
        for lang in sorted(complete_languages):
            print(f"  - {lang}")
        
        print(f"\nНепълни езици: {len(incomplete_languages)}/{len(audit_results)}")
        for lang in sorted(incomplete_languages):
            result = audit_results[lang]
            print(f"  - {lang} (липсват: {result['missing_count']}, кухи: {len(result['empty_translations'])})")
        
        # Запазване на резултатите в JSON
        with open('/Users/dimitardimitrov/nevumo/cleaning_translation_audit.json', 'w') as f:
            json.dump(audit_results, f, indent=2)
        
        print(f"\nДетайлните резултати са записани в: cleaning_translation_audit.json")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()
