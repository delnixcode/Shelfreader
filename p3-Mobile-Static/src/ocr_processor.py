# Rôle : Extraire le texte d'une image
# Technologies : EasyOCR (PyTorch en interne), OpenCV 
# Concepts : preprocessing d'image, confidence filtering

import easyocr
import cv2
import numpy as np
from PIL import Image

class BookOCR:
    # TODO 1 : Initialiser EasyOCR avec les langues et le seuil de confiance
    def __init__(self, languages, confidence_threshold):
        # Initialiser easyocr.Reader avec les langues
        self.reader = easyocr.Reader(languages, gpu=True)
        # Stocker le seuil de confiance
        self.confidence_threshold = confidence_threshold
        
      
    # Prétraitement d'image (niveaux de gris, égalisation)
    def preprocess_image(self, image):
        # Convertir en gris : cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Égaliser histogramme : cv2.equalizeHist(gray)
        equalized = cv2.equalizeHist(gray)
        # Retourner l'image traitée
        return equalized

    # TODO 2 : Compléter cette méthode pour extraire le texte d'une image PIL, avec prétraitement et filtrage par confiance. Retourner le texte et la confiance moyenne.
    def extract_text_from_pil(self, pil_image, preprocess=True):
        # Convertir PIL → NumPy array
        image_array = np.array(pil_image)
        # Convertir RGB → BGR pour OpenCV
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Prétraitement : si demandé, appliquer la transformation
        if preprocess:
            image = self.preprocess_image(bgr_image)
        else:
            image = bgr_image

        # Appel EasyOCR pour détecter le texte
        results = self.reader.readtext(image)

        # Filtrer les résultats par seuil de confiance
        filtered_results = []
        for r in results:
            if r[2] >= self.confidence_threshold:
                filtered_results.append(r)

        # Extraire tous les textes détectés
        texts = []
        for r in filtered_results:
            texte = r[1]
            texts.append(texte)

        # Combiner tous les textes en une seule chaîne
        full_text = ' '.join(texts)

        # Calculer la confiance moyenne sur les résultats filtrés
        if len(filtered_results) > 0:
            total = 0
            for r in filtered_results:
                total = total + r[2]
            avg_confidence = total / len(filtered_results)
        else:
            avg_confidence = 0.0

        # Retourner le texte combiné et la confiance moyenne
        return (full_text, avg_confidence)
    # TODO 3 : Créer une méthode pour filtrer et extraire uniquement les titres de livres à partir du texte OCR (ex : lignes longues, capitalisées, etc.). Retourner une liste de titres.
    # def extract_book_titles(self, pil_image):
    #     pass
    # TODO 4 : Créer une méthode pour retourner les coordonnées (bounding boxes) des textes détectés par OCR, sous forme de liste de dictionnaires.
    # Format : [{"text": ..., "x": ..., "y": ..., "width": ..., "height": ...}, ...]
    # def get_bounding_boxes(self, pil_image):
    #     pass

# 🧠 Mémoire du Projet ShelfReader

**Dernière mise à jour** : 2025-10-03

## 📊 État d'avancement

### Structure du projet
- `src/api_client.py` : Client Open Library (Phase 1) — Terminé
- `src/ocr_processor.py` : OCR EasyOCR (Phase 2) — En cours
- `src/app.py` : Interface Streamlit (Phase 3) — À faire
- `tests/` : Tests unitaires (Phase 4) — À faire

### TODOs principales
1. Installer Tesseract et EasyOCR ✔️
2. Implémenter extract_text_from_pil ✔️
3. Ajouter extract_book_titles ⏳
4. Ajouter get_bounding_boxes ⏳
5. Tester BookOCR sur une image ⏳

### Documentation simplifiée
- Tous les fichiers `.md` sont à jour et résumés :
    - Phase 1 : API Client — Terminé
    - Phase 2 : OCR — Méthode d’extraction de texte OK, reste titres et bounding boxes
    - Phase 3 : Interface — À faire
    - Phase 4 : Tests — À faire

### Conseils pour agents/futurs modèles
- Suivre la todo list du projet (voir ci-dessus)
- Se référer aux fichiers `.md` pour la structure et les exemples
- Mettre à jour ce fichier à chaque modification importante

### Prochaine étape
- Implémenter la méthode `extract_book_titles` dans `BookOCR`