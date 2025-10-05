"""
ShelfReader - TrOCR Engine
Moteur OCR basé sur TrOCR pour la reconnaissance de texte manuscrit.
"""

from .processor import ShelfReaderTrOCRProcessor
from .config import MODEL_NAME, MAX_LENGTH, NUM_BEAMS

__all__ = [
    'ShelfReaderTrOCRProcessor',
    'MODEL_NAME',
    'MAX_LENGTH',
    'NUM_BEAMS'
]
