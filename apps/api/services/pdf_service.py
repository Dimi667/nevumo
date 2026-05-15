"""PDF generation service for withdrawal forms."""

import re
from io import BytesIO
from pathlib import Path
from typing import Literal

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

# Register NotoSans fonts for Cyrillic support
FONTS_PATH = Path(__file__).parent.parent / "fonts"
pdfmetrics.registerFont(TTFont("NotoSans", str(FONTS_PATH / "NotoSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("NotoSans-Bold", str(FONTS_PATH / "NotoSans-Bold.ttf")))


class PDFService:
    """Service for generating PDF documents."""

    SUPPORTED_LANGUAGES = ("en", "bg", "pl")

    def __init__(self) -> None:
        self._markdown_path = Path(__file__).parent.parent.parent.parent / "docs" / "withdrawal_form_nevumo.md"

    def _extract_language_text(self, lang: str) -> str:
        """Extract withdrawal form text for a specific language from the markdown file.

        Args:
            lang: Language code (en, bg, pl)

        Returns:
            The text content for the specified language

        Raises:
            ValueError: If language is not supported
            FileNotFoundError: If markdown file doesn't exist
        """
        if lang not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {lang}. Supported: {self.SUPPORTED_LANGUAGES}")

        if not self._markdown_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {self._markdown_path}")

        content = self._markdown_path.read_text(encoding="utf-8")

        # Extract language-specific sections based on headers
        if lang == "pl":
            # Polish section starts at "## 🇵🇱 WERSJA POLSKA" and ends before "## 🇬🇧 ENGLISH VERSION"
            start_marker = "## 🇵🇱 WERSJA POLSKA"
            end_marker = "## 🇬🇧 ENGLISH VERSION"
        elif lang == "en":
            # English section starts at "## 🇬🇧 ENGLISH VERSION" and ends before "## 🇧🇬 БЪЛГАРСКА ВЕРСИЯ"
            start_marker = "## 🇬🇧 ENGLISH VERSION"
            end_marker = "## 🇧🇬 БЪЛГАРСКА ВЕРСИЯ"
        else:  # bg
            # Bulgarian section starts at "## 🇧🇬 БЪЛГАРСКА ВЕРСИЯ" and ends before "## 📋 БЕЛЕЖКИ ЗА РАЗРАБОТЧИКА"
            start_marker = "## 🇧🇬 БЪЛГАРСКА ВЕРСИЯ"
            end_marker = "## 📋 БЕЛЕЖКИ ЗА РАЗРАБОТЧИКА"

        start_idx = content.find(start_marker)
        if start_idx == -1:
            raise ValueError(f"Could not find section marker: {start_marker}")

        end_idx = content.find(end_marker, start_idx)
        if end_idx == -1:
            # If end marker not found, take everything after start
            text = content[start_idx:]
        else:
            text = content[start_idx:end_idx]

        return text.strip()

    def generate_withdrawal_form_pdf(self, lang: Literal["en", "bg", "pl"]) -> bytes:
        """Generate a PDF withdrawal form for the specified language.

        Args:
            lang: Language code (en, bg, pl)

        Returns:
            PDF document as bytes

        Raises:
            ValueError: If language is not supported
        """
        # Extract markdown text for the language
        markdown_text = self._extract_language_text(lang)

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

        # Parse markdown and build story
        story = []
        lines = markdown_text.split("\n")
        current_style = normal_style
        in_blockquote = False
        current_paragraph = []

        for line in lines:
            line = line.rstrip()

            # Skip empty lines
            if not line:
                if current_paragraph:
                    paragraph_text = " ".join(current_paragraph)
                    paragraph_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', paragraph_text)
                    # Handle line breaks
                    paragraph_text = paragraph_text.replace("\n", "<br/>")
                    story.append(Paragraph(paragraph_text, current_style))
                    story.append(Spacer(1, 0.2 * cm))
                    current_paragraph = []
                continue

            # Check for headers
            if line.startswith("### "):
                if current_paragraph:
                    paragraph_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', paragraph_text)
                    story.append(Paragraph(paragraph_text, current_style))
                    story.append(Spacer(1, 0.2 * cm))
                    current_paragraph = []
                header_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line[4:])
                story.append(Paragraph(header_text, heading_style))
                story.append(Spacer(1, 0.3 * cm))
                current_style = normal_style
                continue

            if line.startswith("## "):
                if current_paragraph:
                    paragraph_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', paragraph_text)
                    story.append(Spacer(1, 0.2 * cm))
                    current_paragraph = []
                header_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line[3:])
                story.append(Paragraph(header_text, title_style))
                story.append(Spacer(1, 0.4 * cm))
                current_style = normal_style
                continue

            # Check for blockquote markers
            if line.startswith("> "):
                if current_paragraph:
                    paragraph_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', paragraph_text)
                    story.append(Paragraph(paragraph_text, current_style))
                    story.append(Spacer(1, 0.2 * cm))
                    current_paragraph = []
                quote_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line[2:])
                story.append(Paragraph(quote_text, blockquote_style))
                story.append(Spacer(1, 0.2 * cm))
                in_blockquote = True
                continue

            # Check for horizontal rule
            if line.strip() == "---":
                if current_paragraph:
                    paragraph_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', paragraph_text)
                    story.append(Paragraph(paragraph_text, current_style))
                    current_paragraph = []
                story.append(Spacer(1, 0.4 * cm))
                in_blockquote = False
                current_style = normal_style
                continue

            # Regular text
            current_paragraph.append(line)

        # Add any remaining paragraph
        if current_paragraph:
            paragraph_text = " ".join(current_paragraph)
            paragraph_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', paragraph_text)
            story.append(Paragraph(paragraph_text, current_style))

        # Build PDF
        doc.build(story)

        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes


# Global PDF service instance
pdf_service = PDFService()
