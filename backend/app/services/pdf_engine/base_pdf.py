# backend/app/services/pdf_engine/base_pdf.py

import os

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm

styles = getSampleStyleSheet()


def build_pdf(filename: str, elements: list):
    """
    Build a PDF file and return the file path.
    """

    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    doc.build(elements)

    return filename


def title(text: str):
    return Paragraph(f"<b>{text}</b>", styles["Title"])


def section(text: str):
    return Paragraph(f"<b>{text}</b>", styles["Heading2"])


def paragraph(text: str):
    return Paragraph(text, styles["BodyText"])


def spacer():
    return Spacer(1, 12)


def table(data):
    return Table(data)