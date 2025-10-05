# DÉPENDANCES:
#   - Utilise: logic/orchestrator.py, logic/config.py, preprocessing/image_preprocessing.py, detection/spine_detection.py, grouping/text_grouping.py
#   - Importe: Aucun (fichier d'exports)
#   - Utilisé par: main.py, autres modules qui importent le moteur

"""
ShelfReader - Tesseract Engine
Moteur OCR spécialisé pour Tesseract.
"""

from .logic.orchestrator import TesseractOCRProcessor
from .logic.config import *
from .preprocessing.image_preprocessing import TesseractPreprocessing
from .detection.spine_detection import TesseractSpineDetection
from .grouping.text_grouping import TesseractTextGrouping

__all__ = [
    'TesseractOCRProcessor',
    'TesseractPreprocessing',
    'TesseractSpineDetection',
    'TesseractTextGrouping'
]
