import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
import traceback


def main():
    print("=" * 50)
    print("E2E Claim Test Setup")
    print("=" * 50)

    # Step 1: DB INSERT
    print("\n[Step 1] Connecting to database...")
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        sys.exit(1)

    engine = create_engine(database_url, poolclass=NullPool)

    try:
        with engine.begin() as conn:
            print("✅ Connected to database")

            # a) Get category_id for plumbing
            print("\n[Step 1a] Getting category_id for 'plumbing'...")
            category_result = conn.execute(
                text("SELECT id FROM categories WHERE slug = 'plumbing' LIMIT 1")
            ).fetchone()
            
            if not category_result:
                print("❌ Категория plumbing не е намерена")
                sys.exit(1)
            
            category_id = category_result[0]
            print(f"✅ Category ID: {category_id}")

            # b) Get location_id for warszawa
            print("\n[Step 1b] Getting location_id for 'warszawa'...")
            location_result = conn.execute(
                text("SELECT id FROM locations WHERE slug = 'warszawa' LIMIT 1")
            ).fetchone()
            
            if not location_result:
                print("❌ Location warszawa не е намерен")
                sys.exit(1)
            
            location_id = location_result[0]
            print(f"✅ Location ID: {location_id}")

            # c) Insert provider
            print("\n[Step 1c] Inserting provider...")
            provider_result = conn.execute(
                text("""
                    INSERT INTO providers (
                        id, business_name, slug, is_claimed, claim_token,
                        data_source, availability_status, rating, verified, slug_change_count, verification_level
                    ) VALUES (
                        gen_random_uuid(),
                        'TEST Hydraulik Testowski [E2E]',
                        'test-hydraulik-testowski-e2e',
                        FALSE,
                        'e2e-test-claim-2026',
                        'scraped',
                        'active',
                        0,
                        FALSE,
                        0,
                        0
                    )
                    ON CONFLICT (slug) DO NOTHING
                    RETURNING id
                """)
            ).fetchone()

            if provider_result and provider_result[0]:
                provider_id = provider_result[0]
                print(f"✅ Provider inserted with ID: {provider_id}")
            else:
                # Conflict - get existing provider
                print("⚠️  Provider slug conflict, fetching existing...")
                existing_result = conn.execute(
                    text("SELECT id FROM providers WHERE slug = 'test-hydraulik-testowski-e2e'")
                ).fetchone()
                if not existing_result:
                    print("❌ Failed to fetch existing provider")
                    sys.exit(1)
                provider_id = existing_result[0]
                print(f"✅ Using existing provider ID: {provider_id}")

            # d) Insert service
            print("\n[Step 1d] Inserting service...")
            conn.execute(
                text("""
                    INSERT INTO services (id, provider_id, category_id, title, price_type, currency)
                    VALUES (gen_random_uuid(), :provider_id, :category_id, 'Usługi hydrauliczne', 'request', 'PLN')
                    ON CONFLICT DO NOTHING
                """),
                {"provider_id": provider_id, "category_id": category_id}
            )
            print("✅ Service inserted")

            # e) Insert provider_city
            print("\n[Step 1e] Inserting provider_city...")
            conn.execute(
                text("""
                    INSERT INTO provider_cities (provider_id, city_id)
                    VALUES (:provider_id, :location_id)
                    ON CONFLICT DO NOTHING
                """),
                {"provider_id": provider_id, "location_id": location_id}
            )
            print("✅ Provider_city inserted")

    except Exception as e:
        print(f"❌ Database error: {e}")
        traceback.print_exc()
        sys.exit(1)

    # Step 2: Send email
    print("\n[Step 2] Sending outreach email...")
    
    try:
        resend_api_key = os.environ.get("RESEND_API_KEY", "")
        
        if not resend_api_key:
            print("❌ RESEND_API_KEY environment variable not set")
            sys.exit(1)
        
        # Read template from docs directory
        template_path = Path(__file__).parent.parent.parent.parent / "docs" / "outreach_email_pl.html"
        print(f"Reading template from: {template_path}")
        
        if not template_path.exists():
            print(f"❌ Template file not found: {template_path}")
            sys.exit(1)
        
        # Read and replace placeholders using string replacement
        html_content = template_path.read_text(encoding="utf-8")
        
        # Replace Jinja2-style placeholders with actual values
        html_content = html_content.replace("{ business_name }", "TEST Hydraulik Testowski [E2E]")
        html_content = html_content.replace("{ claim_link }", "https://nevumo.com/pl/claim/e2e-test-claim-2026")
        html_content = html_content.replace("{ provider_phone }", "+48 123 456 789")
        html_content = html_content.replace("{ provider_email }", "dimitar.j.dimitroff@gmail.com")
        html_content = html_content.replace("{ provider_address }", "ul. Testowa 1, 00-001 Warszawa")
        html_content = html_content.replace("{ provider_website }", "https://test-example.pl")
        
        # Send email using httpx directly to Resend API
        print("Sending email via Resend API...")
        import httpx
        
        response = httpx.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {resend_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "from": "Nevumo <support@nevumo.com>",
                "to": ["dimitar.j.dimitroff@gmail.com"],
                "subject": "10 707 firm instalacyjnych w Warszawie — czy Twoi klienci Cię znajdą?",
                "html": html_content
            },
            timeout=30.0
        )
        
        if response.status_code == 200:
            print("✅ Email sent successfully")
        else:
            print(f"❌ Email failed with status {response.status_code}: {response.text}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Email error: {e}")
        traceback.print_exc()
        sys.exit(1)

    # Step 3: Print results
    print("\n[Step 3] Results:")
    print("=" * 50)
    print(f"✅ Provider ID: {provider_id}")
    print(f"✅ Claim URL (valid): https://nevumo.com/pl/claim/e2e-test-claim-2026")
    print(f"✅ Not-found URL: https://nevumo.com/bg/claim/invalidtoken")
    print(f"✅ Email изпратен до: dimitar.j.dimitroff@gmail.com")
    print("=" * 50)


if __name__ == "__main__":
    main()
