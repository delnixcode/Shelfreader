"""
ShelfReader - Tesseract OCR Processor
Processeur OCR spécialisé pour Tesseract.
"""

import numpy as np
import cv2
from PIL import Image
import pytesseract
from pytesseract import Output
from .preprocessing.image_preprocessing import TesseractPreprocessing
from .grouping.text_grouping import TesseractTextGrouping
from .config import PSM_CONFIGS, MAX_RESULTS, MIN_TEXT_LENGTH


class TesseractOCRProcessor:
    """Processeur OCR spécialisé pour Tesseract."""

    def __init__(self, languages, confidence_threshold, use_gpu=False):
        """Initialise Tesseract."""
        try:
            import cv2
            import numpy as np
            from PIL import Image
            import pytesseract
            from pytesseract import Output
        except ImportError as e:
            raise ImportError(f"Tesseract nécessite des dépendances manquantes: {e}")

        self.confidence_threshold = confidence_threshold
        self.languages = languages
        self.use_gpu = use_gpu  # Tesseract ne supporte pas vraiment GPU

        print(f"🔍 Tesseract initialisé - Langues: {languages}, Seuil: {confidence_threshold}")

    def _detect_with_psm(self, image, psm_config):
        """Détection avec une configuration PSM spécifique."""
        try:
            config = f'{psm_config} -l {self.languages}'
            data = pytesseract.image_to_data(image, config=config, output_type=Output.DICT)

            results = []
            n_boxes = len(data['text'])
            for i in range(n_boxes):
                confidence = int(data['conf'][i])
                text = data['text'][i].strip()

                if confidence > self.confidence_threshold and len(text) >= MIN_TEXT_LENGTH:
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    bbox = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
                    results.append((bbox, text, confidence / 100.0))

            return results
        except Exception as e:
            print(f"Erreur avec PSM {psm_config}: {e}")
            return []

    def detect_text(self, pil_image, preprocess=True):
        """Détecte le texte avec Tesseract."""
        image_array = np.array(pil_image)
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Prétraitement si demandé
        if preprocess:
            processed_images = TesseractPreprocessing.preprocess_image(bgr_image)
        else:
            processed_images = [cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)]

        # Utiliser la meilleure configuration PSM
        all_results = []
        for processed_img in processed_images:
            results = self._detect_with_psm(processed_img, PSM_CONFIGS[0])
            all_results.extend(results)

        # Trier par confiance et limiter les résultats
        all_results.sort(key=lambda x: x[2], reverse=True)
        return all_results[:MAX_RESULTS]

    def get_text_and_confidence(self, pil_image, preprocess=True, use_spine_detection=True, reference_titles=None, spine_method="simple"):
        """Extrait le texte et la confiance moyenne."""
        boxes = self.get_boxes(pil_image, preprocess=preprocess, use_spine_detection=use_spine_detection)

        texts = [b['text'] for b in boxes]
        confidences = [b['confidence'] for b in boxes]

        full_text = ' | '.join(texts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return full_text, avg_confidence

    def get_boxes(self, pil_image, preprocess=True, vertical_only=False, use_spine_detection=True, debug=False, reference_titles=None, spine_method="simple"):
        """Extrait les boîtes de texte avec coordonnées."""
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

        # Regrouper si demandé
        if boxes and use_spine_detection:
            boxes = TesseractTextGrouping.group_texts_by_spine_lines(boxes, None, debug=debug, method=spine_method)

        return boxes