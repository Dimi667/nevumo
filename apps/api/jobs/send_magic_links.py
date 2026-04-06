from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
import hashlib
from models import PendingLeadClaim, MagicLinkToken
from config import settings

def process_pending_magic_links(db: Session) -> int:
    """
    Finds pending_lead_claims older than 30 minutes that:
    - Are not yet claimed
    - Have not had a magic link sent yet
    - Have not expired
    Generates magic link tokens and sends emails (console for now).
    Returns count of processed claims.
    """
    cutoff = datetime.utcnow() - timedelta(minutes=30)
    now = datetime.utcnow()

    claims = db.query(PendingLeadClaim).filter(
        PendingLeadClaim.claimed == False,
        PendingLeadClaim.magic_link_sent == False,
        PendingLeadClaim.expires_at > now,
        PendingLeadClaim.created_at <= cutoff
    ).all()

    count = 0
    for claim in claims:
        try:
            # Generate token
            raw_token = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

            # Store in magic_link_tokens
            magic_token = MagicLinkToken(
                email=claim.email,
                lead_id=claim.lead_id,
                token_hash=token_hash,
                expires_at=datetime.utcnow() + timedelta(hours=48)
            )
            db.add(magic_token)

            # Send email (console for now — same pattern as send_reset_email)
            magic_link_url = f"{settings.APP_URL}/en/auth/magic?token={raw_token}"
            print(f"[Magic Link Email] To: {claim.email}")
            print(f"[Magic Link Email] Subject: Виж кой отговори на заявката ти")
            print(f"[Magic Link Email] Link: {magic_link_url}")

            # Mark claim as sent
            claim.magic_link_sent = True
            claim.magic_link_sent_at = datetime.utcnow()

            db.commit()
            count += 1
        except Exception as e:
            db.rollback()
            print(f"[Magic Link] Error processing claim {claim.id}: {e}")
            continue

    return count
