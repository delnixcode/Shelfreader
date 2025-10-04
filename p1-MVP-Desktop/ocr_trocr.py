"""
ShelfReader - TrOCR Processor
Module spécialisé pour la détection OCR avec TrOCR (Transformer-based OCR).
"""

# === IMPORTS ===
import cv2
import numpy as np
from PIL import Image
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

# === CLASSE PRINCIPALE ===
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
            self.processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten', use_fast=True)
            self.model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
            self.model.to(self.device)
            self.model.eval()

            device_name = "GPU" if self.device.type == "cuda" else "CPU"
            print(f"🔍 TrOCR initialisé - Langues: {languages}, Seuil: {confidence_threshold}, Device: {device_name}")

        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement de TrOCR: {e}")

    # === PRÉTRAITEMENT ===
    def _preprocess_image(self, image):
        """Prétraitement minimal pour TrOCR."""
        import cv2
        
        # Convertir en RGB
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        return rgb

    # === DÉTECTION OCR ===
    def _trocr_detect(self, pil_image):
        """Détection OCR avec TrOCR, segmentation en bandes pour plusieurs livres."""
        import numpy as np
        import cv2
        from PIL import Image
        
        # Prétraitement
        image_array = np.array(pil_image)
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        processed_image = self._preprocess_image(bgr_image)

        # Segmentation en bandes verticales (pour dos de livres)
        height, width = processed_image.shape[:2]
        num_strips = 14  # Nombre estimé de livres
        strip_width = width // num_strips

        results = []
        for i in range(num_strips):
            left = i * strip_width
            right = (i + 1) * strip_width if i < num_strips - 1 else width
            strip = processed_image[:, left:right]

            # Convertir en PIL Image
            strip_pil = Image.fromarray(strip)

            # Préparation pour TrOCR
            pixel_values = self.processor(strip_pil, return_tensors="pt").pixel_values
            pixel_values = pixel_values.to(self.device)

            # Génération avec beam search
            with torch.no_grad():
                outputs = self.model.generate(
                    pixel_values,
                    max_length=100,
                    num_beams=6,
                    early_stopping=True,
                    no_repeat_ngram_size=2,
                    length_penalty=1.5,
                    repetition_penalty=1.2,
                    return_dict_in_generate=True,
                    output_scores=True
                )

            # Décodage du texte
            generated_text = self.processor.batch_decode(outputs.sequences, skip_special_tokens=True)[0].strip()

            # Calcul de la confiance
            scores = outputs.scores
            if scores:
                log_probs = []
                for score in scores[1:]:
                    probs = torch.softmax(score, dim=-1)
                    max_prob = torch.max(probs, dim=-1).values.max().item()
                    log_probs.append(np.log(max_prob) if max_prob > 0 else -float('inf'))
                confidence = np.exp(np.mean(log_probs)) if log_probs else 0.0
            else:
                confidence = 0.0

            if len(generated_text) >= 2 and confidence >= 0.1:  # Seuil bas pour inclure
                results.append((generated_text, confidence))

        # Retourner les résultats individuels
        return results if results else [("", 0.0)]

    # === INTERFACES PUBLIQUES ===
    def detect_text(self, pil_image, preprocess=True):
        """Détecte le texte avec TrOCR."""
        results = self._trocr_detect(pil_image)

        filtered_results = []
        for text, confidence in results:
            if confidence >= self.confidence_threshold and len(text) >= 2:
                # Créer une boîte fictive pour la compatibilité
                width, height = pil_image.size
                bbox = [(0, 0), (width, 0), (width, height), (0, height)]
                filtered_results.append((bbox, text, confidence))

        return filtered_results

    def get_text_and_confidence(self, pil_image, preprocess=True):
        """Extrait le texte et la confiance."""
        results = self._trocr_detect(pil_image)

        if results and any(conf >= self.confidence_threshold and len(text) >= 2 for text, conf in results):
            texts = [text for text, conf in results if conf >= self.confidence_threshold and len(text) >= 2]
            confidences = [conf for text, conf in results if conf >= self.confidence_threshold and len(text) >= 2]
            combined_text = ' | '.join(texts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            return combined_text, avg_confidence

        return "", 0.0

    def get_boxes(self, pil_image, preprocess=True, vertical_only=False):
        """Extrait les boîtes de texte avec coordonnées."""
        results = self._trocr_detect(pil_image)

        boxes = []
        width, height = pil_image.size
        strip_width = width // len(results) if results else width

        for i, (text, confidence) in enumerate(results):
            if confidence >= self.confidence_threshold and len(text) >= 2:
                # Créer une boîte pour chaque strip
                x = i * strip_width
                y = 0
                boxes.append({
                    "text": text,
                    "x": x, "y": y,
                    "width": strip_width, "height": height,
                    "font_size": height * 0.8,
                    "is_vertical": True,  # Assume vertical for book spines
                    "confidence": confidence
                })

        return boxes

# === SCRIPT PRINCIPAL ===
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
    parser.add_argument('--output', type=str, help='Préfixe des fichiers de sortie (défaut: detected_book)')

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
        print(f"📝 Texte complet: {text}")

        # Sauvegarder dans un fichier unique qui se remplace
        output_file = args.output if args.output else 'result-ocr/trocr_results.txt'
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