#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт за зареждане на login navigation translation ключове в PostgreSQL
"""

import json
import redis
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.i18n import SUPPORTED_LANGUAGES
from apps.api.models import Translation

# Translation данни от JSON файла
LOGIN_NAV_TRANSLATIONS = {
  "bg": {
    "login:nav.home": "Начало",
    "login:nav.services": "Услуги"
  },
  "cs": {
    "login:nav.home": "Domů",
    "login:nav.services": "Služby"
  },
  "da": {
    "login:nav.home": "Hjem",
    "login:nav.services": "Tjenester"
  },
  "de": {
    "login:nav.home": "Startseite",
    "login:nav.services": "Dienstleistungen"
  },
  "el": {
    "login:nav.home": "Αρχική",
    "login:nav.services": "Υπηρεσίες"
  },
  "en": {
    "login:nav.home": "Home",
    "login:nav.services": "Services"
  },
  "es": {
    "login:nav.home": "Inicio",
    "login:nav.services": "Servicios"
  },
  "et": {
    "login:nav.home": "Avaleht",
    "login:nav.services": "Teenused"
  },
  "fi": {
    "login:nav.home": "Etusivu",
    "login:nav.services": "Palvelut"
  },
  "fr": {
    "login:nav.home": "Accueil",
    "login:nav.services": "Services"
  },
  "ga": {
    "login:nav.home": "Baile",
    "login:nav.services": "Seirbhísí"
  },
  "hr": {
    "login:nav.home": "Početna",
    "login:nav.services": "Usluge"
  },
  "hu": {
    "login:nav.home": "Főoldal",
    "login:nav.services": "Szolgáltatások"
  },
  "it": {
    "login:nav.home": "Home",
    "login:nav.services": "Servizi"
  },
  "lt": {
    "login:nav.home": "Pagrindinis",
    "login:nav.services": "Paslaugos"
  },
  "lv": {
    "login:nav.home": "Sākums",
    "login:nav.services": "Pakalpojumi"
  },
  "mk": {
    "login:nav.home": "Почетна",
    "login:nav.services": "Услуги"
  },
  "mt": {
    "login:nav.home": "Paġna ewlenija",
    "login:nav.services": "Servizzi"
  },
  "nl": {
    "login:nav.home": "Home",
    "login:nav.services": "Diensten"
  },
  "no": {
    "login:nav.home": "Hjem",
    "login:nav.services": "Tjenester"
  },
  "pl": {
    "login:nav.home": "Strona główna",
    "login:nav.services": "Usługi"
  },
  "pt": {
    "login:nav.home": "Início",
    "login:nav.services": "Serviços"
  },
  "pt-PT": {
    "login:nav.home": "Início",
    "login:nav.services": "Serviços"
  },
  "ro": {
    "login:nav.home": "Acasă",
    "login:nav.services": "Servicii"
  },
  "sk": {
    "login:nav.home": "Domov",
    "login:nav.services": "Služby"
  },
  "sl": {
    "login:nav.home": "Domov",
    "login:nav.services": "Storitve"
  },
  "sq": {
    "login:nav.home": "Kryefaqja",
    "login:nav.services": "Shërbime"
  },
  "sr": {
    "login:nav.home": "Почетна",
    "login:nav.services": "Услуге"
  },
  "sv": {
    "login:nav.home": "Hem",
    "login:nav.services": "Tjänster"
  },
  "tr": {
    "login:nav.home": "Ana Sayfa",
    "login:nav.services": "Hizmetler"
  }
}

def load_login_nav_translations():
    """Зарежда login navigation translation ключове в PostgreSQL"""
    db = SessionLocal()
    
    try:
        # Брой на добавените/обновени преводи
        total_count = 0
        
        for lang, translations in LOGIN_NAV_TRANSLATIONS.items():
            if lang not in SUPPORTED_LANGUAGES:
                print(f"⚠️  Език {lang} не е в списъка с поддържани езици, пропускам...")
                continue
                
            for key, value in translations.items():
                # Проверяваме дали преводът вече съществува
                existing = db.query(Translation).filter_by(lang=lang, key=key).first()
                
                if existing:
                    # Обновяваме съществуващ превод
                    existing.value = value.strip()
                    print(f"✅ Обновен превод: {lang}:{key} = '{value}'")
                else:
                    # Добавяме нов превод
                    new_translation = Translation(
                        lang=lang,
                        key=key,
                        value=value.strip()
                    )
                    db.add(new_translation)
                    print(f"➕ Добавен превод: {lang}:{key} = '{value}'")
                
                total_count += 1
        
        # Записваме промените в базата данни
        db.commit()
        print(f"\n🎉 Успешно заредени {total_count} превода в PostgreSQL!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Грешка при зареждане на преводи: {e}")
        raise
    finally:
        db.close()

def invalidate_redis_cache():
    """Инвалидира Redis кеша за всички езици"""
    try:
        redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        redis_client.ping()
        
        invalidated_count = 0
        for lang in SUPPORTED_LANGUAGES:
            cache_key = f"translations:{lang}"
            result = redis_client.delete(cache_key)
            if result:
                invalidated_count += 1
                print(f"🗑️  Изтрит кеш за език: {lang}")
        
        print(f"\n🧹 Изтрити са {invalidated_count} Redis кеша за преводи!")
        
    except Exception as e:
        print(f"⚠️  Не може да се връже към Redis или грешка при изтриване на кеша: {e}")
        print("⚠️  Преводите са заредени в PostgreSQL, но кешът не е обновен автоматично.")

def main():
    """Главна функция"""
    print("🚀 Зареждане на login navigation translation ключове...")
    print("=" * 60)
    
    # Стъпка 1: Зареждане в PostgreSQL
    load_login_nav_translations()
    
    print("\n" + "=" * 60)
    
    # Стъпка 2: Инвалидиране на Redis кеша
    invalidate_redis_cache()
    
    print("\n✅ Завършено! Translation ключовете са заредени и кешът е обновен.")

if __name__ == "__main__":
    main()
