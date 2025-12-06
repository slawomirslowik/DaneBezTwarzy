"""
Moduł wizualizacji raportów.
"""

from .html_reporter import generate_html_report
from .pdf_reporter import generate_pdf_report

__all__ = ['generate_html_report', 'generate_pdf_report']
