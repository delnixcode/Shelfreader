"""
ShelfReader - TrOCR Image Preprocessing
Préparation des images pour TrOCR.
"""

import cv2
import numpy as np
from PIL import Image
import torch
from transformers import TrOCRProcessor

class TrOCRImagePreprocessor:
    """Préprocesseur d'images pour TrOCR."""

    def __init__(self, processor: TrOCRProcessor):
        """
        Initialise le préprocesseur.

        Args:
            processor: Processeur TrOCR pour la préparation des images
        """
        self.processor = processor

    def preprocess_image(self, image: np.ndarray) -> torch.Tensor:
        """
        Prétraite une image pour TrOCR.

        Args:
            image: Image d'entrée (numpy array)

        Returns:
            Tensor préparé pour le modèle
        """
        # S'assurer que l'image est en RGB
        if len(image.shape) == 2:  # Image en niveaux de gris
            # Convertir en RGB en dupliquant les canaux
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 1:  # Image avec un seul canal
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        # Convertir en PIL Image
        pil_image = Image.fromarray(image)

        # Utiliser le processeur TrOCR
        pixel_values = self.processor(pil_image, return_tensors="pt").pixel_values

        return pixel_values

    def segment_into_strips(self, image: np.ndarray, num_strips: int = 14) -> list[np.ndarray]:
        """
        Segmente l'image en bandes verticales pour le traitement.

        Args:
            image: Image d'entrée
            num_strips: Nombre de bandes verticales

        Returns:
            Liste des bandes d'image
        """
        height, width = image.shape[:2]
        strip_width = width // num_strips

        strips = []
        for i in range(num_strips):
            start_x = i * strip_width
            end_x = (i + 1) * strip_width if i < num_strips - 1 else width

            strip = image[:, start_x:end_x]
            strips.append(strip)

        return strips

    def enhance_image(self, image: np.ndarray) -> np.ndarray:
        """
        Améliore la qualité de l'image pour une meilleure OCR.

        Args:
            image: Image d'entrée

        Returns:
            Image améliorée
        """
        # Convertir en niveaux de gris si nécessaire
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Améliorer le contraste
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # Réduire le bruit
        denoised = cv2.medianBlur(enhanced, 3)

        return denoised