# DÉPENDANCES:
#   - Utilise: detection/spine_detection.py, logic/config.py
#   - Importe: numpy
#   - Utilisé par: logic/orchestrator.py

"""
ShelfReader - EasyOCR Text Grouping
Module de regroupement intelligent des textes détectés.
"""

import numpy as np
from ..detection.spine_detection import EasyOCRSpineDetection
from ..logic.config import (
    MIN_SPINE_LINES_THRESHOLD, HORIZONTAL_GROUP_THRESHOLD_BASE,
    ADAPTIVE_THRESHOLD_MIN, ADAPTIVE_THRESHOLD_MAX,
    FONT_SIZE_RATIO_STRICT, FONT_SIZE_RATIO_TOLERANT,
    FONT_SIZE_STRICT_MULTIPLIER, FONT_SIZE_TOLERANT_MULTIPLIER
)


class EasyOCRTextGrouping:
    """Utilitaires de regroupement de textes pour EasyOCR."""

    @staticmethod
    def group_texts_by_spine_lines(boxes, image, debug=False, method="iccc2013"):
        """Regroupe les textes par lignes de tranches détectées ou par proximité intelligente."""
        if not boxes:
            return boxes

        # Détecter les lignes de séparation
        spine_lines = EasyOCRSpineDetection.detect_spine_lines(image, debug=debug, method=method)

        print(f"🔍 [{method}] Lignes de tranches détectées: {len(spine_lines) if spine_lines else 0}")

        # Seuil minimum: si trop peu de lignes détectées, utiliser le fallback adaptatif
        if not spine_lines or len(spine_lines) < MIN_SPINE_LINES_THRESHOLD:
            if spine_lines:
                print(f"⚠️ Seulement {len(spine_lines)} ligne(s) détectée(s) (min: {MIN_SPINE_LINES_THRESHOLD}), utilisation du regroupement adaptatif")
            else:
                print("⚠️ Aucune ligne de tranche détectée, utilisation du regroupement adaptatif")
            return EasyOCRTextGrouping.group_by_vertical_proximity(boxes, debug)

        # Pour shelfie: lignes verticales → trier par X et créer des blocs horizontaux
        # Pour ICCC: lignes horizontales → trier par Y et créer des blocs verticaux
        if method == "shelfie":
            # Trier les lignes par position X (horizontale)
            spine_lines.sort(key=lambda line: line.center[0])

            if debug:
                print(f"🔍 [Shelfie] Lignes de tranches triées par X: {[f'{line.center[0]:.0f}' for line in spine_lines]}")

            # Créer des blocs entre les lignes verticales
            blocks = [[] for _ in range(len(spine_lines) + 1)]

            for box in boxes:
                box_center_x = box['x'] + box['width'] / 2

                # Trouver dans quel bloc mettre cette boîte
                assigned = False
                for i in range(len(spine_lines) + 1):
                    if i == 0:
                        # Premier bloc : à gauche de la première ligne
                        if box_center_x < spine_lines[0].center[0]:
                            blocks[i].append(box)
                            assigned = True
                            break
                    elif i == len(spine_lines):
                        # Dernier bloc : à droite de la dernière ligne
                        if box_center_x >= spine_lines[-1].center[0]:
                            blocks[i].append(box)
                            assigned = True
                            break
                    else:
                        # Bloc entre deux lignes verticales
                        if spine_lines[i-1].center[0] <= box_center_x < spine_lines[i].center[0]:
                            blocks[i].append(box)
                            assigned = True
                            break

                if not assigned:
                    # Par défaut, mettre dans le dernier bloc
                    blocks[-1].append(box)

        else:  # ICCC2013
            # Trier les lignes par position Y (verticale)
            spine_lines.sort(key=lambda line: line.center[1])

            if debug:
                print(f"🔍 [ICCC] Lignes de tranches triées par Y: {[f'{line.center[1]:.0f}' for line in spine_lines]}")

            # Créer des blocs entre les lignes horizontales
            blocks = [[] for _ in range(len(spine_lines) + 1)]

            for box in boxes:
                box_center_y = box['y'] + box['height'] / 2

                # Trouver dans quel bloc mettre cette boîte
                assigned = False
                for i in range(len(spine_lines) + 1):
                    if i == 0:
                        # Premier bloc : au-dessus de la première ligne
                        if box_center_y < spine_lines[0].center[1]:
                            blocks[i].append(box)
                            assigned = True
                            break
                    elif i == len(spine_lines):
                        # Dernier bloc : en-dessous de la dernière ligne
                        if box_center_y >= spine_lines[-1].center[1]:
                            blocks[i].append(box)
                            assigned = True
                            break
                    else:
                        # Bloc entre deux lignes horizontales
                        if spine_lines[i-1].center[1] <= box_center_y < spine_lines[i].center[1]:
                            blocks[i].append(box)
                            assigned = True
                            break

                if not assigned:
                    # Par défaut, mettre dans le dernier bloc
                    blocks[-1].append(box)

        # Combiner les textes dans chaque bloc
        grouped_boxes = []
        for block in blocks:
            if not block:
                continue

            if len(block) == 1:
                grouped_boxes.append(block[0])
            else:
                # Trier par position horizontale
                block.sort(key=lambda b: b['x'])

                # Combiner les textes
                combined_text = ' '.join([b['text'] for b in block])

                # Calculer la boîte englobante
                min_x = min([b['x'] for b in block])
                max_x = max([b['x'] + b['width'] for b in block])
                min_y = min([b['y'] for b in block])
                max_y = max([b['y'] + b['height'] for b in block])

                # Confiance moyenne
                avg_confidence = sum([b['confidence'] for b in block]) / len(block)

                combined_box = {
                    "text": combined_text,
                    "x": min_x, "y": min_y,
                    "width": max_x - min_x,
                    "height": max_y - min_y,
                    "font_size": max([b['height'] for b in block]),
                    "is_vertical": any([b['is_vertical'] for b in block]),
                    "confidence": avg_confidence
                }

                grouped_boxes.append(combined_box)

        if debug:
            print(f"🔍 Regroupement par lignes: {len(spine_lines)} lignes détectées, {len(grouped_boxes)} groupes créés")
            for i, block in enumerate(blocks):
                if block:
                    print(f"  Bloc {i}: {len(block)} éléments")

        return grouped_boxes

    @staticmethod
    def group_by_proximity(boxes):
        """Regroupement par proximité horizontale (méthode de secours)."""
        if not boxes:
            return boxes

        # Trier par x croissant
        boxes.sort(key=lambda b: b['x'])

        grouped_boxes = []
        current_group = [boxes[0]]
        group_x_threshold = HORIZONTAL_GROUP_THRESHOLD_BASE

        for box in boxes[1:]:
            # Si la différence x est petite, ajouter au groupe
            if abs(box['x'] - current_group[-1]['x']) < group_x_threshold:
                current_group.append(box)
            else:
                # Nouveau groupe
                grouped_boxes.append(current_group)
                current_group = [box]

        # Ajouter le dernier groupe
        grouped_boxes.append(current_group)

        # Combiner les textes dans chaque groupe
        final_boxes = []
        for group in grouped_boxes:
            if len(group) == 1:
                final_boxes.append(group[0])
            else:
                # Trier par y et combiner
                group.sort(key=lambda b: b['y'])
                combined_text = ' '.join([b['text'] for b in group])
                combined_box = group[0].copy()
                combined_box['text'] = combined_text
                combined_box['width'] = max([b['x'] + b['width'] for b in group]) - min([b['x'] for b in group])
                combined_box['height'] = max([b['y'] + b['height'] for b in group]) - min([b['y'] for b in group])
                combined_box['confidence'] = sum([b['confidence'] for b in group]) / len(group)
                final_boxes.append(combined_box)

        return final_boxes

    @staticmethod
    def group_with_single_threshold(boxes, horizontal_threshold, debug=False):
        """Regroupe les boîtes avec un seuil donné."""
        if not boxes:
            return []

        boxes_sorted = sorted(boxes, key=lambda b: b['x'])
        grouped_books = []
        current_book = [boxes_sorted[0]]

        for box in boxes_sorted[1:]:
            last_box = current_book[-1]
            distance = box['x'] - (last_box['x'] + last_box['width'])

            # Adaptation font size: si police beaucoup plus grande, plus strict
            size_ratio = box['height'] / last_box['height'] if last_box['height'] > 0 else 1.0
            effective_threshold = horizontal_threshold

            if size_ratio > FONT_SIZE_RATIO_STRICT:
                effective_threshold *= FONT_SIZE_STRICT_MULTIPLIER
            elif size_ratio < FONT_SIZE_RATIO_TOLERANT:
                effective_threshold *= FONT_SIZE_TOLERANT_MULTIPLIER

            if distance < effective_threshold:
                current_book.append(box)
            else:
                grouped_books.append(current_book)
                current_book = [box]

        grouped_books.append(current_book)
        return grouped_books

    @staticmethod
    def calculate_adaptive_threshold(boxes, debug=False):
        """Calcule un seuil adaptatif basé sur l'analyse des distances entre boîtes."""
        if len(boxes) < 2:
            return 20  # Fallback

        # Trier par x
        sorted_boxes = sorted(boxes, key=lambda b: b['x'])

        # Calculer tous les gaps entre boîtes consécutives
        gaps = []
        for i in range(len(sorted_boxes) - 1):
            current_end = sorted_boxes[i]['x'] + sorted_boxes[i]['width']
            next_start = sorted_boxes[i+1]['x']
            gap = next_start - current_end
            if gap > 0:  # Ignorer les overlaps
                gaps.append(gap)

        if not gaps:
            return 20

        # Analyse statistique
        gaps_array = np.array(gaps)
        median_gap = np.median(gaps_array)
        std_gap = np.std(gaps_array)
        q25 = np.percentile(gaps_array, 25)

        # Seuil adaptatif: entre Q1 et médiane
        adaptive_threshold = (q25 + median_gap) / 2

        # Limiter entre les valeurs min/max
        adaptive_threshold = max(ADAPTIVE_THRESHOLD_MIN, min(ADAPTIVE_THRESHOLD_MAX, adaptive_threshold))

        if debug:
            print(f"📊 Analyse adaptative:")
            print(f"   Gaps: Q25={q25:.1f}, médiane={median_gap:.1f}, std={std_gap:.1f}px")
            print(f"   Seuil adaptatif calculé: {adaptive_threshold:.1f}px")

        return adaptive_threshold

    @staticmethod
    def group_by_vertical_proximity(boxes, debug=False):
        """Regroupement ADAPTATIF par proximité horizontale avec multi-scale detection."""
        if not boxes:
            return boxes

        # Trier par position horizontale (gauche à droite)
        boxes.sort(key=lambda b: b['x'])

        # Calcul du seuil adaptatif
        adaptive_threshold = EasyOCRTextGrouping.calculate_adaptive_threshold(boxes, debug=debug)

        # Multi-scale detection: essayer plusieurs seuils
        thresholds_to_try = [
            adaptive_threshold * 0.6,  # Plus strict
            adaptive_threshold,         # Standard
            adaptive_threshold * 1.4    # Plus tolérant
        ]

        all_results = []
        for threshold in thresholds_to_try:
            grouped_books = EasyOCRTextGrouping.group_with_single_threshold(boxes, threshold, debug=False)
            all_results.append((threshold, grouped_books))

        # Afficher les résultats multi-scale
        print(f"🔍 Multi-scale detection:")
        for thresh, result in all_results:
            print(f"   Seuil {thresh:.1f}px → {len(result)} livres")

        # Sélection du meilleur résultat
        valid_results = [(t, r) for t, r in all_results if len(r) <= 20]
        if not valid_results:
            valid_results = all_results

        best_threshold, grouped_books = max(valid_results, key=lambda x: len(x[1]))

        print(f"✅ Meilleur seuil sélectionné: {best_threshold:.1f}px → {len(grouped_books)} livres")

        # Fusion des groupes pour créer les boîtes finales
        final_boxes = []
        for book in grouped_books:
            if len(book) == 1:
                final_boxes.append(book[0])
            else:
                # Trier par position verticale
                book.sort(key=lambda b: b['y'])

                # Combiner les textes
                combined_text = ' '.join([b['text'] for b in book])

                # Calculer la boîte englobante
                min_x = min([b['x'] for b in book])
                max_x = max([b['x'] + b['width'] for b in book])
                min_y = min([b['y'] for b in book])
                max_y = max([b['y'] + b['height'] for b in book])

                # Confiance moyenne
                avg_confidence = sum([b['confidence'] for b in book]) / len(book)

                combined_box = {
                    "text": combined_text,
                    "x": min_x, "y": min_y,
                    "width": max_x - min_x,
                    "height": max_y - min_y,
                    "font_size": max([b['height'] for b in book]),
                    "is_vertical": any([b['is_vertical'] for b in book]),
                    "confidence": avg_confidence
                }

                final_boxes.append(combined_box)

        if debug:
            print(f"🔍 Regroupement horizontal: {len(final_boxes)} livres créés")
            for i, book in enumerate(grouped_books):
                print(f"  Livre {i+1}: {len(book)} éléments")

        return final_boxes