"""
ShelfReader - TrOCR Text Detection
Détection et segmentation du texte pour TrOCR.
"""

import cv2
import numpy as np
from typing import List, Tuple

class TrOCRTextDetector:
    """Détecteur de texte pour TrOCR."""

    def __init__(self, strip_height_threshold: int = 50):
        """
        Initialise le détecteur.

        Args:
            strip_height_threshold: Seuil de hauteur minimum pour considérer une bande comme contenant du texte
        """
        self.strip_height_threshold = strip_height_threshold

    def detect_text_regions(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Détecte les régions de texte dans l'image.
        Pour TrOCR, nous segmentons simplement en bandes verticales.

        Args:
            image: Image d'entrée

        Returns:
            Liste de boîtes englobantes (x, y, w, h)
        """
        height, width = image.shape[:2]

        # Diviser en bandes verticales
        num_strips = 14
        strip_width = width // num_strips

        regions = []
        for i in range(num_strips):
            x = i * strip_width
            w = strip_width if i < num_strips - 1 else (width - x)

            # Pour TrOCR, on traite toute la hauteur
            regions.append((x, 0, w, height))

        return regions

    def filter_empty_regions(self, image: np.ndarray, regions: List[Tuple[int, int, int, int]]) -> List[Tuple[int, int, int, int]]:
        """
        Filtre les régions qui ne contiennent probablement pas de texte.

        Args:
            image: Image d'entrée
            regions: Régions candidates

        Returns:
            Régions filtrées
        """
        filtered_regions = []

        for region in regions:
            x, y, w, h = region

            # Extraire la région
            roi = image[y:y+h, x:x+w]

            # Calculer la variance pour détecter le contenu
            if len(roi.shape) == 3:
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            else:
                gray_roi = roi

            variance = np.var(gray_roi)

            # Garder la région si elle a suffisamment de variance (contenu)
            if variance > 100:  # Seuil arbitraire
                filtered_regions.append(region)

        return filtered_regions

    def merge_adjacent_regions(self, regions: List[Tuple[int, int, int, int]], max_gap: int = 10) -> List[Tuple[int, int, int, int]]:
        """
        Fusionne les régions adjacentes.

        Args:
            regions: Régions à fusionner
            max_gap: Écart maximum entre régions pour la fusion

        Returns:
            Régions fusionnées
        """
        if not regions:
            return regions

        # Trier par position x
        sorted_regions = sorted(regions, key=lambda r: r[0])

        merged = [sorted_regions[0]]

        for current in sorted_regions[1:]:
            last = merged[-1]

            # Vérifier si les régions sont adjacentes
            if current[0] <= last[0] + last[2] + max_gap:
                # Fusionner
                new_x = min(last[0], current[0])
                new_w = max(last[0] + last[2], current[0] + current[2]) - new_x
                new_y = min(last[1], current[1])
                new_h = max(last[1] + last[3], current[1] + current[3]) - new_y

                merged[-1] = (new_x, new_y, new_w, new_h)
            else:
                merged.append(current)

        return merged