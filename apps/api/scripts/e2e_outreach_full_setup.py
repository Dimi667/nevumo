#!/usr/bin/env python3
"""
E2E Test Setup Script for Outreach Email Testing
Creates 3 unclaimed test providers in the production Neon DB and generates a CSV for outreach email test.
Uses data_source="e2e_test" as the safety marker for cleanup.
"""

import csv
from pathlib import Path

from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models import (
    Provider,
    ProviderCity,
    Service,
    ServiceCity,
    Location,
    Category,
)
from apps.api.services.provider_service import generate_provider_slug, is_slug_taken, generate_claim_token


# Test providers to create
TEST_PROVIDERS = [
    {
        "email": "nevumo.dev@gmail.com",
        "business_name": "Sprzątanie Testowe E2E",
        "category_slug": "cleaning",
        "category_id": 1,
    },
    {
        "email": "dimitar.j.dimitroff@gmail.com",
        "business_name": "Hydraulik Testowy E2E",
        "category_slug": "plumbing",
        "category_id": 2,
    },
    {
        "email": "neli.b.bojilova@gmail.com",
        "business_name": "Studio Masażu Testowe E2E",
        "category_slug": "massage",
        "category_id": 3,
    },
]

# DB constants
WARSAW_CITY_ID = 2
CURRENCY = "PLN"
CSV_OUTPUT_PATH = Path(__file__).parent / "e2e_test_outreach.csv"


def create_provider(
    email: str,
    business_name: str,
    category_slug: str,
    category_id: int,
    db: Session,
) -> tuple[bool, dict]:
    """
    Create a single unclaimed provider with all required relationships.
    Returns (success: bool, provider_data: dict).
    """
    try:
        # 1. Generate slug
        slug = generate_provider_slug(business_name, db)

        # 2. Check if slug already exists, try with "-test" suffix
        if is_slug_taken(slug, db):
            slug = f"{slug}-test"
            if is_slug_taken(slug, db):
                return False, {"error": f"Slug '{slug}' already exists even with -test suffix"}

        # 3. Generate claim token
        claim_token = generate_claim_token(db)

        # 4. Create Provider
        provider = Provider(
            user_id=None,
            business_name=business_name,
            slug=slug,
            description="",
            is_claimed=False,
            claim_token=claim_token,
            data_source="e2e_test",
            verified=False,
            availability_status="active",
            rating=0,
        )
        db.add(provider)
        db.flush()  # Get provider.id before commit

        # 5. Create ProviderCity
        provider_city = ProviderCity(provider_id=provider.id, city_id=WARSAW_CITY_ID)
        db.add(provider_city)

        # 6. Create Service
        service = Service(
            provider_id=provider.id,
            category_id=category_id,
            title=category_slug,
            price_type="request",
            base_price=None,
            currency=CURRENCY,
        )
        db.add(service)
        db.flush()  # Get service.id before creating ServiceCity

        # 7. Create ServiceCity
        service_city = ServiceCity(service_id=service.id, city_id=WARSAW_CITY_ID)
        db.add(service_city)

        # 8. Commit
        db.commit()

        return True, {
            "business_name": business_name,
            "slug": slug,
            "claim_token": claim_token,
            "email": email,
            "category": category_slug,
        }

    except Exception as e:
        db.rollback()
        return False, {"error": str(e)}


def main() -> None:
    """Main entry point."""
    db = SessionLocal()
    created_providers = []

    try:
        for provider_data in TEST_PROVIDERS:
            email = provider_data["email"]
            business_name = provider_data["business_name"]
            category_slug = provider_data["category_slug"]
            category_id = provider_data["category_id"]

            success, result = create_provider(
                email=email,
                business_name=business_name,
                category_slug=category_slug,
                category_id=category_id,
                db=db,
            )

            if success:
                created_providers.append(result)
                print(f"CREATED: {result['business_name']}")
                print(f"Slug: {result['slug']}")
                print(f"Claim token: {result['claim_token']}")
                print(f"Claim URL: https://nevumo.com/pl/claim/{result['claim_token']}")
                print(f"Email: {result['email']}")
                print("---")
            else:
                print(f"WARNING: Failed to create {business_name}: {result.get('error', 'Unknown error')}")

        # Generate CSV
        if created_providers:
            with CSV_OUTPUT_PATH.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["email", "business_name", "claim_token", "category"],
                )
                writer.writeheader()
                for provider in created_providers:
                    writer.writerow({
                        "email": provider["email"],
                        "business_name": provider["business_name"],
                        "claim_token": provider["claim_token"],
                        "category": provider["category"],
                    })

            print(f"CSV written to {CSV_OUTPUT_PATH}")
        else:
            print("No providers were created. CSV not generated.")

    except Exception as e:
        db.rollback()
        print(f"Fatal error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
