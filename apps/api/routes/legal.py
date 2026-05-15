"""Legal document routes for PDF generation and withdrawal form submission."""

from datetime import date
from typing import Literal, Optional

from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import Response as FastAPIResponse
from pydantic import BaseModel, EmailStr, field_validator

from apps.api.services.email_service import email_service
from apps.api.services.pdf_service import pdf_service

router = APIRouter(prefix="/api/v1/legal", tags=["legal"])


class WithdrawalFormRequest(BaseModel):
    """Request schema for withdrawal form submission."""
    service_description: str
    contract_date: date
    consumer_name: str
    consumer_address: str
    account_id: Optional[str] = None
    email: EmailStr
    submission_date: date
    lang: str

    @field_validator('service_description', 'consumer_name', 'consumer_address')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()

    @field_validator('lang')
    @classmethod
    def validate_lang(cls, v: str) -> str:
        valid_langs = ['en', 'bg', 'pl']
        if v not in valid_langs:
            raise ValueError(f'Language must be one of: {", ".join(valid_langs)}')
        return v


@router.get("/withdrawal-form/{lang}")
async def get_withdrawal_form_pdf(lang: Literal["en", "bg", "pl"]) -> FastAPIResponse:
    """Generate and return withdrawal form PDF for the specified language.

    Args:
        lang: Language code (en, bg, pl)

    Returns:
        PDF document as downloadable file

    Raises:
        HTTPException: If language is not supported or PDF generation fails
    """
    try:
        pdf_bytes = pdf_service.generate_withdrawal_form_pdf(lang)
        return FastAPIResponse(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="withdrawal-form-{lang}.pdf"',
                "Content-Type": "application/pdf",
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")


@router.post("/withdrawal")
async def submit_withdrawal_form(request: WithdrawalFormRequest) -> dict:
    """Submit withdrawal form and send email to legal@nevumo.com.

    Args:
        request: Withdrawal form data with all required fields

    Returns:
        Success response with submission confirmation

    Raises:
        HTTPException: If validation fails or email sending fails
    """
    try:
        # Send email via email service
        email_sent = email_service.send_withdrawal_form_email(
            service_description=request.service_description,
            contract_date=request.contract_date,
            consumer_name=request.consumer_name,
            consumer_address=request.consumer_address,
            account_id=request.account_id,
            email=request.email,
            submission_date=request.submission_date,
            lang=request.lang
        )

        if not email_sent:
            raise HTTPException(
                status_code=500,
                detail="Failed to send withdrawal form email"
            )

        return {
            "success": True,
            "message": "Withdrawal form submitted successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process withdrawal form: {str(e)}")
