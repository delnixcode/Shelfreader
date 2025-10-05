"""
ShelfReader - Tesseract Image Preprocessing
Module de prétraitement d'images pour Tesseract.
"""

import cv2
from ..config import (
    CLAHE_CLIP_LIMIT, CLAHE_TILE_GRID_SIZE,
    BILATERAL_D, BILATERAL_SIGMA_COLOR, BILATERAL_SIGMA_SPACE
)


class TesseractPreprocessing:
    """Utilitaires de prétraitement d'images pour Tesseract."""

    @staticmethod
    def preprocess_image(image):
        """
        Prétraitement rapide et efficace pour Tesseract.

        Args:
            image: Image numpy array (BGR)

        Returns:
            Liste d'images prétraitées (une seule pour Tesseract)
        """
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Améliorer le contraste avec CLAHE
        clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP_LIMIT, tileGridSize=CLAHE_TILE_GRID_SIZE)
        enhanced = clahe.apply(gray)

        # Léger débruitage pour améliorer la qualité
        denoised = cv2.bilateralFilter(enhanced, BILATERAL_D, BILATERAL_SIGMA_COLOR, BILATERAL_SIGMA_SPACE)

        return [denoised]  # Retourner une seule image optimisée