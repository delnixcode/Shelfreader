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
        results = self.detect_text(pil_image, preprocess=preprocess)

        texts = [r[1] for r in results]
        confidences = [r[2] for r in results]

        full_text = ' '.join(texts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return full_text, avg_confidence

    def get_boxes(self, pil_image, preprocess=True, vertical_only=False):
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
                "is_vertical": is_vertical
            })

        return boxes

# === SCRIPT PRINCIPAL ===
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
        print(f"📝 Texte: {text[:100]}{'...' if len(text) > 100 else ''}")

        if boxes:
            print("\n📦 Textes détectés:")
            for i, box in enumerate(boxes[:10], 1):  # Limiter à 10 premiers
                print(f"  {i:2d}. {box['text'][:50]}{'...' if len(box['text']) > 50 else ''}")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)