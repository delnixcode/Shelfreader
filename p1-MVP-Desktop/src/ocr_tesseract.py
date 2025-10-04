"""
ShelfReader - Tesseract OCR Processor
Module spécialisé pour la détection OCR avec Tesseract.
"""

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
        self.use_gpu = use_gpu  # Tesseract ne supporte pas vraiment GPU, mais gardé pour cohérence

        # Configurations PSM pour différents types de texte
        self.psm_configs = [
            '--psm 6',  # Texte uniforme
            '--psm 8',  # Mot unique
            '--psm 11', # Texte vertical
            '--psm 13'  # Texte brut
        ]

        print(f"🔍 Tesseract initialisé - Langues: {languages}, Seuil: {confidence_threshold}")

    def _preprocess_for_tesseract(self, image):
        """Prétraitement optimisé pour Tesseract avec variantes."""
        import cv2
        
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        processed_images = []

        # 1. Version originale avec CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        processed_images.append(enhanced)

        # 2. Version avec binarisation adaptative
        binary = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        processed_images.append(binary)

        # 3. Version avec réduction du bruit
        denoised = cv2.bilateralFilter(enhanced, 5, 50, 50)
        processed_images.append(denoised)

        # 4. Version avec amélioration du contraste
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # Approximation
        enhanced_lab_gray = clahe.apply(lab)
        processed_images.append(enhanced_lab_gray)

        # 5. Version avec morphologie mathématique
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        processed_images.append(morphed)
        
        # 6. Version avec seuillage Otsu
        _, otsu = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        processed_images.append(otsu)

        return processed_images

    def _detect_with_psm(self, image, psm_config):
        """Détection avec une configuration PSM spécifique."""
        import pytesseract
        from pytesseract import Output
        
        try:
            config = f'{psm_config} -l {self.languages}'
            data = pytesseract.image_to_data(image, config=config, output_type=Output.DICT)

            results = []
            n_boxes = len(data['text'])
            for i in range(n_boxes):
                confidence = int(data['conf'][i])
                text = data['text'][i].strip()

                if confidence > self.confidence_threshold and len(text) >= 2:
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    bbox = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
                    results.append((bbox, text, confidence / 100.0))

            return results
        except Exception as e:
            print(f"Erreur avec PSM {psm_config}: {e}")
            return []

    def detect_text(self, pil_image, preprocess=True):
        """Détecte le texte avec Tesseract en essayant plusieurs PSM."""
        import numpy as np
        import cv2
        
        image_array = np.array(pil_image)
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Prétraitement si demandé
        if preprocess:
            processed_images = self._preprocess_for_tesseract(bgr_image)
        else:
            processed_images = [cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)]

        # Essayer chaque configuration PSM et combiner les résultats
        all_results = []
        for psm_config in self.psm_configs:
            for processed_img in processed_images:
                results = self._detect_with_psm(processed_img, psm_config)
                all_results.extend(results)

        # Supprimer les doublons et trier par confiance
        unique_results = []
        seen_texts = set()
        for result in sorted(all_results, key=lambda x: x[2], reverse=True):
            text = result[1]
            if text not in seen_texts:
                unique_results.append(result)
                seen_texts.add(text)

        return unique_results[:20]  # Limiter à 20 meilleurs résultats

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

if __name__ == "__main__":
    """
    Point d'entrée pour tester Tesseract directement.
    Usage: python ocr_tesseract.py <image_path> [--gpu]
    """
    import sys
    import argparse
    from PIL import Image

    parser = argparse.ArgumentParser(description='Test Tesseract directement')
    parser.add_argument('image_path', help='Chemin vers l\'image à analyser')
    parser.add_argument('--gpu', action='store_true', help='Utiliser le GPU (si disponible)')
    parser.add_argument('--confidence', type=float, default=0.2, help='Seuil de confiance (défaut: 0.2)')
    parser.add_argument('--lang', default='eng', help='Langue pour Tesseract (défaut: eng)')

    args = parser.parse_args()

    try:
        # Initialisation
        processor = TesseractOCRProcessor(args.lang, args.confidence, args.gpu)

        # Chargement de l'image
        pil_image = Image.open(args.image_path)

        # Traitement
        text, confidence = processor.get_text_and_confidence(pil_image, preprocess=True)
        boxes = processor.get_boxes(pil_image, preprocess=True)

        # Résultats
        print(f"🔍 Tesseract - Image: {args.image_path}")
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