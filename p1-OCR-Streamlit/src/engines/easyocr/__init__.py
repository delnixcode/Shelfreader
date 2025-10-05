# DÉPENDANCES:
#   - Utilise: logic/orchestrator.py, logic/config.py, models/line.py, preprocessing/image_preprocessing.py, detection/spine_detection.py, grouping/text_grouping.py
#   - Importe: Aucun (fichier d'exports)
#   - Utilisé par: main.py, autres modules qui importent le moteur

"""
ShelfReader - EasyOCR Engine
Moteur OCR spécialisé pour EasyOCR avec détection de tranches.
"""

from .logic.orchestrator import EasyOCRProcessor
from .logic.config import *
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
