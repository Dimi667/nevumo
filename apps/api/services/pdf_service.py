"""PDF generation service for withdrawal forms."""

from io import BytesIO
from pathlib import Path
from typing import Literal

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from sqlalchemy.orm import Session

from apps.api.database import SessionLocal
from apps.api.i18n import SUPPORTED_LANGUAGES
from apps.api.models import Translation

# Register NotoSans fonts for Cyrillic support
FONTS_PATH = Path(__file__).parent.parent / "fonts"
pdfmetrics.registerFont(TTFont("NotoSans", str(FONTS_PATH / "NotoSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("NotoSans-Bold", str(FONTS_PATH / "NotoSans-Bold.ttf")))


class PDFService:
    """Service for generating PDF documents."""

    SUPPORTED_LANGUAGES = SUPPORTED_LANGUAGES

    def _fetch_pdf_translations(self, lang: str) -> dict[str, str]:
        """Fetch PDF translations from database for a specific language.

        Args:
            lang: Language code

        Returns:
            Dictionary of translation key-value pairs for PDF content

        Raises:
            ValueError: If language is not supported
        """
        if lang not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {lang}. Supported: {self.SUPPORTED_LANGUAGES}")

        db = SessionLocal()
        try:
            translations = (
                db.query(Translation)
                .filter(Translation.key.like("pdf.%"), Translation.lang == lang)
                .all()
            )
            return {t.key: t.value for t in translations}
        finally:
            db.close()

    def generate_withdrawal_form_pdf(self, lang: str) -> bytes:
        """Generate a PDF withdrawal form for the specified language.

        Args:
            lang: Language code

        Returns:
            PDF document as bytes

        Raises:
            ValueError: If language is not supported
        """
        # Fetch translations from database
        translations = self._fetch_pdf_translations(lang)

        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        # Create styles with NotoSans font for Cyrillic support
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=12,
            textColor="#000000",
            fontName="NotoSans-Bold",
        )
        heading_style = ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading2"],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=10,
            textColor="#000000",
            fontName="NotoSans-Bold",
        )
        normal_style = ParagraphStyle(
            "CustomNormal",
            parent=styles["Normal"],
            fontSize=10,
            spaceAfter=6,
            leading=14,
            textColor="#000000",
            fontName="NotoSans",
        )
        blockquote_style = ParagraphStyle(
            "CustomBlockquote",
            parent=styles["Normal"],
            fontSize=9,
            spaceAfter=8,
            spaceBefore=8,
            leftIndent=20,
            textColor="#333333",
            fontName="NotoSans",
        )

        # Build story from translations
        story = []

        # Add important notice section
        if "pdf.important_notice_title" in translations:
            story.append(Paragraph(translations["pdf.important_notice_title"], title_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.important_notice_text" in translations:
            story.append(Paragraph(translations["pdf.important_notice_text"], blockquote_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.important_notice_text_part2" in translations:
            story.append(Paragraph(translations["pdf.important_notice_text_part2"], blockquote_style))
            story.append(Spacer(1, 0.4 * cm))

        # Add right of withdrawal section
        if "pdf.right_of_withdrawal_title" in translations:
            story.append(Paragraph(translations["pdf.right_of_withdrawal_title"], title_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.right_of_withdrawal_text" in translations:
            story.append(Paragraph(translations["pdf.right_of_withdrawal_text"], normal_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.right_of_withdrawal_text_part2" in translations:
            story.append(Paragraph(translations["pdf.right_of_withdrawal_text_part2"], normal_style))
            story.append(Spacer(1, 0.4 * cm))

        # Add how to exercise withdrawal section
        if "pdf.how_to_withdrawal_title" in translations:
            story.append(Paragraph(translations["pdf.how_to_withdrawal_title"], title_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.how_to_withdrawal_text" in translations:
            story.append(Paragraph(translations["pdf.how_to_withdrawal_text"], normal_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.company_address_block" in translations:
            story.append(Paragraph(translations["pdf.company_address_block"], blockquote_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.how_to_withdrawal_text_part2" in translations:
            story.append(Paragraph(translations["pdf.how_to_withdrawal_text_part2"], normal_style))
            story.append(Spacer(1, 0.4 * cm))

        # Add effects of withdrawal section
        if "pdf.effects_of_withdrawal_title" in translations:
            story.append(Paragraph(translations["pdf.effects_of_withdrawal_title"], title_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.effects_of_withdrawal_text" in translations:
            story.append(Paragraph(translations["pdf.effects_of_withdrawal_text"], normal_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.effects_of_withdrawal_text_part2" in translations:
            story.append(Paragraph(translations["pdf.effects_of_withdrawal_text_part2"], normal_style))
            story.append(Spacer(1, 0.4 * cm))

        # Add digital services section
        if "pdf.digital_services_title" in translations:
            story.append(Paragraph(translations["pdf.digital_services_title"], title_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.digital_services_text" in translations:
            story.append(Paragraph(translations["pdf.digital_services_text"], normal_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.digital_services_text_part2" in translations:
            story.append(Paragraph(translations["pdf.digital_services_text_part2"], normal_style))
            story.append(Spacer(1, 0.4 * cm))

        # Add model form section
        if "pdf.model_form_title" in translations:
            story.append(Paragraph(translations["pdf.model_form_title"], title_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.model_form_text" in translations:
            story.append(Paragraph(translations["pdf.model_form_text"], normal_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.model_form_text_part2" in translations:
            story.append(Paragraph(translations["pdf.model_form_text_part2"], normal_style))
            story.append(Spacer(1, 0.4 * cm))

        # Add form template instruction
        if "pdf.form_template_instruction" in translations:
            story.append(Paragraph(translations["pdf.form_template_instruction"], normal_style))
            story.append(Spacer(1, 0.4 * cm))

        # Add form template to block
        if "pdf.form_template_to_block" in translations:
            story.append(Paragraph(translations["pdf.form_template_to_block"], normal_style))
            story.append(Spacer(1, 0.4 * cm))

        # Add form template declaration
        if "pdf.form_template_declaration" in translations:
            story.append(Paragraph(translations["pdf.form_template_declaration"], normal_style))
            story.append(Spacer(1, 0.4 * cm))

        # Add form fields section (reordered to match markdown structure)
        # Service description
        if "pdf.service_description_label" in translations:
            story.append(Paragraph(f"<b>{translations['pdf.service_description_label']}:</b>", normal_style))
            story.append(Spacer(1, 0.1 * cm))
        if "pdf.service_description_placeholder" in translations:
            story.append(Paragraph(translations["pdf.service_description_placeholder"], normal_style))
            story.append(Spacer(1, 0.4 * cm))

        # Contract date
        if "pdf.contract_date_label" in translations:
            story.append(Paragraph(f"<b>{translations['pdf.contract_date_label']}:</b>", normal_style))
            story.append(Spacer(1, 0.4 * cm))

        # Consumer info
        if "pdf.consumer_name_label" in translations:
            story.append(Paragraph(f"<b>{translations['pdf.consumer_name_label']}:</b>", normal_style))
            story.append(Spacer(1, 0.1 * cm))
        if "pdf.consumer_address_label" in translations:
            story.append(Paragraph(f"<b>{translations['pdf.consumer_address_label']}:</b>", normal_style))
            story.append(Spacer(1, 0.1 * cm))

        # Account info
        if "pdf.account_id_label" in translations:
            story.append(Paragraph(f"<b>{translations['pdf.account_id_label']}:</b>", normal_style))
            story.append(Spacer(1, 0.1 * cm))
        if "pdf.email_label" in translations:
            story.append(Paragraph(f"<b>{translations['pdf.email_label']}:</b>", normal_style))
            story.append(Spacer(1, 0.1 * cm))

        # Signature
        if "pdf.consumer_signature_label" in translations:
            story.append(Paragraph(f"<b>{translations['pdf.consumer_signature_label']}:</b>", normal_style))
            story.append(Spacer(1, 0.4 * cm))

        # Withdrawal date
        if "pdf.withdrawal_date_label" in translations:
            story.append(Paragraph(f"<b>{translations['pdf.withdrawal_date_label']}:</b>", normal_style))
            story.append(Spacer(1, 0.4 * cm))

        # Add how to submit section (Group 14)
        story.append(Spacer(1, 0.4 * cm))
        if "pdf.how_to_submit_title" in translations:
            story.append(Paragraph(translations["pdf.how_to_submit_title"], title_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.how_to_submit_electronic" in translations:
            story.append(Paragraph(translations["pdf.how_to_submit_electronic"], normal_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.how_to_submit_post" in translations:
            story.append(Paragraph(translations["pdf.how_to_submit_post"], normal_style))
            story.append(Spacer(1, 0.2 * cm))
        if "pdf.how_to_submit_acknowledgement" in translations:
            story.append(Paragraph(translations["pdf.how_to_submit_acknowledgement"], normal_style))

        # Build PDF
        doc.build(story)

        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes


# Global PDF service instance
pdf_service = PDFService()
