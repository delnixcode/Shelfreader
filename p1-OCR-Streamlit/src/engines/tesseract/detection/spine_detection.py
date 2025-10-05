"""
ShelfReader - Tesseract Spine Detection
Module simplifié de détection pour Tesseract (pas de détection avancée).
"""

class TesseractSpineDetection:
    """Détection simplifiée pour Tesseract - pas de détection de tranches sophistiquée."""

    @staticmethod
    def detect_spine_lines(image, debug=False, method="simple"):
        """Tesseract n'a pas de détection de tranches avancée."""
        if debug:
            print("🔍 Tesseract: pas de détection de tranches disponible")
        return []