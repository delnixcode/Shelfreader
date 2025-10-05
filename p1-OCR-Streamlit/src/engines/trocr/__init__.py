# DÉPENDANCES:
#   - Utilise: logic/orchestrator.py, logic/config.py
#   - Importe: Aucun (fichier d'exports)
#   - Utilisé par: main.py, autres modules qui importent le moteur

"""
ShelfReader - TrOCR Engine
Moteur OCR basé sur TrOCR pour la reconnaissance de texte manuscrit.
"""

from .logic.orchestrator import ShelfReaderTrOCRProcessor
from .logic.config import MODEL_NAME, MAX_LENGTH, NUM_BEAMS

__all__ = [
    'ShelfReaderTrOCRProcessor',
    'MODEL_NAME',
    'MAX_LENGTH',
    'NUM_BEAMS'
]
