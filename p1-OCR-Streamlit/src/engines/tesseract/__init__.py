"""
ShelfReader - Tesseract Engine
Moteur OCR spécialisé pour Tesseract.
"""

from .processor import TesseractOCRProcessor
from .config import *
from .preprocessing.image_preprocessing import TesseractPreprocessing
from .detection.spine_detection import TesseractSpineDetection
from .grouping.text_grouping import TesseractTextGrouping

__all__ = [
    'TesseractOCRProcessor',
    'TesseractPreprocessing',
    'TesseractSpineDetection',
    'TesseractTextGrouping'
]
