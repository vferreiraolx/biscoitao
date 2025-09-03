"""
Biscoitão Generators Module
Geradores de relatórios e visualizações
"""

from .visual_assistant import IntelligentReportGenerator
from .html_generator import HTMLReportGenerator  
from .pdf_generator import ProfessionalPDFReportGenerator

__all__ = ['IntelligentReportGenerator', 'HTMLReportGenerator', 'ProfessionalPDFReportGenerator']
