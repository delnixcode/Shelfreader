"""
ShelfReader - OCR Processor (Phase 1)
Détection de titres de livres sur images de bibliothèques.
"""

import easyocr
import cv2
import numpy as np
from PIL import Image
import math
import pytesseract

class BookOCR:
    """Processeur OCR pour détecter les titres de livres."""

    def __init__(self, languages, confidence_threshold, use_gpu=False, use_tesseract=False):
        """Initialise l'OCR avec langue, seuil de confiance et option GPU."""
        self.use_tesseract = use_tesseract
        self.confidence_threshold = confidence_threshold

        if use_tesseract:
            # Utiliser Tesseract avec configs spéciales pour texte vertical
            self.tesseract_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .:()-'
            print(f"🔍 OCR initialisé - Tesseract, Seuil: {confidence_threshold}")
        else:
            # Utiliser EasyOCR
            self.reader = easyocr.Reader(languages, gpu=use_gpu)
            device = "GPU" if use_gpu else "CPU"
            print(f"🔍 OCR initialisé - EasyOCR, Langues: {languages}, Seuil: {confidence_threshold}, Device: {device}")

    def _is_vertical_text(self, bbox):
        """Vérifie si un texte est vertical (rotation 90° ou 270°)."""
        # Calculer les dimensions de la bbox
        width = max([p[0] for p in bbox]) - min([p[0] for p in bbox])
        height = max([p[1] for p in bbox]) - min([p[1] for p in bbox])
        
        # Texte vertical : hauteur >> largeur
        return height > width * 1.5

    def _calculate_font_size(self, bbox):
        """Calcule la taille approximative de la police."""
        height = max([p[1] for p in bbox]) - min([p[1] for p in bbox])
        return height

    def _preprocess_image(self, image):
        """Améliore agressivement la qualité d'image pour une meilleure détection OCR."""
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

    def _tesseract_detect(self, pil_image):
        """Détection OCR avec Tesseract (meilleur pour textes longs)."""
        # Convertir PIL en array numpy
        image_array = np.array(pil_image)

        # Prétraitement pour Tesseract
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        # Améliorer le contraste
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)

        # Détection avec Tesseract
        try:
            data = pytesseract.image_to_data(enhanced, config=self.tesseract_config, output_type=pytesseract.Output.DICT)

            results = []
            n_boxes = len(data['text'])
            for i in range(n_boxes):
                text = data['text'][i].strip()
                confidence = int(data['conf'][i]) / 100.0

                if confidence > 0.1 and len(text) >= 2:
                    # Calculer bbox depuis les coordonnées Tesseract
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    bbox = [[x, y], [x+w, y], [x+w, y+h], [x, y+h]]

                    results.append([bbox, text, confidence])

            return results
        except Exception as e:
            print(f"⚠️ Erreur Tesseract: {e}")
            return []

    def get_text_and_confidence(self, pil_image, preprocess=True):
        """Extrait le texte et la confiance moyenne."""
        if self.use_tesseract:
            # Utiliser Tesseract
            results = self._tesseract_detect(pil_image)
            texts = [r[1] for r in results]
            confidences = [r[2] for r in results]
        else:
            # Utiliser EasyOCR
            image_array = np.array(pil_image)
            bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

            # Prétraitement si demandé
            if preprocess:
                bgr_image = self._preprocess_image(bgr_image)

            # Détection OCR
            results = self.reader.readtext(bgr_image, rotation_info=[0, 90, 180, 270])

            # Filtrage par confiance et longueur
            filtered_results = [
                r for r in results
                if r[2] >= self.confidence_threshold and len(r[1].strip()) >= 2
            ]

            texts = [r[1] for r in filtered_results]
            confidences = [r[2] for r in filtered_results]

        full_text = ' '.join(texts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return (full_text, avg_confidence)

    def get_boxes(self, pil_image, preprocess=False, vertical_only=False):
        """Extrait les boîtes de texte avec coordonnées."""
        if self.use_tesseract:
            # Utiliser Tesseract
            results = self._tesseract_detect(pil_image)
        else:
            # Utiliser EasyOCR
            image_array = np.array(pil_image)
            bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

            # Prétraitement pour améliorer la détection
            if preprocess:
                bgr_image = self._preprocess_image(bgr_image)

            # Détection OCR avec paramètres très optimisés pour texte vertical
            results = self.reader.readtext(
                bgr_image,
                rotation_info=[0, 90, 180, 270],
                width_ths=0.3,      # Encore plus tolérant
                height_ths=0.3,     # Encore plus tolérant
                contrast_ths=0.05,  # Seuil de contraste très bas
                adjust_contrast=0.7, # Ajustement de contraste plus fort
                text_threshold=0.5, # Seuil de texte plus bas
                link_threshold=0.3  # Seuil de liaison plus bas
            )

        # Extraction des coordonnées (format unifié)
        boxes = []
        for r in results:
            if self.use_tesseract:
                bbox, text, confidence = r
            else:
                bbox, text, confidence = r[0], r[1], r[2]

            # Filtrage plus permissif
            if confidence < 0.1 or len(text.strip()) < 1:
                continue

            # Vérifier si vertical (optionnel)
            if vertical_only and not self._is_vertical_text(bbox):
                continue

            # Calculer coordonnées et taille de police
            x = min([p[0] for p in bbox])
            y = min([p[1] for p in bbox])
            width = max([p[0] for p in bbox]) - x
            height = max([p[1] for p in bbox]) - y
            font_size = self._calculate_font_size(bbox)

            boxes.append({
                "text": text,
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                "font_size": font_size,
                "is_vertical": self._is_vertical_text(bbox)
            })

        return boxes    # ============================================
    # MÉTHODE DE REGROUPEMENT - DÉTECTION DE LIVRES
    # ============================================

    def group_by_books(self, boxes, vertical_threshold=50):
        """Regroupe les textes par livre et reconstitue les titres."""
        if not boxes:
            return []
        
        # Filtrer: garder seulement les textes verticaux avec grandes polices
        vertical_boxes = [b for b in boxes if b.get('is_vertical', False)]
        
        if not vertical_boxes:
            return []
        
        # Calculer la médiane de la taille de police
        font_sizes = [b['font_size'] for b in vertical_boxes]
        median_font_size = sorted(font_sizes)[len(font_sizes) // 2]
        
        # Garder seulement les grandes polices (> 80% de la médiane)
        large_text_boxes = [b for b in vertical_boxes if b['font_size'] >= median_font_size * 0.8]
        
        # Trier par position X (gauche à droite)
        sorted_boxes = sorted(large_text_boxes, key=lambda b: b['x'])
        
        # Regrouper par colonnes (même livre)
        books = []
        current_book = [sorted_boxes[0]]
        current_x = sorted_boxes[0]['x']
        
        for box in sorted_boxes[1:]:
            if abs(box['x'] - current_x) <= vertical_threshold:
                current_book.append(box)
            else:
                books.append(current_book)
                current_book = [box]
                current_x = box['x']
        
        if current_book:
            books.append(current_book)
        
        # Extraire les titres
        formatted_books = []
        for book_texts in books:
            title = self._extract_book_title(book_texts)
            formatted_books.append({
                'title': title,
                'x': book_texts[0]['x'],
                'all_texts': [b['text'] for b in book_texts],
                'text_count': len(book_texts)
            })
        
        return formatted_books

    def _extract_book_title(self, book_texts):
        """Combine tous les textes détectés pour former un titre approximatif."""
        if not book_texts:
            return "Unknown"
        
        # Trier par position Y (du haut vers le bas du livre)
        sorted_texts = sorted(book_texts, key=lambda b: b['y'])
        
        # Combiner tous les textes
        all_texts = [b['text'].strip() for b in sorted_texts]
        combined = ' / '.join(all_texts)
        
        # Limiter la longueur
        if len(combined) > 60:
            combined = combined[:60] + '...'
        
        return combined

    def get_books(self, pil_image, preprocess=True):
        """Détecte les livres individuels (titres verticaux avec grandes polices)."""
        boxes = self.get_boxes(pil_image, preprocess=preprocess, vertical_only=False)
        books = self.group_by_books(boxes)
        return books

if __name__ == "__main__":
    """
    Point d'entrée pour les tests en ligne de commande.

    Permet de tester rapidement le processeur OCR sur une image
    en exécutant directement le fichier Python.

    Usage: python ocr_processor.py <chemin_image>
    """
    import sys
    import os

    # Vérification des arguments
    if len(sys.argv) != 2:
        print("Usage: python ocr_processor.py <image_path>")
        print("Example: python ocr_processor.py ../data/test_images/books.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    # Vérification que l'image existe
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        sys.exit(1)

    # === INITIALISATION ===
    # Créer une instance de BookOCR
    # - Langue: Anglais ['en']
    # - Seuil de confiance: 0.2 (permissif pour détecter plus de texte)
    processor = BookOCR(['en'], 0.2)

    # === CHARGEMENT DE L'IMAGE ===
    pil_image = Image.open(image_path)

    # === TRAITEMENT OCR ===
    print(f"🔍 Processing image: {image_path}")

    # Désactiver le préprocessing pour de meilleurs résultats
    text, confidence = processor.get_text_and_confidence(pil_image, preprocess=False)
    boxes = processor.get_boxes(pil_image, preprocess=False)
    books = processor.get_books(pil_image, preprocess=False)

    # === AFFICHAGE DES RÉSULTATS ===
    print("\n📊 === OCR Results ===")
    print(f"📝 Total text detected: {text[:100]}{'...' if len(text) > 100 else ''}")
    print(f"🎯 Confidence: {confidence:.3f}")
    print(f"� Number of text boxes: {len(boxes)}")
    print(f"📚 Number of books detected: {len(books)}")

    # Afficher les livres détectés
    if books:
        print("\n� Books detected:")
        for i, book in enumerate(books, 1):
            print(f"  {i:2d}. {book['title']}")
            if book['text_count'] > 1:
                print(f"      (+ {book['text_count']-1} other texts: {', '.join(book['all_texts'][:3])})")

    print("\n✅ Processing complete!")

