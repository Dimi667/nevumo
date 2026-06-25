"""Email service for review-related notifications."""

import logging
from datetime import date
from pathlib import Path
from typing import Optional
from uuid import UUID

from jinja2 import Template
from sqlalchemy.orm import Session

from apps.api.config import settings
from apps.api.models import Review, User, Provider

logger = logging.getLogger(__name__)


class EmailService:
    """Minimal email service for review reply notifications.

    Implements a clean abstraction for sending emails without overbuilding
    a full email platform. Supports both SMTP and email service APIs.
    """

    def __init__(self) -> None:
        self._api_key = getattr(settings, 'RESEND_API_KEY', '')
        self._from_email = getattr(settings, 'FROM_EMAIL', 'Nevumo <noreply@nevumo.com>')
        self._legal_email = getattr(settings, 'LEGAL_EMAIL', 'legal@nevumo.com')
        self._app_url = getattr(settings, 'APP_URL', 'https://nevumo.com')
        self._enabled = bool(self._api_key)
        if self._enabled:
            import resend
            resend.api_key = self._api_key

    def _send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
    ) -> bool:
        if not self._enabled:
            print(f"[EMAIL] To: {to_email} | Subject: {subject}")
            return True
        try:
            import resend
            params: resend.Emails.SendParams = {
                "from": self._from_email,
                "to": [to_email],
                "subject": subject,
                "html": html_body,
            }
            if text_body:
                params["text"] = text_body
            resend.Emails.send(params)
            return True
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send to {to_email}: {e}")
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

    def send_password_reset_email(self, email: str, reset_url: str) -> bool:
        subject = "Reset your Nevumo password"
        html_body = f"""<!DOCTYPE html><html><body style="font-family:Arial,sans-serif;color:#333;">
    <div style="max-width:600px;margin:0 auto;padding:20px;">
    <h2 style="color:#f97316;">Reset your password</h2>
    <p>Click the button below to reset your password. The link expires in 30 minutes.</p>
    <p><a href="{reset_url}" style="background:#f97316;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;display:inline-block;">Reset Password</a></p>
    <p>If you did not request this, ignore this email.</p>
    </div></body></html>"""
        return self._send_email(email, subject, html_body)

    def send_welcome_email(self, email: str, role: str) -> bool:
        dashboard_url = f"{self._app_url}/provider/dashboard" if role == "provider" else f"{self._app_url}/client/dashboard"
        subject = "Welcome to Nevumo"
        html_body = f"""<!DOCTYPE html><html><body style="font-family:Arial,sans-serif;color:#333;">
    <div style="max-width:600px;margin:0 auto;padding:20px;">
    <h2 style="color:#f97316;">Welcome to Nevumo!</h2>
    <p>Your account has been created successfully.</p>
    <p><a href="{dashboard_url}" style="background:#f97316;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;display:inline-block;">Go to Dashboard</a></p>
    </div></body></html>"""
        return self._send_email(email, subject, html_body)

    def send_magic_link_email(self, email: str, magic_link_url: str) -> bool:
        subject = "Your Nevumo access link"
        html_body = f"""<!DOCTYPE html><html><body style="font-family:Arial,sans-serif;color:#333;">
    <div style="max-width:600px;margin:0 auto;padding:20px;">
    <h2 style="color:#f97316;">View your service request</h2>
    <p>Click below to access your request. The link expires in 48 hours.</p>
    <p><a href="{magic_link_url}" style="background:#f97316;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;display:inline-block;">View My Request</a></p>
    </div></body></html>"""
        return self._send_email(email, subject, html_body)

    def send_login_magic_link_email(
        self,
        email: str,
        magic_link_url: str,
        lang: str = "en",
    ) -> bool:
        if lang.startswith("pl"):
            subject = "Twój link do logowania w Nevumo"
            html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;color:#333;background-color:#ffffff;">
    <div style="max-width:600px;margin:0 auto;padding:20px;">
        <h2 style="color:#f97316;">Zaloguj się do Nevumo</h2>
        <p>Kliknij poniższy przycisk, aby zalogować się na swoje konto. Link jest ważny przez 24 godziny i może być użyty tylko raz.</p>
        <p><a href="{magic_link_url}" style="background:#f97316;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;display:inline-block;">Zaloguj się →</a></p>
        <p style="text-align:center;color:#666;">lub</p>
        <p><a href="{magic_link_url}" style="background:#f97316;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;display:inline-block;">Kopiuj link</a></p>
        <p style="font-size:12px;color:#666;">Jeśli nie prosiłeś/aś o ten link, zignoruj tę wiadomość.</p>
    </div>
</body>
</html>"""
        else:
            subject = "Your Nevumo login link"
            html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;color:#333;background-color:#ffffff;">
    <div style="max-width:600px;margin:0 auto;padding:20px;">
        <h2 style="color:#f97316;">Sign in to Nevumo</h2>
        <p>Click below to sign in to your account. This link expires in 24 hours and can only be used once.</p>
        <p><a href="{magic_link_url}" style="background:#f97316;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;display:inline-block;">Sign in →</a></p>
        <p style="text-align:center;color:#666;">or</p>
        <p><a href="{magic_link_url}" style="background:#f97316;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;display:inline-block;">Copy link</a></p>
        <p style="font-size:12px;color:#666;">If you didn't request this link, you can safely ignore this email.</p>
    </div>
</body>
</html>"""
        return self._send_email(email, subject, html_body)

    def send_new_lead_notification(
        self,
        provider_email: str,
        provider_name: str,
        category: str,
        city: str,
        description: Optional[str],
        dashboard_url: str,
    ) -> bool:
        subject = f"New request in {city} — {category}"
        desc_html = f"<p><em>{description}</em></p>" if description else ""
        html_body = f"""<!DOCTYPE html><html><body style="font-family:Arial,sans-serif;color:#333;">
    <div style="max-width:600px;margin:0 auto;padding:20px;">
    <h2 style="color:#f97316;">New service request</h2>
    <p>Hi {provider_name}, you have a new request:</p>
    <div style="background:#f3f4f6;padding:15px;border-radius:8px;margin:20px 0;">
    <p><strong>Category:</strong> {category}</p>
    <p><strong>City:</strong> {city}</p>
    {desc_html}
    </div>
    <p><a href="{dashboard_url}" style="background:#f97316;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;display:inline-block;">View Request</a></p>
    </div></body></html>"""
        return self._send_email(provider_email, subject, html_body)

    def send_lead_status_notification(
        self,
        to_email: str,
        new_status: str,
        category: str,
        city: str,
        dashboard_url: str,
    ) -> bool:
        status_messages = {
            "contacted": ("Provider contacted you", "A provider has contacted you regarding your request."),
            "done": ("Request marked as completed", "Your service request has been marked as completed."),
            "cancelled": ("Request cancelled", "A service request has been cancelled."),
        }
        subject, body_text = status_messages.get(new_status, ("Request update", "Your request status has been updated."))
        html_body = f"""<!DOCTYPE html><html><body style="font-family:Arial,sans-serif;color:#333;">
    <div style="max-width:600px;margin:0 auto;padding:20px;">
    <h2 style="color:#f97316;">{subject}</h2>
    <p>{body_text}</p>
    <div style="background:#f3f4f6;padding:15px;border-radius:8px;margin:20px 0;">
    <p><strong>Category:</strong> {category}</p>
    <p><strong>City:</strong> {city}</p>
    </div>
    <p><a href="{dashboard_url}" style="background:#f97316;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;display:inline-block;">View Dashboard</a></p>
    </div></body></html>"""
        return self._send_email(to_email, subject, html_body)

    def send_new_review_notification(
        self,
        provider_email: str,
        provider_name: str,
        client_name: str,
        rating: int,
        comment: Optional[str],
        dashboard_url: str,
    ) -> bool:
        subject = f"New review from {client_name} — {rating}/5 stars"
        comment_html = f"<p><em>{comment}</em></p>" if comment else ""
        html_body = f"""<!DOCTYPE html><html><body style="font-family:Arial,sans-serif;color:#333;">
    <div style="max-width:600px;margin:0 auto;padding:20px;">
    <h2 style="color:#f97316;">You received a new review</h2>
    <p>Hi {provider_name},</p>
    <div style="background:#f3f4f6;padding:15px;border-radius:8px;margin:20px 0;">
    <p><strong>{client_name}</strong> rated you <strong>{rating}/5 ⭐</strong></p>
    {comment_html}
    </div>
    <p><a href="{dashboard_url}" style="background:#f97316;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;display:inline-block;">View & Reply</a></p>
    </div></body></html>"""
        return self._send_email(provider_email, subject, html_body)

    def send_article14_notification(
        self,
        to_email: str,
        business_name: str,
        dashboard_link: str,
        nip: str | None = None,
        provider_phone: str | None = None,
        scraped_email: str | None = None,
        provider_website: str | None = None,
        category_label: str = "usługi",
    ) -> None:
        try:
            import jinja2
            import pathlib

            template_dir = pathlib.Path(__file__).parent / "templates"
            env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(template_dir)))
            template = env.get_template("article14_confirmation_pl.html")

            html = template.render(
                business_name=business_name,
                dashboard_link=dashboard_link,
                nip=nip,
                provider_phone=provider_phone,
                scraped_email=scraped_email,
                provider_website=provider_website,
                category_label=category_label,
            )

            self._send_email(
                to_email=to_email,
                subject="Profil aktywny ✓ — informacja o danych (art. 14 RODO)",
                html_body=html,
            )
        except Exception as e:
            print(f"[EMAIL_WARNING] send_article14_notification failed: {e}", flush=True)

    def send_claim_welcome_email(
        self,
        provider_email: str,
        provider_name: str,
    ) -> bool:
        """Send welcome email after successful profile claim."""
        dashboard_url = f"{self._app_url}/provider/dashboard"
        subject = "Your Nevumo profile is now active"
        html_body = f"""<!DOCTYPE html><html><body style="font-family:Arial,sans-serif;color:#333;">
    <div style="max-width:600px;margin:0 auto;padding:20px;">
    <h2 style="color:#f97316;">Your Nevumo profile is now active!</h2>
    <p>Dear {provider_name},</p>
    <p>Congratulations! Your profile has been successfully claimed and is now active on Nevumo.</p>
    <p>You can start receiving client requests right away. Make sure to complete your profile information to increase your visibility.</p>
    <p><a href="{dashboard_url}" style="background:#f97316;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;display:inline-block;">Go to Dashboard</a></p>
    <hr style="border:none;border-top:1px solid #e5e7eb;margin:30px 0;">
    <p style="font-size:12px;color:#6b7280;">If you have any questions, feel free to contact our support team.</p>
    </div></body></html>"""
        return self._send_email(provider_email, subject, html_body)

    def send_claim_verification_email(
        self,
        to_email: str,
        business_name: str,
        code: str,
    ) -> bool:
        """Send 6-digit verification code to the business scraped_email."""
        try:
            template_path = Path(__file__).parent.parent / "scripts" / "templates" / "claim_verification_pl.html"
            html_body = Template(template_path.read_text(encoding="utf-8")).render(
                business_name=business_name,
                code=code,
                expires_hours=24,
            )
            self._send_email(
                to_email=to_email,
                subject=f"Kod weryfikacyjny Nevumo — {business_name}",
                html_body=html_body,
            )
            return True
        except Exception as exc:
            logger.error("[EMAIL_WARNING] send_claim_verification_email failed: %s", exc)
            return False


# Global email service instance
email_service = EmailService()
