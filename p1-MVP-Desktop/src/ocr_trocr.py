"""
ShelfReader - TrOCR Processor
Module spécialisé pour la détection OCR avec TrOCR (Transformer-based OCR).
"""

import cv2
import numpy as np
from PIL import Image
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

class TrOCRProcessor:
    """Processeur OCR spécialisé pour TrOCR."""

    def __init__(self, languages, confidence_threshold, use_gpu=False):
        """Initialise TrOCR."""
        try:
            import cv2
            import numpy as np
            from PIL import Image
            import torch
            from transformers import TrOCRProcessor, VisionEncoderDecoderModel
        except ImportError as e:
            raise ImportError(f"TrOCR nécessite des dépendances manquantes: {e}")

        self.confidence_threshold = confidence_threshold
        self.languages = languages
        self.use_gpu = use_gpu

        # Détection automatique du device
        self.device = torch.device("cuda" if use_gpu and torch.cuda.is_available() else "cpu")

        # Chargement du modèle TrOCR
        try:
            self.processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-printed', use_fast=True)
            self.model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-printed')
            self.model.to(self.device)
            self.model.eval()

            device_name = "GPU" if self.device.type == "cuda" else "CPU"
            print(f"🔍 TrOCR initialisé - Langues: {languages}, Seuil: {confidence_threshold}, Device: {device_name}")

        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement de TrOCR: {e}")

    def _preprocess_image(self, image):
        """Prétraitement optimisé pour TrOCR."""
        import cv2
        
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Améliorer le contraste avec CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)

        # Réduction du bruit
        denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)

        # Améliorer la netteté
        gaussian = cv2.GaussianBlur(denoised, (0, 0), 1.0)
        sharpened = cv2.addWeighted(denoised, 1.5, gaussian, -0.5, 0)

        # Binarisation adaptative
        binary = cv2.adaptiveThreshold(
            sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Reconvertir en RGB pour TrOCR
        rgb = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)

        return rgb

    def _trocr_detect(self, pil_image):
        """Détection OCR avec TrOCR."""
        import numpy as np
        import cv2
        from PIL import Image
        
        # Prétraitement
        image_array = np.array(pil_image)
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        processed_image = self._preprocess_image(bgr_image)

        # Convertir en PIL Image
        pil_processed = Image.fromarray(processed_image)

        # Préparation pour TrOCR
        pixel_values = self.processor(pil_processed, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(self.device)

        # Génération avec beam search
        with torch.no_grad():
            generated_ids = self.model.generate(
                pixel_values,
                max_length=50,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=3,
                length_penalty=2.0,
                repetition_penalty=1.5
            )

        # Décodage du texte
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        # TrOCR ne fournit pas de confiance directement, on utilise une valeur fixe élevée
        # pour la compatibilité avec l'interface
        confidence = 0.95 if len(generated_text.strip()) > 0 else 0.0

        return generated_text.strip(), confidence

    def detect_text(self, pil_image, preprocess=True):
        """Détecte le texte avec TrOCR."""
        text, confidence = self._trocr_detect(pil_image)

        if confidence >= self.confidence_threshold and len(text) >= 2:
            # Créer une boîte fictive pour la compatibilité
            # TrOCR ne détecte pas les boîtes, seulement le texte complet
            width, height = pil_image.size
            bbox = [(0, 0), (width, 0), (width, height), (0, height)]
            return [(bbox, text, confidence)]

        return []

    def get_text_and_confidence(self, pil_image, preprocess=True):
        """Extrait le texte et la confiance."""
        text, confidence = self._trocr_detect(pil_image)

        if confidence >= self.confidence_threshold and len(text) >= 2:
            return text, confidence

        return "", 0.0

    def get_boxes(self, pil_image, preprocess=True, vertical_only=False):
        """Extrait les boîtes de texte avec coordonnées."""
        text, confidence = self._trocr_detect(pil_image)

        if confidence >= self.confidence_threshold and len(text) >= 2:
            width, height = pil_image.size
            font_size = height  # Estimation

            # Détection verticale basée sur les dimensions
            is_vertical = height > width

            if vertical_only and not is_vertical:
                return []

            return [{
                "text": text,
                "x": 0, "y": 0,
                "width": width, "height": height,
                "font_size": font_size,
                "is_vertical": is_vertical
            }]

        return []

if __name__ == "__main__":
    """
    Point d'entrée pour tester TrOCR directement.
    Usage: python ocr_trocr.py <image_path> [--gpu]
    """
    import sys
    import argparse
    from PIL import Image

    parser = argparse.ArgumentParser(description='Test TrOCR directement')
    parser.add_argument('image_path', help='Chemin vers l\'image à analyser')
    parser.add_argument('--gpu', action='store_true', help='Utiliser le GPU')
    parser.add_argument('--confidence', type=float, default=0.2, help='Seuil de confiance (défaut: 0.2)')

    args = parser.parse_args()

    try:
        # Initialisation
        processor = TrOCRProcessor(['en'], args.confidence, args.gpu)

        # Chargement de l'image
        pil_image = Image.open(args.image_path)

        # Traitement
        text, confidence = processor.get_text_and_confidence(pil_image, preprocess=True)
        boxes = processor.get_boxes(pil_image, preprocess=True)

        # Résultats
        print(f"🔍 TrOCR - Image: {args.image_path}")
        print(f"📊 Résultats: {len(boxes)} textes détectés")
        print(f"🎯 Confiance: {confidence:.3f}")
        print(f"📝 Texte: {text[:100]}{'...' if len(text) > 100 else ''}")

        if boxes:
            print("\n📦 Textes détectés:")
            for i, box in enumerate(boxes[:10], 1):  # Limiter à 10 premiers
                print(f"  {i:2d}. {box['text'][:50]}{'...' if len(box['text']) > 50 else ''}")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)