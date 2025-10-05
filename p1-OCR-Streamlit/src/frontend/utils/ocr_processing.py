"""
Utilitaires de traitement OCR - ShelfReader P1

Ce module contient la logique métier pour le traitement OCR adaptatif multi-échelle.
Il gère la sélection et l'utilisation des différents moteurs OCR (EasyOCR, Tesseract, TrOCR).
"""

import time
from typing import Dict, List, Optional, Tuple, Any
from PIL import Image

import sys
import os
# Ajouter le répertoire parent (src) au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from engines.easyocr_engine import EasyOCRProcessor
from engines.tesseract_engine import TesseractOCRProcessor
from engines.trocr_engine import TrOCRProcessor


class OCRProcessor:
    """
    Classe principale pour le traitement OCR adaptatif.

    Cette classe orchestre l'utilisation des différents moteurs OCR et fournit
    une interface unifiée pour le traitement d'images de livres sur étagères.

    Attributs:
        engines (dict): Dictionnaire des moteurs OCR disponibles
    """

    def __init__(self):
        """Initialise les moteurs OCR disponibles."""
        self.engines = {
            'EasyOCR': None,  # Sera initialisé à la demande
            'Tesseract': None,
            'TrOCR': None
        }

    def get_processor(self, engine_name: str, confidence: float = 0.3, use_gpu: bool = True) -> Any:
        """
        Récupère ou crée un processeur OCR pour le moteur spécifié.

        Args:
            engine_name (str): Nom du moteur ('EasyOCR', 'Tesseract', 'TrOCR')
            confidence (float): Seuil de confiance pour le filtrage (0.0-1.0)
            use_gpu (bool): Utilisation du GPU si disponible

        Returns:
            Any: Instance du processeur OCR approprié

        Raises:
            ValueError: Si le moteur spécifié n'est pas supporté
        """
        if engine_name not in self.engines:
            raise ValueError(f"Moteur OCR inconnu : {engine_name}")

        if self.engines[engine_name] is None:
            if engine_name == 'EasyOCR':
                self.engines[engine_name] = EasyOCRProcessor(['en'], confidence, use_gpu)
            elif engine_name == 'Tesseract':
                self.engines[engine_name] = TesseractOCRProcessor('eng', confidence, use_gpu)
            elif engine_name == 'TrOCR':
                self.engines[engine_name] = TrOCRProcessor(['en'], confidence, use_gpu)

        return self.engines[engine_name]

    def process_image(self, image_path: str, engine_name: str = 'EasyOCR',
                     confidence: float = 0.3, use_gpu: bool = True,
                     debug: bool = False) -> Tuple[Optional[Dict], float]:
        """
        Traite une image avec le moteur OCR spécifié.

        Cette fonction est le cœur du traitement OCR adaptatif. Elle utilise
        des algorithmes spécialisés pour la détection de livres sur étagères,
        avec préprocessing intelligent et méthodes de détection de dos de livres.

        Args:
            image_path (str): Chemin vers l'image à traiter
            engine_name (str): Moteur OCR à utiliser ('EasyOCR', 'Tesseract', 'TrOCR')
            confidence (float): Seuil de confiance minimum (0.0-1.0)
            use_gpu (bool): Utilisation du GPU pour accélérer le traitement
            debug (bool): Mode debug pour analyses détaillées

        Returns:
            Tuple[Optional[Dict], float]: (résultats, temps de traitement)
                - results: dict avec 'books', 'text', 'confidence' ou None si erreur
                - processing_time: temps en secondes

        Note:
            Pour EasyOCR, utilise la détection spécialisée de dos de livres
            avec la méthode "shelfie" pour optimiser la reconnaissance sur étagères.
        """
        try:
            start_time = time.time()

            # Charger l'image
            pil_image = Image.open(image_path)

            # Récupérer le processeur approprié
            processor = self.get_processor(engine_name, confidence, use_gpu)

            # Traitement spécifique selon le moteur
            if engine_name == 'EasyOCR':
                # EasyOCR avec détection spécialisée de dos de livres
                boxes = processor.get_boxes(
                    pil_image,
                    preprocess=False,  # Préprocessing déjà fait dans le moteur
                    use_spine_detection=True,  # Détection intelligente des dos
                    debug=debug,
                    reference_titles=None,
                )
                text, avg_confidence = processor.get_text_and_confidence(
                    pil_image,
                    preprocess=False,
                    use_spine_detection=True,
                    reference_titles=None,
                    spine_method="shelfie"  # Méthode optimisée pour étagères
                )

            elif engine_name in ['Tesseract', 'TrOCR']:
                # Traitement standard pour Tesseract et TrOCR
                boxes = processor.get_boxes(pil_image)
                text, avg_confidence = processor.get_text_and_confidence(pil_image)

            else:
                raise ValueError(f"Moteur OCR non supporté : {engine_name}")

            processing_time = time.time() - start_time

            results = {
                'books': boxes,
                'text': text,
                'confidence': avg_confidence,
                'processing_time': processing_time,
                'engine': engine_name
            }

            return results, processing_time

        except Exception as e:
            print(f"Erreur lors du traitement OCR avec {engine_name}: {str(e)}")
            return None, 0.0

    def compare_engines(self, image_path: str, engines: List[str],
                       confidence: float = 0.3, use_gpu: bool = True,
                       debug: bool = False) -> Dict[str, Tuple[Optional[Dict], float]]:
        """
        Compare plusieurs moteurs OCR sur la même image.

        Utile pour évaluer les performances relatives des différents moteurs
        et choisir le plus adapté selon le cas d'usage.

        Args:
            image_path (str): Chemin vers l'image à analyser
            engines (List[str]): Liste des moteurs à comparer
            confidence (float): Seuil de confiance pour tous les moteurs
            use_gpu (bool): Utilisation du GPU pour tous les moteurs
            debug (bool): Mode debug pour analyses détaillées

        Returns:
            Dict[str, Tuple[Optional[Dict], float]]: Résultats par moteur
                clé = nom du moteur, valeur = (résultats, temps de traitement)
        """
        results = {}

        for engine_name in engines:
            print(f"Traitement avec {engine_name}...")
            result, processing_time = self.process_image(
                image_path, engine_name, confidence, use_gpu, debug
            )
            results[engine_name] = (result, processing_time)

        return results


# Instance globale pour éviter les réinitialisations
ocr_processor = OCRProcessor()