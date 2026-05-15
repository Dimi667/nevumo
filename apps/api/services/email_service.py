"""Email service for review-related notifications."""

from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from apps.api.config import settings
from apps.api.models import Review, User, Provider


class EmailService:
    """Minimal email service for review reply notifications.

    Implements a clean abstraction for sending emails without overbuilding
    a full email platform. Supports both SMTP and email service APIs.
    """

    def __init__(self) -> None:
        self._enabled = bool(getattr(settings, 'SMTP_HOST', None) or
                            getattr(settings, 'EMAIL_API_KEY', None))
        self._from_email = getattr(settings, 'FROM_EMAIL', 'noreply@nevumo.com')
        self._app_url = getattr(settings, 'APP_URL', 'https://nevumo.com')

    def _send_email(
        self,
        to_email: str,
        subject: str,
        text_body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """Send email via configured provider.

        Returns True if email was sent successfully, False otherwise.
        This is idempotent - duplicate sends are safe.
        """
        if not self._enabled:
            # Log to console in development
            print(f"[EMAIL] To: {to_email}")
            print(f"[EMAIL] Subject: {subject}")
            print(f"[EMAIL] Body: {text_body[:200]}...")
            return True

        # TODO: Implement actual email sending via SMTP or email API
        # This is a minimal abstraction that can be extended later
        try:
            # Placeholder for actual email implementation
            # if hasattr(settings, 'EMAIL_API_KEY'):
            #     return self._send_via_api(to_email, subject, text_body, html_body)
            # else:
            #     return self._send_via_smtp(to_email, subject, text_body, html_body)
            return True
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send email to {to_email}: {e}")
            return False

    def send_review_reply_notification(
        self,
        db: Session,
        review: Review,
        is_first_reply: bool = True
    ) -> bool:
        """Send email notification to client when provider replies to review.

        Only sends on first reply (not on edits) unless explicitly overridden.
        Respects user's email preference opt-out.

        Returns True if email was sent or would have been sent but user opted out.
        Returns False if there was an error sending.
        """
        # Only send on first reply, not on edits
        if not is_first_reply:
            return True

        # Get client user to check email preference
        client = db.query(User).filter(User.id == review.client_id).first()
        if not client:
            return True  # Client not found, nothing to do

        # Check opt-out preference (default is enabled=True)
        if not client.review_reply_email_enabled:
            return True  # User opted out, skip silently

        # Get provider info for email context
        provider = db.query(Provider).filter(Provider.id == review.provider_id).first()
        provider_name = provider.business_name if provider else "Your service provider"

        # Build email content
        subject = f"{provider_name} responded to your review"

        text_body = f"""Hi,

{provider_name} has replied to your review.

Your review ({review.rating}/5 stars):
{review.comment or 'No comment'}

Provider's reply:
{review.provider_reply or 'No reply text'}

View your reviews: {self._app_url}/client/reviews

---
You can manage your email preferences in your account settings.
"""

        html_body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{subject}</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #2563eb;">New Reply to Your Review</h2>

        <p><strong>{provider_name}</strong> has responded to your review.</p>

        <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <p style="margin: 0;"><strong>Your review</strong> ({review.rating}/5 ⭐)</p>
            <p style="margin: 10px 0 0 0; font-style: italic;">{review.comment or 'No comment'}</p>
        </div>

        <div style="background: #eff6ff; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #2563eb;">
            <p style="margin: 0;"><strong>{provider_name}'s reply:</strong></p>
            <p style="margin: 10px 0 0 0;">{review.provider_reply or 'No reply text'}</p>
        </div>

        <p>
            <a href="{self._app_url}/client/reviews" style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                View Your Reviews
            </a>
        </p>

        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">

        <p style="font-size: 12px; color: #6b7280;">
            You can <a href="{self._app_url}/client/settings">manage your email preferences</a> in your account settings.
        </p>
    </div>
</body>
</html>"""

        return self._send_email(
            to_email=client.email,
            subject=subject,
            text_body=text_body,
            html_body=html_body
        )

    def send_withdrawal_form_email(
        self,
        service_description: str,
        contract_date: date,
        consumer_name: str,
        consumer_address: str,
        account_id: Optional[str],
        email: str,
        submission_date: date,
        lang: str = "en"
    ) -> bool:
        """Send withdrawal form submission email to legal@nevumo.com.

        Args:
            service_description: Description of the service
            contract_date: Date of the contract
            consumer_name: Name of the consumer
            consumer_address: Address of the consumer
            account_id: Optional account ID
            email: Consumer's email address
            submission_date: Date of form submission
            lang: Language code for email formatting (en, bg, pl)

        Returns:
            True if email was sent successfully, False otherwise
        """
        # Get language-specific subject
        subjects = {
            "en": "Withdrawal from contract",
            "bg": "Отказ от договор",
            "pl": "Odstąpienie od umowy"
        }
        subject = subjects.get(lang, subjects["en"])

        # Build text email body
        text_body = f"""Withdrawal Form Submission

Service Description:
{service_description}

Contract Date:
{contract_date}

Consumer Name:
{consumer_name}

Consumer Address:
{consumer_address}

Account ID:
{account_id or 'Not provided'}

Email:
{email}

Submission Date:
{submission_date}

---
This withdrawal form was submitted via the Nevumo online form.
"""

        # Build HTML email body
        html_body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{subject}</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #dc2626;">{subject}</h2>

        <div style="background: #fef2f2; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #dc2626;">
            <h3 style="margin-top: 0;">Withdrawal Form Submission</h3>

            <p><strong>Service Description:</strong></p>
            <p style="background: white; padding: 10px; border-radius: 4px; margin: 10px 0;">{service_description}</p>

            <p><strong>Contract Date:</strong> {contract_date}</p>

            <p><strong>Consumer Name:</strong> {consumer_name}</p>

            <p><strong>Consumer Address:</strong></p>
            <p style="background: white; padding: 10px; border-radius: 4px; margin: 10px 0;">{consumer_address}</p>

            <p><strong>Account ID:</strong> {account_id or 'Not provided'}</p>

            <p><strong>Email:</strong> {email}</p>

            <p><strong>Submission Date:</strong> {submission_date}</p>
        </div>

        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">

        <p style="font-size: 12px; color: #6b7280;">
            This withdrawal form was submitted via the Nevumo online form.
        </p>
    </div>
</body>
</html>"""

        return self._send_email(
            to_email="legal@nevumo.com",
            subject=subject,
            text_body=text_body,
            html_body=html_body
        )


# Global email service instance
email_service = EmailService()
