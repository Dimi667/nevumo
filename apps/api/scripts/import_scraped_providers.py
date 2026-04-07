#!/usr/bin/env python3
"""
CSV Import Script for Scraped Provider Data
Reads a CSV file and creates skeleton (unclaimed) provider records.
"""

import csv
import sys
import os
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal
from models import (
    Provider,
    ProviderCity,
    Service,
    ServiceCity,
    Location,
    Category,
    CategoryTranslation,
)
from services.provider_service import generate_provider_slug, is_slug_taken, generate_claim_token


COUNTRY_CURRENCY = {
    "PL": "PLN", "BG": "EUR", "RS": "RSD", "CZ": "CZK",
    "GR": "EUR", "DE": "EUR", "FR": "EUR", "IT": "EUR",
    "ES": "EUR", "NL": "EUR", "AT": "EUR", "BE": "EUR",
    "PT": "EUR", "FI": "EUR", "IE": "EUR", "LU": "EUR",
    "MT": "EUR", "SK": "EUR", "SI": "EUR", "EE": "EUR",
    "LV": "EUR", "LT": "EUR", "HU": "HUF", "RO": "RON",
    "SE": "SEK", "DK": "DKK", "NO": "NOK", "CH": "CHF",
    "TR": "TRY", "AL": "ALL", "MK": "MKD", "HR": "HRK",
    "BA": "BAM",
}


def get_english_category_name(category_id: int, category_slug: str, db: Session) -> str:
    """Get English category name from CategoryTranslation. Fallback to slug if not found."""
    translation = (
        db.query(CategoryTranslation)
        .filter(
            CategoryTranslation.category_id == category_id,
            CategoryTranslation.lang == "en",
        )
        .first()
    )
    return translation.name if translation else category_slug


def process_row(
    row_num: int,
    row: dict,
    db: Session,
) -> tuple[bool, str]:
    """
    Process a single CSV row.
    Returns (success: bool, message: str).
    """
    # 1. Strip whitespace from all fields
    business_name = row.get("business_name", "").strip()
    city_slug = row.get("city_slug", "").strip()
    category_slug = row.get("category_slug", "").strip()
    phone = row.get("phone", "").strip()
    website = row.get("website", "").strip()
    address = row.get("address", "").strip()
    description = row.get("description", "").strip()

    # 2. Find Location by slug
    location = db.query(Location).filter(Location.slug == city_slug).first()
    if not location:
        return False, f"SKIP row {row_num}: city '{city_slug}' not found"

    # 3. Find Category by slug
    category = db.query(Category).filter(Category.slug == category_slug).first()
    if not category:
        return False, f"SKIP row {row_num}: category '{category_slug}' not found"

    # 4. Generate slug
    slug = generate_provider_slug(business_name, db)

    # 5. Check if slug already exists
    if is_slug_taken(slug, db):
        return False, f"SKIP row {row_num}: slug '{slug}' already exists"

    # 6. Generate claim token
    claim_token = generate_claim_token(db)

    # 7. Detect currency
    currency = COUNTRY_CURRENCY.get(location.country_code, "EUR")

    # 8. Get category English name
    title = get_english_category_name(category.id, category.slug, db)

    # 9. Create Provider
    provider = Provider(
        user_id=None,
        business_name=business_name,
        slug=slug,
        description=description if description else "",
        is_claimed=False,
        claim_token=claim_token,
        data_source="scraped",
        verified=False,
        availability_status="active",
        rating=0,
    )
    db.add(provider)
    db.flush()  # Get provider.id before commit

    # 10. Create ProviderCity
    provider_city = ProviderCity(provider_id=provider.id, city_id=location.id)
    db.add(provider_city)

    # 11. Create Service
    service = Service(
        provider_id=provider.id,
        category_id=category.id,
        title=title,
        price_type="request",
        base_price=None,
        currency=currency,
    )
    db.add(service)
    db.flush()  # Get service.id before creating ServiceCity

    # 12. Create ServiceCity
    service_city = ServiceCity(service_id=service.id, city_id=location.id)
    db.add(service_city)

    # 13. Commit this row
    db.commit()

    # 14. Return success message
    return True, f"IMPORTED row {row_num}: {business_name} → slug={slug}"


def import_csv(file_path: str, db: Session) -> tuple[int, int, int]:
    """
    Import providers from CSV file.
    Returns (imported_count, skipped_count, error_count).
    """
    imported = 0
    skipped = 0
    errors = 0

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=1):
            try:
                success, message = process_row(row_num, row, db)
                print(message)
                if success:
                    imported += 1
                else:
                    if "SKIP" in message:
                        skipped += 1
            except Exception as e:
                db.rollback()
                print(f"ERROR row {row_num}: {e}")
                errors += 1
                continue

    return imported, skipped, errors


def main() -> None:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python import_scraped_providers.py path/to/file.csv")
        sys.exit(1)

    csv_file = sys.argv[1]

    if not os.path.exists(csv_file):
        print(f"Error: File not found: {csv_file}")
        sys.exit(1)

    db = SessionLocal()
    try:
        imported, skipped, errors = import_csv(csv_file, db)
        print(f"\nDone. Imported: {imported}, Skipped: {skipped}, Errors: {errors}")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
