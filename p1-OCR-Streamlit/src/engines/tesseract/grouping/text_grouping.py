"""
ShelfReader - Tesseract Text Grouping
Module de regroupement simple pour Tesseract.
"""

class TesseractTextGrouping:
    """Regroupement simple pour Tesseract."""

    @staticmethod
    def group_texts_by_spine_lines(boxes, image, debug=False, method="simple"):
        """Tesseract utilise un regroupement simple."""
        if debug:
            print("🔍 Tesseract: regroupement simple par proximité")
        return TesseractTextGrouping.group_by_proximity(boxes)

    @staticmethod
    def group_by_proximity(boxes):
        """Regroupement simple par proximité horizontale."""
        if not boxes:
            return boxes

        # Trier par position horizontale
        boxes.sort(key=lambda b: b['x'])

        # Regrouper les boîtes proches
        grouped_boxes = []
        current_group = [boxes[0]]

        for box in boxes[1:]:
            # Distance entre les boîtes
            distance = box['x'] - (current_group[-1]['x'] + current_group[-1]['width'])

            if distance < 50:  # Seuil fixe de proximité
                current_group.append(box)
            else:
                grouped_boxes.append(current_group)
                current_group = [box]

        grouped_boxes.append(current_group)

        # Combiner les textes dans chaque groupe
        final_boxes = []
        for group in grouped_boxes:
            if len(group) == 1:
                final_boxes.append(group[0])
            else:
                # Combiner les textes
                combined_text = ' '.join([b['text'] for b in group])
                combined_box = group[0].copy()
                combined_box['text'] = combined_text
                combined_box['width'] = max([b['x'] + b['width'] for b in group]) - min([b['x'] for b in group])
                combined_box['height'] = max([b['y'] + b['height'] for b in group]) - min([b['y'] for b in group])
                combined_box['confidence'] = sum([b['confidence'] for b in group]) / len(group)
                final_boxes.append(combined_box)

        return final_boxes