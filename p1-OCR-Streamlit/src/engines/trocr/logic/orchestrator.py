# DÉPENDANCES:
#   - Utilise: config.py, preprocessing/image_preprocessing.py, detection/text_detection.py, grouping/text_grouping.py
#   - Importe: torch, numpy, transformers, typing, logging
#   - Utilisé par: __init__.py, main.py

"""
ShelfReader - TrOCR Processor
Processeur principal pour TrOCR.
"""

import torch
import numpy as np
from transformers import VisionEncoderDecoderModel, TrOCRProcessor
from typing import List, Dict, Any, Optional
import logging

from .config import *
from ..preprocessing.image_preprocessing import TrOCRImagePreprocessor
from ..detection.text_detection import TrOCRTextDetector
from ..grouping.text_grouping import TrOCRTextGrouper

logger = logging.getLogger(__name__)

class ShelfReaderTrOCRProcessor:
    """Processeur principal pour TrOCR."""

    def __init__(self, device: str = 'auto'):
        """
        Initialise le processeur TrOCR.

        Args:
            device: Device pour l'inférence ('cpu', 'cuda', 'auto')
        """
        self.device = self._setup_device(device)

        # Charger le modèle et le processeur
        logger.info(f"Chargement du modèle TrOCR: {MODEL_NAME}")
        self.model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)
        self.processor = TrOCRProcessor.from_pretrained(MODEL_NAME)

        # Déplacer le modèle sur le device approprié
        self.model.to(self.device)

        # Initialiser les composants modulaires
        self.preprocessor = TrOCRImagePreprocessor(self.processor)
        self.detector = TrOCRTextDetector()
        self.grouper = TrOCRTextGrouper()

        logger.info("TrOCR Processor initialisé avec succès")

    def _setup_device(self, device: str) -> str:
        """Configure le device pour l'inférence."""
        if device == 'auto':
            return 'cuda' if torch.cuda.is_available() else 'cpu'
        return device

    def process_image(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Traite une image complète avec TrOCR.

        Args:
            image: Image d'entrée (numpy array)

        Returns:
            Liste des résultats de texte détecté
        """
        try:
            # Prétraitement
            enhanced_image = self.preprocessor.enhance_image(image)

            # Détection des régions de texte
            regions = self.detector.detect_text_regions(enhanced_image)

            # Traiter chaque région
            text_results = []
            for region in regions:
                x, y, w, h = region
                roi = enhanced_image[y:y+h, x:x+w]

                # OCR sur la région
                result = self._ocr_region(roi, region)
                if result:
                    text_results.append(result)

            # Regrouper les résultats
            grouped_lines = self.grouper.group_text_lines(text_results)

            # Filtrer les résultats de faible confiance
            filtered_results = self.grouper.filter_low_confidence(grouped_lines)

            return filtered_results

        except Exception as e:
            logger.error(f"Erreur lors du traitement TrOCR: {e}")
            return []

    def _ocr_region(self, region: np.ndarray, bbox: tuple) -> Optional[Dict[str, Any]]:
        """
        Effectue l'OCR sur une région spécifique.

        Args:
            region: Région d'image à traiter
            bbox: Boîte englobante (x, y, w, h)

        Returns:
            Résultat de l'OCR ou None si échec
        """
        try:
            # Préparer l'image pour le modèle
            pixel_values = self.preprocessor.preprocess_image(region)

            # Déplacer sur le device
            pixel_values = pixel_values.to(self.device)

            # Générer le texte
            with torch.no_grad():
                generated_ids = self.model.generate(
                    pixel_values,
                    max_length=MAX_LENGTH,
                    num_beams=NUM_BEAMS,
                    early_stopping=EARLY_STOPPING,
                    no_repeat_ngram_size=NO_REPEAT_NGRAM_SIZE,
                    length_penalty=LENGTH_PENALTY,
                    repetition_penalty=REPETITION_PENALTY
                )

            # Décoder le texte généré
            generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

            # Calculer une confiance approximative (TrOCR ne fournit pas de scores de confiance directs)
            confidence = self._estimate_confidence(generated_text)

            if confidence > 0.3:  # Seuil minimum
                return {
                    'text': generated_text.strip(),
                    'bbox': list(bbox),
                    'confidence': confidence,
                    'source': 'trocr'
                }

        except Exception as e:
            logger.error(f"Erreur OCR sur région: {e}")

        return None

    def _estimate_confidence(self, text: str) -> float:
        """
        Estime la confiance basée sur la longueur et la complexité du texte.

        Args:
            text: Texte généré

        Returns:
            Score de confiance estimé (0-1)
        """
        if not text or not text.strip():
            return 0.0

        # Facteurs simples pour estimer la confiance
        length_score = min(len(text.strip()) / 20, 1.0)  # Plus c'est long, mieux c'est
        alpha_ratio = sum(c.isalnum() for c in text) / len(text) if text else 0  # Ratio de caractères alphanumériques

        # Score composite
        confidence = (length_score * 0.6) + (alpha_ratio * 0.4)

        return min(confidence, 1.0)

    def get_model_info(self) -> Dict[str, Any]:
        """Retourne les informations sur le modèle."""
        return {
            'model_name': MODEL_NAME,
            'device': self.device,
            'max_length': MAX_LENGTH,
            'num_beams': NUM_BEAMS,
            'model_parameters': sum(p.numel() for p in self.model.parameters())
        }