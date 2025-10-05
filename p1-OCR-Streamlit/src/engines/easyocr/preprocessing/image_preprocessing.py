"""
ShelfReader - EasyOCR Image Preprocessing
Module de prétraitement d'images pour optimiser la détection OCR.
"""

import cv2
import numpy as np
from ..config import (
    CLAHE_CLIP_LIMIT, CLAHE_TILE_GRID_SIZE,
    BILATERAL_D, BILATERAL_SIGMA_COLOR, BILATERAL_SIGMA_SPACE,
    GAUSSIAN_SIGMA, ADAPTIVE_BLOCK_SIZE, ADAPTIVE_C
)


class EasyOCRPreprocessing:
    """Utilitaires de prétraitement d'images pour EasyOCR."""

    @staticmethod
    def preprocess_image(image):
        """
        Prétraitement agressivement optimisé pour EasyOCR.

        Args:
            image: Image numpy array (BGR)

        Returns:
            Image prétraitée
        """
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Améliorer drastiquement le contraste avec CLAHE
        clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP_LIMIT, tileGridSize=CLAHE_TILE_GRID_SIZE)
        enhanced = clahe.apply(gray)

        # Réduction du bruit avec filtre bilatéral (préserve les bords)
        denoised = cv2.bilateralFilter(enhanced, BILATERAL_D, BILATERAL_SIGMA_COLOR, BILATERAL_SIGMA_SPACE)

        # Améliorer la netteté avec unsharp masking
        gaussian = cv2.GaussianBlur(denoised, (0, 0), GAUSSIAN_SIGMA)
        sharpened = cv2.addWeighted(denoised, 1.5, gaussian, -0.5, 0)

        # Binarisation adaptative plus agressive
        binary = cv2.adaptiveThreshold(
            sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
            ADAPTIVE_BLOCK_SIZE, ADAPTIVE_C
        )

        # Dilatation légère pour connecter les caractères
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        dilated = cv2.dilate(binary, kernel, iterations=1)

        # Reconvertir en BGR pour EasyOCR
        processed = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)

        return processed