"""
Utilitaires de traitement OCR - ShelfReader P1

Ce module contient la logique métier pour le traitement OCR adaptatif multi-échelle.
Il gère la sélection et l'utilisation des différents moteurs OCR (EasyOCR, Tesseract, TrOCR).
"""

import time
from typing import Dict, List, Optional, Tuple, Any

from PIL import Image
import numpy as np


import sys
import os

# Ajouter le répertoire parent (src) au path
SRC_PATH = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    ),
    'src'
)
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from engines.easyocr.logic.orchestrator import EasyOCRProcessor
from engines.tesseract.logic.orchestrator import TesseractOCRProcessor
from engines.trocr.logic.orchestrator import ShelfReaderTrOCRProcessor


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

    def get_processor(self, engine_name: str, confidence: float = 0.3, use_gpu: bool = True, 
                      advanced_params: Dict = None) -> Any:
        """
        Récupère ou crée un processeur OCR pour le moteur spécifié.

        Args:
            engine_name (str): Nom du moteur ('EasyOCR', 'Tesseract', 'TrOCR')
            confidence (float): Seuil de confiance pour le filtrage (0.0-1.0)
            use_gpu (bool): Utilisation du GPU si disponible
            advanced_params (Dict): Paramètres avancés spécifiques au moteur

        Returns:
            Any: Instance du processeur OCR approprié

        Raises:
            ValueError: Si le moteur spécifié n'est pas supporté
        """
        if engine_name not in self.engines:
            raise ValueError(f"Moteur OCR inconnu : {engine_name}")

        # Toujours créer une nouvelle instance pour s'assurer que les paramètres sont à jour
        # (notamment le seuil de confiance qui peut changer dynamiquement)
        if engine_name == 'EasyOCR':
            # Utiliser les paramètres avancés si disponibles
            if advanced_params:
                languages = advanced_params.get('languages', ['en'])
                conf_threshold = advanced_params.get('confidence', confidence)
                gpu = advanced_params.get('use_gpu', use_gpu)
            else:
                languages = ['en']
                conf_threshold = confidence
                gpu = use_gpu
            
            processor = EasyOCRProcessor(languages, conf_threshold, gpu)
            
        elif engine_name == 'Tesseract':
            # Utiliser les paramètres avancés si disponibles
            if advanced_params:
                lang = advanced_params.get('lang', 'eng')
                conf_threshold = advanced_params.get('confidence', confidence)
            else:
                lang = 'eng'
                conf_threshold = confidence
            
            # Tesseract utilise des confiances en pourcentage (0-100), convertir le seuil
            processor = TesseractOCRProcessor(lang, conf_threshold * 100, False)  # Convertir en pourcentage
            
        elif engine_name == 'TrOCR':
            # Utiliser les paramètres avancés si disponibles
            if advanced_params:
                device = advanced_params.get('device', 'auto')
            else:
                device = 'cuda' if use_gpu else 'cpu'
            
            processor = ShelfReaderTrOCRProcessor(device)
        else:
            raise ValueError(f"Moteur OCR non supporté : {engine_name}")

        # Stocker la nouvelle instance
        self.engines[engine_name] = processor
        return processor

    def process_image(self, image_path: str, engine_name: str = 'EasyOCR',
                     confidence: float = 0.3, use_gpu: bool = True,
                     debug: bool = False, advanced_params: Dict = None) -> Tuple[Optional[Dict], float]:
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
            advanced_params (Dict): Paramètres avancés spécifiques au moteur

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

            # Récupérer le processeur approprié avec paramètres avancés
            processor = self.get_processor(engine_name, confidence, use_gpu, advanced_params)

            # Traitement spécifique selon le moteur
            if engine_name == 'EasyOCR':
                # Récupérer les paramètres avancés pour EasyOCR
                spine_method = "shelfie"  # défaut
                if advanced_params and 'spine_method' in advanced_params:
                    spine_method = advanced_params['spine_method']
                
                # EasyOCR avec détection spécialisée de dos de livres
                boxes = processor.get_boxes(
                    pil_image,
                    preprocess=False,  # Préprocessing déjà fait dans le moteur
                    use_spine_detection=True,  # Détection intelligente des dos
                    debug=debug,
                    reference_titles=None,
                    spine_method=spine_method
                )
                text, avg_confidence = processor.get_text_and_confidence(
                    pil_image,
                    preprocess=False,
                    use_spine_detection=True,
                    reference_titles=None,
                    spine_method=spine_method
                )

            elif engine_name == 'Tesseract':
                # Traitement standard pour Tesseract
                boxes = processor.get_boxes(pil_image)
                text, avg_confidence = processor.get_text_and_confidence(pil_image)
                
            elif engine_name == 'TrOCR':
                # TrOCR: process_image returns list of dicts with text/confidence/bbox
                image_np = np.array(pil_image)
                trocr_results = processor.process_image(image_np)

                # Convert TrOCR format to standard format expected by visualization
                # and apply confidence filtering
                boxes = []
                filtered_results = []
                for result in trocr_results:
                    result_confidence = result.get('confidence', 0.0)
                    if result_confidence >= confidence:  # Apply confidence threshold
                        if 'bbox' in result and len(result['bbox']) >= 4:
                            x, y, w, h = result['bbox']
                            boxes.append({
                                'x': x,
                                'y': y,
                                'width': w,
                                'height': h,
                                'text': result.get('text', ''),
                                'confidence': result_confidence
                            })
                        filtered_results.append(result)

                text = '\n'.join([r.get('text','') for r in filtered_results]) if filtered_results else ''
                avg_confidence = (sum([r.get('confidence',0) for r in filtered_results])/len(filtered_results)) if filtered_results else 0.0

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
                       debug: bool = False, advanced_params: Dict = None) -> Dict[str, Dict]:
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
            advanced_params (Dict): Paramètres avancés par moteur

        Returns:
            Dict[str, Dict]: Résultats par moteur
                clé = nom du moteur, valeur = résultats du moteur
        """
        results = {}

        for engine_name in engines:
            print(f"Traitement avec {engine_name}...")
            # Utiliser les paramètres avancés spécifiques au moteur si disponibles
            engine_advanced_params = advanced_params.get(engine_name, {}) if advanced_params else None
            
            result, processing_time = self.process_image(
                image_path, engine_name, confidence, use_gpu, debug, engine_advanced_params
            )
            
            if result:
                result['processing_time'] = processing_time
                results[engine_name] = result
            else:
                results[engine_name] = {
                    'books': [],
                    'text': '',
                    'confidence': 0.0,
                    'processing_time': processing_time
                }

        return results


# Instance globale pour éviter les réinitialisations
ocr_processor = OCRProcessor()