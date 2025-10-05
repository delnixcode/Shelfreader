"""
ShelfReader - TrOCR Text Grouping
Regroupement du texte extrait par TrOCR.
"""

from typing import List, Dict, Any

class TrOCRTextGrouper:
    """Grouper de texte pour TrOCR."""

    def __init__(self, proximity_threshold: int = 50):
        """
        Initialise le grouper.

        Args:
            proximity_threshold: Seuil de proximité pour le regroupement
        """
        self.proximity_threshold = proximity_threshold

    def group_text_lines(self, text_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Regroupe les résultats de texte en lignes logiques.

        Args:
            text_results: Liste des résultats de texte avec positions

        Returns:
            Liste des lignes groupées
        """
        if not text_results:
            return []

        # Pour TrOCR, les résultats sont déjà dans l'ordre des bandes
        # Nous les regroupons simplement par proximité verticale

        sorted_results = sorted(text_results, key=lambda x: x.get('bbox', [0, 0, 0, 0])[1])

        grouped_lines = []
        current_group = []

        for result in sorted_results:
            if not current_group:
                current_group.append(result)
                continue

            # Vérifier la proximité verticale
            last_bbox = current_group[-1].get('bbox', [0, 0, 0, 0])
            current_bbox = result.get('bbox', [0, 0, 0, 0])

            # Distance verticale entre les boîtes
            vertical_distance = abs(current_bbox[1] - (last_bbox[1] + last_bbox[3]))

            if vertical_distance <= self.proximity_threshold:
                current_group.append(result)
            else:
                # Créer une nouvelle ligne
                grouped_lines.append(self._merge_group_to_line(current_group))
                current_group = [result]

        # Ajouter le dernier groupe
        if current_group:
            grouped_lines.append(self._merge_group_to_line(current_group))

        return grouped_lines

    def _merge_group_to_line(self, group: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Fusionne un groupe de résultats en une seule ligne.

        Args:
            group: Groupe de résultats à fusionner

        Returns:
            Ligne fusionnée
        """
        if not group:
            return {}

        if len(group) == 1:
            return group[0]

        # Combiner le texte
        combined_text = ' '.join([result.get('text', '') for result in group if result.get('text', '').strip()])

        # Calculer la boîte englobante combinée
        bboxes = [result.get('bbox', [0, 0, 0, 0]) for result in group]
        min_x = min(bbox[0] for bbox in bboxes)
        min_y = min(bbox[1] for bbox in bboxes)
        max_x = max(bbox[0] + bbox[2] for bbox in bboxes)
        max_y = max(bbox[1] + bbox[3] for bbox in bboxes)

        combined_bbox = [min_x, min_y, max_x - min_x, max_y - min_y]

        # Calculer la confiance moyenne
        confidences = [result.get('confidence', 0) for result in group]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        return {
            'text': combined_text.strip(),
            'bbox': combined_bbox,
            'confidence': avg_confidence,
            'source': 'trocr'
        }

    def filter_low_confidence(self, lines: List[Dict[str, Any]], min_confidence: float = 0.5) -> List[Dict[str, Any]]:
        """
        Filtre les lignes avec une faible confiance.

        Args:
            lines: Lignes à filtrer
            min_confidence: Confiance minimale requise

        Returns:
            Lignes filtrées
        """
        return [line for line in lines if line.get('confidence', 0) >= min_confidence]