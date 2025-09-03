"""
Biscoitão Core Module
Módulos centrais do sistema Biscoitão
"""

__version__ = "2.0.0"
__author__ = "OLX Data Team"

from .query import execute_query
from .data_processor import DataProcessor

__all__ = ['execute_query', 'DataProcessor']
