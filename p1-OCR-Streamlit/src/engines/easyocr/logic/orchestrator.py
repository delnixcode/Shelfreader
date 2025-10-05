# DÉPENDANCES:
#   - Utilise: preprocessing/image_preprocessing.py, detection/spine_detection.py, grouping/text_grouping.py, config.py
#   - Importe: numpy, cv2 (opencv), PIL (Pillow)
#   - Utilisé par: __init__.py, main.py

"""
ShelfReader - EasyOCR Processor
Processeur OCR spécialisé pour EasyOCR avec détection de tranches.
"""

import numpy as np
import cv2
from PIL import Image
from ..preprocessing.image_preprocessing import EasyOCRPreprocessing
from ..detection.spine_detection import EasyOCRSpineDetection
from ..grouping.text_grouping import EasyOCRTextGrouping
from .config import (
    OCR_WIDTH_THS, OCR_HEIGHT_THS, OCR_CONTRAST_THS,
    OCR_ADJUST_CONTRAST, OCR_TEXT_THRESHOLD, OCR_LINK_THRESHOLD
)


class EasyOCRProcessor:
    """Processeur OCR spécialisé pour EasyOCR avec détection de tranches."""

    def __init__(self, languages, confidence_threshold, use_gpu=False):
        """Initialise EasyOCR."""
        try:
            import easyocr
        except ImportError as e:
            raise ImportError(f"EasyOCR nécessite des dépendances manquantes: {e}")

        self.confidence_threshold = confidence_threshold
        self.reader = easyocr.Reader(languages, gpu=use_gpu)
        device = "GPU" if use_gpu else "CPU"
        print(f"🔍 EasyOCR initialisé - Langues: {languages}, Seuil: {confidence_threshold}, Device: {device}")

    def detect_text(self, pil_image, preprocess=True):
        """Détecte le texte avec EasyOCR."""
        image_array = np.array(pil_image)
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Prétraitement si demandé
        if preprocess:
            bgr_image = EasyOCRPreprocessing.preprocess_image(bgr_image)

        # Détection OCR avec paramètres optimisés pour texte vertical
        results = self.reader.readtext(
            bgr_image,
            rotation_info=[0, 90, 180, 270],
            width_ths=OCR_WIDTH_THS,
            height_ths=OCR_HEIGHT_THS,
            contrast_ths=OCR_CONTRAST_THS,
            adjust_contrast=OCR_ADJUST_CONTRAST,
            text_threshold=OCR_TEXT_THRESHOLD,
            link_threshold=OCR_LINK_THRESHOLD
        )

        # Filtrage par confiance et longueur
        filtered_results = [
            r for r in results
            if r[2] >= self.confidence_threshold and len(r[1].strip()) >= 2
        ]

        return filtered_results

    def get_text_and_confidence(self, pil_image, preprocess=True, use_spine_detection=True, reference_titles=None, spine_method="iccc2013"):
        """Extrait le texte et la confiance moyenne."""
        boxes = self.get_boxes(pil_image, preprocess=preprocess, use_spine_detection=use_spine_detection, reference_titles=reference_titles, spine_method=spine_method)

        texts = [b['text'] for b in boxes]
        confidences = [b['confidence'] for b in boxes]

        full_text = ' | '.join(texts)  # Séparer par | pour les livres
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return full_text, avg_confidence

    def get_boxes(self, pil_image, preprocess=True, vertical_only=False, use_spine_detection=True, debug=False, reference_titles=None, spine_method="iccc2013"):
        """Extrait les boîtes de texte avec coordonnées, groupées par livre."""
        results = self.detect_text(pil_image, preprocess=preprocess)

        boxes = []
        for bbox, text, confidence in results:
            # Calcul des dimensions
            x = min([p[0] for p in bbox])
            y = min([p[1] for p in bbox])
            width = max([p[0] for p in bbox]) - x
            height = max([p[1] for p in bbox]) - y
            font_size = height

            # Détection verticale
            is_vertical = height > width * 1.5

            if vertical_only and not is_vertical:
                continue

            boxes.append({
                "text": text,
                "x": x, "y": y,
                "width": width, "height": height,
                "font_size": font_size,
                "is_vertical": is_vertical,
                "confidence": confidence
            })

        # Regrouper les boîtes par livre
        if boxes and use_spine_detection:
            # Convertir l'image PIL en numpy array pour la détection de lignes
            image_array = np.array(pil_image)
            bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

            # Utiliser le regroupement par lignes de tranches
            boxes = EasyOCRTextGrouping.group_texts_by_spine_lines(boxes, bgr_image, debug=debug, method=spine_method)
        elif boxes:
            # Méthode de secours par proximité
            boxes = EasyOCRTextGrouping.group_by_proximity(boxes)

        return boxes