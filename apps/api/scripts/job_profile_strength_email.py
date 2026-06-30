"""
Railway Scheduler job — Profile Strength Email
Runs daily. Sends profile_strength_email to every provider where:
  - is_complete = True
  - profile_strength_email_sent_at IS NULL
  - At least one field is missing (photo, gallery, description < 100 chars, phone)
"""
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from apps.api.services.email_service import EmailService
from apps.api.services.auth_service import generate_magic_link_token

DATABASE_URL = os.environ["DATABASE_URL"]
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://nevumo.com")

engine = create_engine(DATABASE_URL)


def build_dashboard_url(locale: str, raw_token: str, anchor: str = "") -> str:
    base = f"{FRONTEND_URL}/{locale}/auth/magic?token={raw_token}&next=%2F{locale}%2Fprovider%2Fdashboard%2Fprofile"
    if anchor:
        base += f"%23{anchor}-section"
    return base


def build_unsubscribe_url(provider_id: int) -> str:
    return f"{FRONTEND_URL}/unsubscribe?pid={provider_id}"


def main() -> None:
    email_service = EmailService()
    sent = 0
    failed = 0

    with Session(engine) as db:
        rows = db.execute(text("""
            SELECT
                p.id                        AS provider_id,
                p.business_name,
                p.profile_image_url,
                p.description,
                u.locale,
                p.category_slug,
                u.email,
                u.phone,
                (
                    SELECT COUNT(*) FROM provider_images pi
                    WHERE pi.provider_id = p.id
                ) AS gallery_count
            FROM providers p
            JOIN users u ON u.id = p.user_id
            WHERE
                p.business_name IS NOT NULL
                AND p.category_slug IS NOT NULL
                AND (
                    p.profile_strength_email_sent_at IS NULL
                    OR p.profile_strength_email_sent_at < NOW() - INTERVAL '14 days'
                )
                AND u.email IS NOT NULL
                AND (
                    p.profile_image_url IS NULL
                    OR (SELECT COUNT(*) FROM provider_images pi WHERE pi.provider_id = p.id) = 0
                    OR p.description IS NULL
                    OR LENGTH(p.description) < 100
                    OR u.phone IS NULL
                )
        """)).fetchall()

        print(f"[job_profile_strength_email] Found {len(rows)} providers to email.")

        for row in rows:
            show_photo       = row.profile_image_url is None
            show_gallery     = row.gallery_count == 0
            show_description = row.description is None or len(row.description) < 100
            show_phone       = row.phone is None
            missing_count    = sum([show_photo, show_gallery, show_description, show_phone])

            if missing_count == 0:
                continue

            locale        = row.locale or "en"
            category_slug = row.category_slug or "plumbing"

            token_photo = generate_magic_link_token(row.email, db, hours=336, invalidate_existing=False, multi_use=True)
            token_gallery = generate_magic_link_token(row.email, db, hours=336, invalidate_existing=False, multi_use=True)
            token_description = generate_magic_link_token(row.email, db, hours=336, invalidate_existing=False, multi_use=True)
            token_phone = generate_magic_link_token(row.email, db, hours=336, invalidate_existing=False, multi_use=True)
            token_main = generate_magic_link_token(row.email, db, hours=336, invalidate_existing=False, multi_use=True)
            db.commit()

            photo_url = build_dashboard_url(locale, token_photo, "photo")
            gallery_url = build_dashboard_url(locale, token_gallery, "gallery")
            description_url = build_dashboard_url(locale, token_description, "details")
            phone_url = build_dashboard_url(locale, token_phone, "photo")
            main_url = build_dashboard_url(locale, token_main)

            success = email_service.send_profile_strength_email(
                provider_id=row.provider_id,
                business_name=row.business_name or "",
                provider_email=row.email,
                locale=locale,
                category_slug=category_slug,
                show_photo=show_photo,
                show_gallery=show_gallery,
                show_description=show_description,
                show_phone=show_phone,
                missing_count=missing_count,
                photo_url=photo_url,
                gallery_url=gallery_url,
                description_url=description_url,
                phone_url=phone_url,
                main_url=main_url,
                unsubscribe_url=build_unsubscribe_url(row.provider_id),
                db=db,
            )

            if success:
                db.execute(
                    text("""
                        UPDATE providers
                        SET profile_strength_email_sent_at = :now
                        WHERE id = :pid
                    """),
                    {"now": datetime.now(timezone.utc), "pid": row.provider_id},
                )
                db.commit()
                sent += 1
                print(f"  ✅ Sent to provider {row.provider_id} ({row.email})")
            else:
                failed += 1
                print(f"  ❌ Failed for provider {row.provider_id} ({row.email})")

    print(f"[job_profile_strength_email] Done. Sent: {sent}, Failed: {failed}")


if __name__ == "__main__":
    main()
