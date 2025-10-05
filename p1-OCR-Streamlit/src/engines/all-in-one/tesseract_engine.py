"""
ShelfReader - Tesseract OCR Processor
Module spécialisé pour la détection OCR avec Tesseract.
"""

# === IMPORTS ===
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

        # Configurations PSM optimisées (seulement les plus efficaces)
        self.psm_configs = [
            '--psm 6',  # Texte uniforme - le plus rapide et efficace
        ]

        print(f"🔍 Tesseract initialisé - Langues: {languages}, Seuil: {confidence_threshold}")

    # === PRÉTRAITEMENT ===
    def _preprocess_for_tesseract(self, image):
        """Prétraitement rapide et efficace pour Tesseract."""
        import cv2
        
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Améliorer le contraste avec CLAHE (simple et efficace)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)

        # Léger débruitage pour améliorer la qualité
        denoised = cv2.bilateralFilter(enhanced, 5, 50, 50)

        return [denoised]  # Retourner une seule image optimisée

    # === DÉTECTION OCR ===
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
        """Détecte le texte avec Tesseract de façon optimisée."""
        import numpy as np
        import cv2
        
        image_array = np.array(pil_image)
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Prétraitement rapide si demandé
        if preprocess:
            processed_images = self._preprocess_for_tesseract(bgr_image)
        else:
            processed_images = [cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)]

        # Utiliser seulement la meilleure configuration PSM
        all_results = []
        for processed_img in processed_images:
            results = self._detect_with_psm(processed_img, self.psm_configs[0])
            all_results.extend(results)

        # Trier par confiance et limiter les résultats
        all_results.sort(key=lambda x: x[2], reverse=True)
        return all_results[:15]  # Limiter à 15 meilleurs résultats

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
                "is_vertical": is_vertical,
                "confidence": confidence
            })

        return boxes

# === SCRIPT PRINCIPAL ===
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
    parser.add_argument('--output', type=str, help='Préfixe des fichiers de sortie (défaut: detected_book)')

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
        print(f"📝 Texte complet: {text}")

        # Sauvegarder dans un fichier unique qui se remplace
        output_file = args.output if args.output else 'result-ocr/tesseract_results.txt'
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