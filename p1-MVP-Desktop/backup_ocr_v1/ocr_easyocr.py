"""
ShelfReader - EasyOCR Processor
Module spécialisé pour la détection OCR avec EasyOCR.
"""

# === IMPORTS ===
class EasyOCRProcessor:
    """Processeur OCR spécialisé pour EasyOCR."""

    def __init__(self, languages, confidence_threshold, use_gpu=False):
        """Initialise EasyOCR."""
        try:
            import easyocr
            import cv2
            import numpy as np
            from PIL import Image
        except ImportError as e:
            raise ImportError(f"EasyOCR nécessite des dépendances manquantes: {e}")

        self.confidence_threshold = confidence_threshold
        self.reader = easyocr.Reader(languages, gpu=use_gpu)
        device = "GPU" if use_gpu else "CPU"
        print(f"🔍 EasyOCR initialisé - Langues: {languages}, Seuil: {confidence_threshold}, Device: {device}")

    # === PRÉTRAITEMENT ===
    def _preprocess_image(self, image):
        """Prétraitement agressivement optimisé pour EasyOCR."""
        import cv2
        
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Améliorer drastiquement le contraste avec CLAHE
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(6,6))
        enhanced = clahe.apply(gray)

        # Réduction du bruit avec filtre bilatéral (préserve les bords)
        denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)

        # Améliorer la netteté avec unsharp masking
        gaussian = cv2.GaussianBlur(denoised, (0, 0), 1.0)
        sharpened = cv2.addWeighted(denoised, 1.5, gaussian, -0.5, 0)

        # Binarisation adaptative plus agressive
        binary = cv2.adaptiveThreshold(
            sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 3
        )

        # Dilatation légère pour connecter les caractères
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        dilated = cv2.dilate(binary, kernel, iterations=1)

        # Reconvertir en BGR pour EasyOCR
        processed = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)

        return processed

    # === DÉTECTION OCR ===
    def detect_text(self, pil_image, preprocess=True):
        """Détecte le texte avec EasyOCR."""
        import numpy as np
        import cv2
        
        image_array = np.array(pil_image)
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Prétraitement si demandé
        if preprocess:
            bgr_image = self._preprocess_image(bgr_image)

        # Détection OCR avec paramètres optimisés pour texte vertical
        results = self.reader.readtext(
            bgr_image,
            rotation_info=[0, 90, 180, 270],
            width_ths=0.3,      # Tolérance largeur
            height_ths=0.3,     # Tolérance hauteur
            contrast_ths=0.05,  # Seuil contraste très bas
            adjust_contrast=0.7, # Ajustement contraste
            text_threshold=0.5, # Seuil texte
            link_threshold=0.3  # Seuil liaison
        )

        # Filtrage par confiance et longueur
        filtered_results = [
            r for r in results
            if r[2] >= self.confidence_threshold and len(r[1].strip()) >= 2
        ]

        return filtered_results

    # === INTERFACES PUBLIQUES ===
    def get_text_and_confidence(self, pil_image, preprocess=True):
        """Extrait le texte et la confiance moyenne."""
        boxes = self.get_boxes(pil_image, preprocess=preprocess)

        texts = [b['text'] for b in boxes]
        confidences = [b['confidence'] for b in boxes]

        full_text = ' | '.join(texts)  # Séparer par | pour les livres
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return full_text, avg_confidence

    def get_boxes(self, pil_image, preprocess=True, vertical_only=False):
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

        # Grouper les boîtes par position horizontale (même livre)
        if boxes:
            # Trier par x croissant
            boxes.sort(key=lambda b: b['x'])

            grouped_boxes = []
            current_group = [boxes[0]]
            group_x_threshold = 50  # pixels de tolérance horizontale

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

            # Pour chaque groupe, trier par y et combiner les textes
            final_boxes = []
            for group in grouped_boxes:
                if len(group) == 1:
                    final_boxes.append(group[0])
                else:
                    # Trier le groupe par y croissant (haut en bas)
                    group.sort(key=lambda b: b['y'])
                    combined_text = ' '.join([b['text'] for b in group])
                    # Utiliser la première boîte comme base
                    combined_box = group[0].copy()
                    combined_box['text'] = combined_text
                    combined_box['width'] = max([b['x'] + b['width'] for b in group]) - min([b['x'] for b in group])
                    combined_box['height'] = max([b['y'] + b['height'] for b in group]) - min([b['y'] for b in group])
                    # Confiance moyenne
                    combined_box['confidence'] = sum([b['confidence'] for b in group]) / len(group)
                    final_boxes.append(combined_box)

            boxes = final_boxes

        return boxes

# === SCRIPT PRINCIPAL ===
if __name__ == "__main__":
    """
    Point d'entrée pour tester EasyOCR directement.
    Usage: python ocr_easyocr.py <image_path> [--gpu]
    """
    import sys
    import argparse
    from PIL import Image

    parser = argparse.ArgumentParser(description='Test EasyOCR directement')
    parser.add_argument('image_path', help='Chemin vers l\'image à analyser')
    parser.add_argument('--gpu', action='store_true', help='Utiliser le GPU')
    parser.add_argument('--confidence', type=float, default=0.2, help='Seuil de confiance (défaut: 0.2)')
    parser.add_argument('--output', type=str, help='Préfixe des fichiers de sortie (défaut: detected_book)')

    args = parser.parse_args()

    try:
        # Initialisation
        processor = EasyOCRProcessor(['en'], args.confidence, args.gpu)

        # Chargement de l'image
        pil_image = Image.open(args.image_path)

        # Traitement
        text, confidence = processor.get_text_and_confidence(pil_image, preprocess=False)
        boxes = processor.get_boxes(pil_image, preprocess=False)

        # Résultats
        print(f"🔍 EasyOCR - Image: {args.image_path}")
        print(f"📊 Résultats: {len(boxes)} textes détectés")
        print(f"🎯 Confiance moyenne: {confidence:.3f}")
        print(f"📝 Texte complet: {text}")

        # Sauvegarder dans un fichier unique qui se remplace
        output_file = args.output if args.output else 'result-ocr/easyocr_results.txt'
        if not output_file.startswith('result-ocr/'):
            output_file = f'result-ocr/{output_file}'
        
        # Créer le dossier s'il n'existe pas
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"=== RÉSULTATS OCR - {args.image_path} ===\n")
            f.write(f"Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Nombre de textes détectés: {len(boxes)}\n")
            f.write(f"Confiance moyenne: {confidence:.3f}\n\n")
            f.write(f"TEXTE COMPLET:\n{text}\n\n")
            
            if boxes:
                f.write("DÉTAIL PAR LIVRE:\n")
                for i, box in enumerate(boxes, 1):
                    f.write(f"\n--- Livre {i} ---\n")
                    f.write(f"Confiance: {box['confidence']:.3f}\n")
                    f.write(f"Texte: {box['text']}\n")
        
        print(f"💾 Résultats sauvegardés dans {output_file}")

        if boxes:
            print("\n📦 Textes détectés:")
            for i, box in enumerate(boxes, 1):
                print(f"  {i:2d}. {box['text']}")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)