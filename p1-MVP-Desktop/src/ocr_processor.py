# ============================================
# Schéma d'interaction des méthodes BookOCR
# ============================================
"""
Diagramme d'interaction :

   [image_path ou PIL]
    │
    ▼
Image.open(image_path) si besoin
    │
    ▼
get_text_and_confidence(pil_image)
    │
    ├──► Texte brut + confiance moyenne
    │
    └──► Utilisé par get_boxes(pil_image)
           │
           ▼
      Extraction des coordonnées (bounding boxes)
           │
           ▼
      Liste des positions des textes détectés
"""
# ============================================
# TODO ShelfReader - OCR Processor (MVP Desktop)
# ============================================
# 1. Initialisation OCR ✅
#    - __init__ : EasyOCR, seuil de confiance
# 2. Prétraitement d'image ✅
#    - preprocess_image : niveaux de gris, égalisation
# 3. Extraction texte + confiance ✅
#    - get_text_and_confidence : OCR, filtrage, retour texte + confiance
# 4. Extraction des bounding boxes ✅
#    - get_boxes : coordonnées des textes détectés

import easyocr
import cv2
import numpy as np
from PIL import Image

class BookOCR:
    # TODO 1 🟧 : Initialisation OCR (EasyOCR, seuil de confiance)
    def __init__(self, languages, confidence_threshold):
        self.reader = easyocr.Reader(languages, gpu=False)
        self.confidence_threshold = confidence_threshold

    # TODO 2 🟧 : Prétraitement d'image (niveaux de gris, égalisation)
    def preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Améliorer le contraste pour les textes difficiles
        equalized = cv2.equalizeHist(gray)
        # Appliquer un filtre pour réduire le bruit
        blurred = cv2.GaussianBlur(equalized, (3, 3), 0)
        # Améliorer le contraste avec CLAHE pour les textes fins
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
        enhanced = clahe.apply(blurred)
        # Augmenter la netteté
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(enhanced, -1, kernel)
        # Redimensionner pour améliorer la détection de petits textes
        height, width = sharpened.shape
        if height < 1000:  # Si l'image est petite, l'agrandir
            scale_factor = 1000 / height
            new_width = int(width * scale_factor)
            sharpened = cv2.resize(sharpened, (new_width, 1000), interpolation=cv2.INTER_CUBIC)
        return sharpened

    # TODO 3 🟧 : Extraction texte + confiance (OCR, filtrage, retour texte + confiance)
    def get_text_and_confidence(self, pil_image, preprocess=True):
        """
        Retourne le texte extrait ET la confiance moyenne.
        """
        # Convertir PIL → NumPy array
        image_array = np.array(pil_image)
        # Convertir RGB → BGR pour OpenCV
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Prétraitement : si demandé, appliquer la transformation
        if preprocess:
            image = self.preprocess_image(bgr_image)
        else:
            image = bgr_image

        # Appel EasyOCR pour détecter le texte avec détection de rotation
        results = self.reader.readtext(image, rotation_info=[0, 90, 180, 270])

        # Filtrer les résultats par seuil de confiance et longueur minimale
        filtered_results = [r for r in results if r[2] >= self.confidence_threshold and len(r[1].strip()) >= 2]

        # Extraire tous les textes détectés
        texts = [r[1] for r in filtered_results]

        # Combiner tous les textes en une seule chaîne
        full_text = ' '.join(texts)

        # Calculer la confiance moyenne sur les résultats filtrés
        if filtered_results:
            avg_confidence = sum(r[2] for r in filtered_results) / len(filtered_results)
        else:
            avg_confidence = 0.0

        # Retourner le texte combiné et la confiance moyenne
        return (full_text, avg_confidence)

    # Pour obtenir texte + confiance depuis un chemin, utiliser :
    # pil_image = Image.open(image_path)
    # texte, confiance = self.get_text_and_confidence(pil_image)

    # TODO 4 🟧 : Extraction des bounding boxes (coordonnées des textes détectés)
    # Format : [{"text": ..., "x": ..., "y": ..., "width": ..., "height": ...}, ...]
    def get_boxes(self, pil_image, preprocess=True):
        # Convertir PIL → NumPy array
        image_array = np.array(pil_image)
        # Convertir RGB → BGR pour OpenCV
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Prétraitement : si demandé, appliquer la transformation
        if preprocess:
            image = self.preprocess_image(bgr_image)
        else:
            image = bgr_image

        # Appel EasyOCR pour détecter le texte avec détection de rotation
        results = self.reader.readtext(image, rotation_info=[0, 90, 180, 270])

        # Extraire les coordonnées (bounding boxes) des textes détectés (filtrés)
        boxes = []
        for r in results:
            text = r[1]
            confidence = r[2]
            # Filtrer par confiance et longueur
            if confidence >= self.confidence_threshold and len(text.strip()) >= 2:
                bbox = r[0]
                x = min([p[0] for p in bbox])
                y = min([p[1] for p in bbox])
                width = max([p[0] for p in bbox]) - x
                height = max([p[1] for p in bbox]) - y
                boxes.append({"text": text, "x": x, "y": y, "width": width, "height": height})

        # Retourner la liste des positions des textes détectés
        return boxes


if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) != 2:
        print("Usage: python ocr_processor.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        sys.exit(1)

    # Initialize OCR processor
    processor = BookOCR(['en'], 0.2)  # English, even lower confidence threshold to detect more text

    # Load image
    pil_image = Image.open(image_path)

    # Process the image
    print(f"Processing image: {image_path}")
    text, confidence = processor.get_text_and_confidence(pil_image, preprocess=False)  # Try without preprocessing
    boxes = processor.get_boxes(pil_image, preprocess=False)

    print("\n=== OCR Results ===")
    print(f"Text: {text}")
    print(f"Confidence: {confidence}")
    print(f"Number of text boxes: {len(boxes)}")

    if boxes:
        print("\nAll detected boxes:")
        for i, box in enumerate(boxes):
            print(f"Box {i+1}: {box}")

