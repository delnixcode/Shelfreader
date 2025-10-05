"""
ShelfReader - EasyOCR Engine
Moteur OCR spécialisé pour EasyOCR avec détection de tranches.
"""

from .processor import EasyOCRProcessor
from .config import *
from .models.line import Line
from .preprocessing.image_preprocessing import EasyOCRPreprocessing
from .detection.spine_detection import EasyOCRSpineDetection
from .grouping.text_grouping import EasyOCRTextGrouping

__all__ = [
    'EasyOCRProcessor',
    'EasyOCRPreprocessing',
    'EasyOCRSpineDetection',
    'EasyOCRTextGrouping',
    'Line'
]
