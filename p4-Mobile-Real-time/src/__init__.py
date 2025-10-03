"""
ShelfReader - Détection et recherche de livres sur étagère
"""

__version__ = "0.1.0"
__author__ = "Delart"

# Imports pour faciliter l'utilisation
from .api_client import OpenLibraryClient
from .ocr_processor import BookOCR

__all__ = ['OpenLibraryClient', 'BookOCR']
