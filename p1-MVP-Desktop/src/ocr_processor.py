# ============================================
# ShelfReader - OCR Processor (Phase 1 - MVP Desktop)
# ============================================
"""
Module de traitement OCR pour la détection de titres de livres.

Ce module utilise EasyOCR pour détecter automatiquement les textes
sur les images de bibliothèques et extraire les titres de livres.

Fonctionnalités principales:
- Détection OCR multi-langues (actuellement anglais)
- Prétraitement d'image optionnel (désactivé pour meilleurs résultats)
- Filtrage par seuil de confiance
- Extraction des coordonnées des textes détectés

Auteur: ShelfReader Team
Date: 2025
"""

# ============================================
# IMPORTS ET DÉPENDANCES
# ============================================

import easyocr          # Bibliothèque OCR principale
import cv2              # Traitement d'images OpenCV
import numpy as np      # Calculs numériques
from PIL import Image    # Manipulation d'images PIL/Pillow

# ============================================
# CLASSE PRINCIPALE - BookOCR
# ============================================

class BookOCR:
    """
    Classe principale pour le traitement OCR des images de livres.

    Cette classe encapsule toute la logique de détection de texte
    sur les images de bibliothèques, avec support pour le prétraitement
    et le filtrage des résultats.

    Attributs:
        reader (easyocr.Reader): Instance du lecteur OCR
        confidence_threshold (float): Seuil de confiance (0.0-1.0)
    """

    def __init__(self, languages, confidence_threshold):
        """
        Initialise le processeur OCR.

        Args:
            languages (list): Liste des langues à détecter (ex: ['en', 'fr'])
            confidence_threshold (float): Seuil minimum de confiance (0.0-1.0)
                                         Les textes avec une confiance inférieure
                                         seront filtrés
        """
        # Créer l'instance EasyOCR
        # gpu=False pour utiliser le CPU (plus lent mais compatible partout)
        self.reader = easyocr.Reader(languages, gpu=False)

        # Stocker le seuil de confiance pour le filtrage
        self.confidence_threshold = confidence_threshold

        print(f"🔍 OCR initialisé - Langues: {languages}, Seuil: {confidence_threshold}")

    def preprocess_image(self, image):
        """
        Applique un prétraitement à l'image pour améliorer la détection OCR.

        NOTE: Cette méthode est actuellement conservée mais DÉSACTIVÉE
        par défaut car elle dégradait la qualité de détection sur les
        images de bibliothèques naturelles.

        Args:
            image (numpy.ndarray): Image OpenCV (format BGR)

        Returns:
            numpy.ndarray: Image prétraitée en niveaux de gris
        """
        # Conversion en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Égalisation d'histogramme pour améliorer le contraste
        # (utile pour les textes peu contrastés)
        equalized = cv2.equalizeHist(gray)

        # Réduction du bruit avec un flou gaussien léger
        blurred = cv2.GaussianBlur(equalized, (3, 3), 0)

        # Amélioration du contraste avec CLAHE (Contrast Limited Adaptive Histogram Equalization)
        # clipLimit=4.0 : limite le contraste pour éviter les artefacts
        # tileGridSize=(8,8) : taille des tuiles pour l'adaptation locale
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
        enhanced = clahe.apply(blurred)

        # Augmentation de la netteté avec un filtre de convolution
        # Noyau de netteté : accentue les contours
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(enhanced, -1, kernel)

        # Redimensionnement si l'image est petite (< 1000px de hauteur)
        # Utile pour améliorer la détection de petits textes
        height, width = sharpened.shape
        if height < 1000:
            scale_factor = 1000 / height
            new_width = int(width * scale_factor)
            sharpened = cv2.resize(sharpened, (new_width, 1000), interpolation=cv2.INTER_CUBIC)

        return sharpened

    # ============================================
    # MÉTHODES PRINCIPALES - EXTRACTION DE TEXTE
    # ============================================

    def get_text_and_confidence(self, pil_image, preprocess=True):
        """
        Extrait le texte d'une image et retourne la confiance moyenne.

        Cette méthode est le cœur du système OCR. Elle prend une image PIL,
        applique optionnellement un prétraitement, détecte le texte avec
        EasyOCR, filtre les résultats et retourne le texte combiné avec
        la confiance moyenne.

        Args:
            pil_image (PIL.Image): Image PIL (format RGB)
            preprocess (bool): Si True, applique le prétraitement d'image
                              (désactivé par défaut pour meilleurs résultats)

        Returns:
            tuple: (texte_combine, confiance_moyenne)
                   - texte_combine (str): Tous les textes détectés concaténés
                   - confiance_moyenne (float): Moyenne des confiances (0.0-1.0)
        """
        # Conversion PIL → NumPy array
        # PIL utilise le format RGB, OpenCV utilise BGR
        image_array = np.array(pil_image)

        # Conversion RGB → BGR pour OpenCV
        # OpenCV attend le format BGR par défaut
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Application du prétraitement si demandé
        if preprocess:
            image = self.preprocess_image(bgr_image)
        else:
            # Utilisation directe de l'image originale (recommandé)
            image = bgr_image

        # === DÉTECTION OCR AVEC EASYOCR ===
        # rotation_info : Liste des angles de rotation à tester
        # [0, 90, 180, 270] = texte horizontal et vertical
        results = self.reader.readtext(image, rotation_info=[0, 90, 180, 270])

        # === FILTRAGE DES RÉSULTATS ===
        # Chaque résultat EasyOCR est un tuple: (bounding_box, text, confidence)
        # On filtre par:
        # 1. Seuil de confiance minimum
        # 2. Longueur minimale du texte (évite les faux positifs)
        filtered_results = [
            r for r in results
            if r[2] >= self.confidence_threshold and len(r[1].strip()) >= 2
        ]

        # Extraction de tous les textes détectés (après filtrage)
        texts = [r[1] for r in filtered_results]

        # Concaténation de tous les textes en une seule chaîne
        # Séparés par des espaces pour la lisibilité
        full_text = ' '.join(texts)

        # Calcul de la confiance moyenne
        if filtered_results:
            # Somme des confiances divisée par le nombre de résultats
            avg_confidence = sum(r[2] for r in filtered_results) / len(filtered_results)
        else:
            # Aucun résultat détecté
            avg_confidence = 0.0

        # Retour du texte combiné et de la confiance moyenne
        return (full_text, avg_confidence)

    def get_boxes(self, pil_image, preprocess=True):
        """
        Extrait les coordonnées (bounding boxes) des textes détectés.

        Cette méthode retourne une liste détaillée de tous les textes détectés
        avec leurs positions dans l'image. Utile pour visualiser ou traiter
        individuellement chaque texte trouvé.

        Args:
            pil_image (PIL.Image): Image PIL (format RGB)
            preprocess (bool): Si True, applique le prétraitement d'image

        Returns:
            list: Liste de dictionnaires avec les clés:
                  - 'text': Le texte détecté (str)
                  - 'x': Position X du coin supérieur gauche (float)
                  - 'y': Position Y du coin supérieur gauche (float)
                  - 'width': Largeur de la boîte (float)
                  - 'height': Hauteur de la boîte (float)
        """
        # Conversion PIL → NumPy array (même processus que get_text_and_confidence)
        image_array = np.array(pil_image)
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Application du prétraitement si demandé
        if preprocess:
            image = self.preprocess_image(bgr_image)
        else:
            image = bgr_image

        # Détection OCR avec EasyOCR (mêmes paramètres)
        results = self.reader.readtext(image, rotation_info=[0, 90, 180, 270])

        # === EXTRACTION DES COORDONNÉES ===
        boxes = []
        for r in results:
            text = r[1]          # Le texte détecté
            confidence = r[2]    # La confiance (0.0-1.0)
            bbox = r[0]          # Liste des 4 coins de la boîte: [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]

            # Appliquer les mêmes filtres que dans get_text_and_confidence
            if confidence >= self.confidence_threshold and len(text.strip()) >= 2:
                # Calcul des coordonnées de la boîte englobante
                # x = coordonnée X minimale (coin gauche)
                # y = coordonnée Y minimale (coin supérieur)
                # width = largeur = Xmax - Xmin
                # height = hauteur = Ymax - Ymin
                x = min([p[0] for p in bbox])
                y = min([p[1] for p in bbox])
                width = max([p[0] for p in bbox]) - x
                height = max([p[1] for p in bbox]) - y

                # Ajouter à la liste des résultats
                boxes.append({
                    "text": text,
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height
                })

        # Retourner la liste complète des boîtes détectées
        return boxes


# ============================================
# SECTION PRINCIPALE - TESTS ET DÉMONSTRATION
# ============================================

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

    # === AFFICHAGE DES RÉSULTATS ===
    print("\n📊 === OCR Results ===")
    print(f"📝 Text: {text}")
    print(f"🎯 Confidence: {confidence:.3f}")
    print(f"📚 Number of text boxes: {len(boxes)}")

    # Afficher le détail de chaque boîte détectée
    if boxes:
        print("\n📍 All detected boxes:")
        for i, box in enumerate(boxes):
            print(f"  Box {i+1}: {box}")

    print("\n✅ Processing complete!")

