# 🔍 **OCR Code Explanation - ShelfReader P1**
## Comprendre et recréer le système OCR de détection de livres

*Ce document explique en détail le code OCR de ShelfReader P1, vous permettant de comprendre chaque concept et de recréer le système de zéro.*

---

## 📋 **Table des matières**
1. [Architecture générale](#architecture-générale)
2. [Concepts OCR fondamentaux](#concepts-ocr-fondamentaux)
3. [Architecture modulaire OCR](#architecture-modulaire-ocr)
4. [Module EasyOCR](#module-easyocr)
5. [Module Tesseract](#module-tesseract)
6. [Module TrOCR](#module-trocr)
7. [Script de détection unifié](#script-de-détection-unifié)
8. [Prétraitement d'image](#prétraitement-dimage)
9. [Extraction des boîtes de texte](#extraction-des-boîtes-de-texte)
10. [Regroupement par livres](#regroupement-par-livres)
11. [Interactions entre modules](#interactions-entre-modules)
12. [Flux d'exécution détaillé](#flux-dexécution-détaillé)
13. [Comment utiliser le système](#comment-utiliser-le-système)

---

## 🏗️ **Architecture générale**

Le système OCR de ShelfReader P1 utilise une **architecture modulaire** composée de **quatre fichiers principaux** :

### Moteurs OCR individuels
- **`src/ocr_easyocr.py`** : Module EasyOCR avec GPU support
  - **Classe** : `EasyOCRProcessor`
  - **Spécialisation** : Détection précise avec rotations automatiques
- **`src/ocr_tesseract.py`** : Module Tesseract avec configurations PSM
  - **Classe** : `TesseractOCRProcessor`
  - **Spécialisation** : Performance et texte horizontal
- **`src/ocr_trocr.py`** : Module TrOCR avec transformers
  - **Classe** : `TrOCRProcessor`
  - **Spécialisation** : Modèle transformer avancé

### Script unifié
- **`scripts/ocr_detect.py`** : Interface en ligne de commande unifiée
- **Responsabilités** :
  - Parsing des arguments
  - Sélection du moteur OCR
  - Configuration du système
  - Affichage des résultats
  - Gestion des erreurs

### Flux de données :
```
Image → Sélection moteur → Prétraitement → Détection OCR → Boîtes de texte → Regroupement → Livres détectés
```

### Avantages de l'architecture modulaire :
1. **Indépendance** : Chaque moteur peut être testé et utilisé séparément
2. **Maintenance** : Modifications isolées par moteur
3. **Performance** : Choix du moteur optimal selon les besoins
4. **Évolutivité** : Ajout de nouveaux moteurs facile

---

## 🎯 **Concepts OCR fondamentaux**

### Qu'est-ce que l'OCR ?
L'**OCR (Optical Character Recognition)** est la technologie qui permet de **convertir des images de texte en texte numérique**.

### Défis spécifiques aux tranches de livres :
1. **Texte vertical** : Les titres sont écrits verticalement sur les tranches
2. **Petite taille** : Texte souvent petit et fin
3. **Contraste variable** : Qualité d'impression inégale
4. **Déformation** : Courbure des tranches de livres

### Moteurs OCR utilisés :

#### EasyOCR
- **Avantages** : Détection automatique des rotations, très précis, GPU support
- **Inconvénients** : Plus lent au chargement, nécessite PyTorch
- **Usage** : Texte complexe, rotations multiples, précision maximale

#### Tesseract
- **Avantages** : Rapide, léger, configurations PSM avancées
- **Inconvénients** : Moins bon avec les rotations complexes
- **Usage** : Texte simple, performance importante, CPU uniquement

#### TrOCR (Transformer OCR)
- **Avantages** : Modèle de deep learning avancé, excellente précision
- **Inconvénients** : Lent, nécessite beaucoup de ressources
- **Usage** : Haute précision requise, GPU recommandé

---

## 🏗️ **Architecture modulaire OCR**

Le système utilise une architecture modulaire où chaque moteur OCR est encapsulé dans sa propre classe :

### Interface commune
Tous les modules OCR implémentent une interface similaire :
- `__init__(confidence_threshold, use_gpu=False)` : Initialisation
- `detect_text(image_path)` : Détection principale
- `get_text_and_confidence(pil_image)` : Texte + confiance
- CLI intégré avec `argparse` pour utilisation standalone

### Structure des modules
```
src/
├── ocr_easyocr.py     # EasyOCRProcessor
├── ocr_tesseract.py   # TesseractOCRProcessor
└── ocr_trocr.py       # TrOCRProcessor
```

### Gestion des dépendances
- **EasyOCR** : `easyocr`, `torch`, `torchvision`
- **Tesseract** : `pytesseract`, `tesseract` system package
- **TrOCR** : `transformers`, `torch`

### Avantages modulaires
1. **Testabilité** : Chaque moteur testable indépendamment
2. **Performance** : Choix du moteur selon les besoins
3. **Maintenance** : Modifications isolées
4. **Extensibilité** : Nouveaux moteurs faciles à ajouter

---

## 🔧 **Module EasyOCR**

Le module `ocr_easyocr.py` encapsule le moteur EasyOCR :

```python
class EasyOCRProcessor:
    def __init__(self, confidence_threshold=0.2, use_gpu=True):
        self.confidence_threshold = confidence_threshold
        self.reader = easyocr.Reader(['en'], gpu=use_gpu)
        print(f"🔍 EasyOCR initialisé - Seuil: {confidence_threshold}, GPU: {use_gpu}")

    def detect_text(self, image_path):
        # Chargement et traitement de l'image
        pil_image = Image.open(image_path)
        return self.get_text_and_confidence(pil_image)

    def get_text_and_confidence(self, pil_image):
        # Conversion et détection OCR
        image_array = np.array(pil_image)
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        results = self.reader.readtext(bgr_image, rotation_info=[0, 90, 180, 270])
        filtered_results = [r for r in results if r[2] >= self.confidence_threshold]

        texts = [r[1] for r in filtered_results]
        avg_confidence = np.mean([r[2] for r in filtered_results]) if filtered_results else 0.0

        return ' '.join(texts), avg_confidence
```

### Utilisation standalone :
```bash
python src/ocr_easyocr.py --image path/to/image.jpg --gpu
```

---

## 📝 **Module Tesseract**

Le module `ocr_tesseract.py` utilise Tesseract avec configurations PSM :

```python
class TesseractOCRProcessor:
    def __init__(self, confidence_threshold=0.3, psm_mode=6):
        self.confidence_threshold = confidence_threshold
        self.psm_mode = psm_mode
        self.tesseract_config = f'--oem 3 --psm {psm_mode} -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ...'
        print(f"🔍 Tesseract initialisé - Seuil: {confidence_threshold}, PSM: {psm_mode}")

    def detect_text(self, image_path):
        pil_image = Image.open(image_path)
        return self.get_text_and_confidence(pil_image)

    def get_text_and_confidence(self, pil_image):
        # Prétraitement et détection
        image_array = np.array(pil_image)
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

        data = pytesseract.image_to_data(gray, config=self.tesseract_config, output_type=pytesseract.Output.DICT)

        results = []
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 0:
                text = data['text'][i].strip()
                confidence = int(data['conf'][i]) / 100.0
                if confidence >= self.confidence_threshold and len(text) >= 2:
                    results.append((text, confidence))

        texts = [text for text, conf in results]
        avg_confidence = np.mean([conf for text, conf in results]) if results else 0.0

        return ' '.join(texts), avg_confidence
```

### Utilisation standalone :
```bash
python src/ocr_tesseract.py --image path/to/image.jpg --psm 6
```

---

## 🤖 **Module TrOCR**

Le module `ocr_trocr.py` utilise le modèle Transformer TrOCR :

```python
class TrOCRProcessor:
    def __init__(self, confidence_threshold=0.5, use_gpu=True):
        self.confidence_threshold = confidence_threshold
        self.device = torch.device('cuda' if use_gpu and torch.cuda.is_available() else 'cpu')

        self.processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-printed')
        self.model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-printed')
        self.model.to(self.device)

        print(f"🔍 TrOCR initialisé - Seuil: {confidence_threshold}, Device: {self.device}")

    def detect_text(self, image_path):
        pil_image = Image.open(image_path)
        return self.get_text_and_confidence(pil_image)

    def get_text_and_confidence(self, pil_image):
        # Prétraitement et génération
        pixel_values = self.processor(pil_image, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(self.device)

        generated_ids = self.model.generate(
            pixel_values,
            max_length=50,
            num_beams=4,
            early_stopping=True
        )

        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        confidence = self._estimate_confidence(pixel_values, generated_ids)

        return generated_text, confidence
```

### Utilisation standalone :
```bash
python src/ocr_trocr.py --image path/to/image.jpg --gpu
```

### Configuration Tesseract :
```python
self.tesseract_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ...'
```
- `--oem 3` : Mode moteur par défaut
- `--psm 6` : Assume un bloc uniforme de texte
- `tessedit_char_whitelist` : Limite aux caractères alphanumériques

---

## 🖼️ **Prétraitement d'image**

Le prétraitement améliore drastiquement la qualité de détection OCR :

```python
def _preprocess_image(self, image):
    # 1. Conversion en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. Amélioration du contraste (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(6,6))
    enhanced = clahe.apply(gray)

    # 3. Réduction du bruit
    denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)

    # 4. Amélioration de la netteté
    gaussian = cv2.GaussianBlur(denoised, (0, 0), 1.0)
    sharpened = cv2.addWeighted(denoised, 1.5, gaussian, -0.5, 0)

    # 5. Binarisation adaptative
    binary = cv2.adaptiveThreshold(sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 3)

    # 6. Dilatation légère
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    dilated = cv2.dilate(binary, kernel, iterations=1)

    return cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
```

### Étapes du prétraitement :

#### 1. **Conversion en niveaux de gris**
```python
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```
**Pourquoi ?** L'OCR fonctionne mieux sur des images en noir et blanc.

#### 2. **CLAHE (Contrast Limited Adaptive Histogram Equalization)**
```python
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(6,6))
enhanced = clahe.apply(gray)
```
**Pourquoi ?** Améliore le contraste localement sans amplifier le bruit.

#### 3. **Filtre bilatéral**
```python
denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)
```
**Pourquoi ?** Réduit le bruit tout en préservant les bords des caractères.

#### 4. **Unsharp masking**
```python
gaussian = cv2.GaussianBlur(denoised, (0, 0), 1.0)
sharpened = cv2.addWeighted(denoised, 1.5, gaussian, -0.5, 0)
```
**Pourquoi ?** Augmente la netteté des caractères.

#### 5. **Binarisation adaptative**
```python
binary = cv2.adaptiveThreshold(sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 3)
```
**Pourquoi ?** Convertit en noir/blanc en s'adaptant aux variations d'éclairage.

#### 6. **Dilatation**
```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
dilated = cv2.dilate(binary, kernel, iterations=1)
```
**Pourquoi ?** Connecte les parties des caractères qui ont été séparées.

---

## 🔍 **Détection de texte avec EasyOCR**

EasyOCR est le moteur OCR principal :

```python
def get_text_and_confidence(self, pil_image, preprocess=True):
    # Conversion PIL → NumPy → BGR
    image_array = np.array(pil_image)
    bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

    # Prétraitement si demandé
    if preprocess:
        bgr_image = self._preprocess_image(bgr_image)

    # Détection OCR avec paramètres optimisés
    results = self.reader.readtext(
        bgr_image,
        rotation_info=[0, 90, 180, 270],  # Détecte toutes les orientations
        width_ths=0.3,      # Tolérance largeur
        height_ths=0.3,     # Tolérance hauteur
        contrast_ths=0.05,  # Seuil contraste très bas
        adjust_contrast=0.7, # Ajustement contraste
        text_threshold=0.5,  # Seuil détection texte
        link_threshold=0.3   # Seuil liaison caractères
    )

    # Filtrage par confiance et longueur
    filtered_results = [
        r for r in results
        if r[2] >= self.confidence_threshold and len(r[1].strip()) >= 2
    ]

    return ' '.join([r[1] for r in filtered_results]), np.mean([r[2] for r in filtered_results])
```

### Paramètres EasyOCR importants :

- **`rotation_info`** : Détecte le texte dans toutes les orientations
- **`width_ths/height_ths`** : Tolérance aux variations de taille
- **`contrast_ths`** : Sensibilité au contraste (très bas pour texte fin)
- **`text_threshold`** : Seuil de confiance pour considérer du texte

### Format des résultats EasyOCR :
```python
[
    [[[x1,y1], [x2,y2], [x3,y3], [x4,y4]], "texte détecté", confiance],
    ...
]
```

---

## 📝 **Détection de texte avec Tesseract**

Tesseract est utilisé comme alternative :

```python
def _tesseract_detect(self, pil_image):
    # Conversion et prétraitement
    image_array = np.array(pil_image)
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    # Détection avec Tesseract
    data = pytesseract.image_to_data(enhanced, config=self.tesseract_config, output_type=pytesseract.Output.DICT)

    results = []
    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        confidence = int(data['conf'][i]) / 100.0

        if confidence > 0.1 and len(text) >= 2:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            bbox = [[x, y], [x+w, y], [x+w, y+h], [x, y+h]]
            results.append([bbox, text, confidence])

    return results
```

### Avantages de Tesseract :
- Plus rapide que EasyOCR
- Meilleur pour le texte horizontal long
- Moins de dépendances

### Inconvénients :
- Moins performant sur les rotations
- Préconfiguration nécessaire pour le texte vertical

---

## 📦 **Extraction des boîtes de texte**

La méthode `get_boxes()` extrait les coordonnées de chaque texte détecté :

```python
def get_boxes(self, pil_image, preprocess=False, vertical_only=False):
    # Détection OCR (EasyOCR ou Tesseract)
    results = self._tesseract_detect(pil_image) if self.use_tesseract else self.reader.readtext(...)

    boxes = []
    for bbox, text, confidence in results:
        # Filtrage de qualité
        if confidence < 0.1 or len(text.strip()) < 1:
            continue

        # Calcul des dimensions
        x = min([p[0] for p in bbox])
        y = min([p[1] for p in bbox])
        width = max([p[0] for p in bbox]) - x
        height = max([p[1] for p in bbox]) - y
        font_size = height  # Approximation

        # Détection texte vertical
        is_vertical = self._is_vertical_text(bbox)

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
```

### Détection du texte vertical :
```python
def _is_vertical_text(self, bbox):
    width = max([p[0] for p in bbox]) - min([p[0] for p in bbox])
    height = max([p[1] for p in bbox]) - min([p[1] for p in bbox])
    return height > width * 1.5  # Ratio hauteur/largeur > 1.5
```

---

## 📚 **Regroupement par livres**

L'algorithme principal regroupe les textes par livre :

```python
def group_by_books(self, boxes, vertical_threshold=50):
    # 1. Filtrer les textes verticaux avec grandes polices
    vertical_boxes = [b for b in boxes if b.get('is_vertical', False)]
    if not vertical_boxes:
        return []

    # 2. Calculer la médiane de la taille de police
    font_sizes = [b['font_size'] for b in vertical_boxes]
    median_font_size = sorted(font_sizes)[len(font_sizes) // 2]

    # 3. Garder seulement les grandes polices
    large_text_boxes = [b for b in vertical_boxes if b['font_size'] >= median_font_size * 0.8]

    # 4. Trier par position X (gauche à droite)
    sorted_boxes = sorted(large_text_boxes, key=lambda b: b['x'])

    # 5. Regrouper par colonnes (même livre)
    books = []
    current_book = [sorted_boxes[0]]
    current_x = sorted_boxes[0]['x']

    for box in sorted_boxes[1:]:
        if abs(box['x'] - current_x) <= vertical_threshold:
            current_book.append(box)  # Même livre
        else:
            books.append(current_book)  # Nouveau livre
            current_book = [box]
            current_x = box['x']

    if current_book:
        books.append(current_book)

    # 6. Extraire les titres
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
```

### Logique de regroupement :

1. **Filtrage vertical** : Seuls les textes verticaux (sur les tranches)
2. **Filtrage par taille** : Les grands textes (titres) vs petits textes (auteurs)
3. **Tri horizontal** : De gauche à droite dans l'image
4. **Regroupement spatial** : Textes proches horizontalement = même livre
5. **Reconstruction** : Combiner tous les textes d'un livre en titre

### Extraction du titre :
```python
def _extract_book_title(self, book_texts):
    # Trier verticalement (haut vers bas)
    sorted_texts = sorted(book_texts, key=lambda b: b['y'])
    all_texts = [b['text'].strip() for b in sorted_texts]
    combined = ' / '.join(all_texts)

    # Limitation de longueur
    return combined[:60] + '...' if len(combined) > 60 else combined
```

---

## 🚀 **Script de détection unifié**

Le script `scripts/ocr_detect.py` orchestre tous les modules OCR :

```python
def main():
    parser = argparse.ArgumentParser(description='ShelfReader - Détection OCR unifiée')
    parser.add_argument('image_path', help='Chemin vers l\'image')
    parser.add_argument('--engine', choices=['easyocr', 'tesseract', 'trocr'],
                       default='easyocr', help='Moteur OCR à utiliser')
    parser.add_argument('--gpu', action='store_true', help='Utiliser GPU')
    parser.add_argument('--confidence', type=float, default=0.2,
                       help='Seuil de confiance')

    args = parser.parse_args()

    # Sélection du processeur selon le moteur choisi
    if args.engine == 'easyocr':
        from src.ocr_easyocr import EasyOCRProcessor
        processor = EasyOCRProcessor(args.confidence, args.gpu)
    elif args.engine == 'tesseract':
        from src.ocr_tesseract import TesseractOCRProcessor
        processor = TesseractOCRProcessor(args.confidence)
    elif args.engine == 'trocr':
        from src.ocr_trocr import TrOCRProcessor
        processor = TrOCRProcessor(args.confidence, args.gpu)

    # Traitement
    text, confidence = processor.detect_text(args.image_path)

    print(f"📊 Résultats avec {args.engine}:")
    print(f"   Texte: {text}")
    print(f"   Confiance: {confidence:.2f}")
```

### Utilisation :
```bash
# Avec EasyOCR (défaut)
python scripts/ocr_detect.py image.jpg

# Avec Tesseract
python scripts/ocr_detect.py image.jpg --engine tesseract

# Avec TrOCR et GPU
python scripts/ocr_detect.py image.jpg --engine trocr --gpu
```

## � **Interactions entre méthodes**

### **Méthodes publiques principales**

La classe `BookOCR` expose **3 méthodes publiques principales** qui s'appellent hiérarchiquement :

```python
# Niveau 1 : Méthode principale appelée par l'utilisateur
def get_books(self, pil_image, preprocess=True):
    boxes = self.get_boxes(pil_image, preprocess=preprocess, vertical_only=False)
    books = self.group_by_books(boxes)
    return books

# Niveau 2 : Extraction des boîtes de texte
def get_boxes(self, pil_image, preprocess=False, vertical_only=False):
    # Appelle _tesseract_detect() ou self.reader.readtext()
    # Appelle _is_vertical_text() et _calculate_font_size()
    return boxes

# Niveau 3 : Détection brute du texte
def get_text_and_confidence(self, pil_image, preprocess=True):
    # Appelle _preprocess_image() si preprocess=True
    # Appelle _tesseract_detect() ou self.reader.readtext()
    return text, confidence
```

### **Arbre d'appels des méthodes**

```
get_books()                    # Point d'entrée principal
├── get_boxes()               # Extraction coordonnées
│   ├── _tesseract_detect()   # OU reader.readtext() (EasyOCR)
│   ├── _is_vertical_text()   # Détection orientation
│   └── _calculate_font_size() # Calcul taille police
├── group_by_books()          # Regroupement spatial
│   └── _extract_book_title() # Reconstruction titre
└── get_text_and_confidence() # Texte + confiance (optionnel)
    ├── _preprocess_image()   # Prétraitement
    └── _tesseract_detect()   # OU reader.readtext()
```

### **Dépendances entre méthodes**

#### **Méthodes utilitaires** (appelées par plusieurs autres) :
- **`_is_vertical_text(bbox)`** : Détecte si texte vertical
  - **Utilisée par** : `get_boxes()`, `group_by_books()`
  - **Raison** : Décision d'inclure/exclure des textes

- **`_calculate_font_size(bbox)`** : Calcule taille approximative
  - **Utilisée par** : `get_boxes()`
  - **Raison** : Filtrage par taille de police

- **`_preprocess_image(image)`** : Améliore qualité image
  - **Utilisée par** : `get_text_and_confidence()`, `get_boxes()`
  - **Raison** : Améliorer précision OCR

#### **Méthodes de détection OCR** :
- **`_tesseract_detect(pil_image)`** : Détection avec Tesseract
  - **Utilisée par** : `get_text_and_confidence()`, `get_boxes()`
  - **Condition** : `self.use_tesseract == True`

- **`self.reader.readtext()`** : Détection avec EasyOCR
  - **Utilisée par** : `get_text_and_confidence()`, `get_boxes()`
  - **Condition** : `self.use_tesseract == False`

### **Flux de données interne**

```python
# Exemple d'appel get_books()
def get_books(self, pil_image, preprocess=True):
    # 1. Obtenir TOUTES les boîtes de texte
    all_boxes = self.get_boxes(pil_image, preprocess=preprocess, vertical_only=False)
    #    ↓
    #    get_boxes() appelle get_text_and_confidence() ou _tesseract_detect()
    #    qui peut appeler _preprocess_image()
    
    # 2. Regrouper spatialement
    books = self.group_by_books(all_boxes)
    #    ↓
    #    group_by_books() appelle _extract_book_title()
    #    qui utilise _is_vertical_text()
    
    return books
```

---

## 🔗 **Interactions entre fichiers**

### **Relation `ocr_detect.py` → `ocr_processor.py`**

Le script `ocr_detect.py` est le **point d'entrée utilisateur** qui **configure et utilise** `BookOCR` :

```python
# ocr_detect.py
def main():
    # 1. PARSING DES ARGUMENTS UTILISATEUR
    args = parser.parse_args()  # --gpu, --tesseract, etc.
    
    # 2. CONFIGURATION DU CHEMIN D'IMPORT
    script_dir = Path(__file__).parent          # scripts/
    src_dir = script_dir.parent / "src"         # src/
    sys.path.insert(0, str(src_dir))            # Ajoute src/ au PYTHONPATH
    
    # 3. IMPORT DE LA CLASSE
    from ocr_processor import BookOCR           # Import depuis src/
    
    # 4. INSTANCIATION AVEC PARAMÈTRES UTILISATEUR
    processor = BookOCR(
        ['en'],                    # langues
        0.2,                       # seuil confiance
        use_gpu=args.gpu,          # option GPU
        use_tesseract=args.tesseract  # moteur OCR
    )
    
    # 5. UTILISATION DES MÉTHODES
    pil_image = Image.open(args.image_path)
    
    # Appel séquentiel des méthodes de BookOCR
    text, confidence = processor.get_text_and_confidence(pil_image, preprocess=False)
    boxes = processor.get_boxes(pil_image, preprocess=False)
    books = processor.get_books(pil_image, preprocess=False)
    
    # 6. AFFICHAGE DES RÉSULTATS
    print(f"📊 Résultats: {len(boxes)} textes, {len(books)} livres")
```

### **Responsabilités séparées**

#### **`ocr_detect.py`** (Couche Interface)
- **Parsing** des arguments utilisateur
- **Configuration** de l'environnement Python
- **Gestion des erreurs** utilisateur
- **Affichage** des résultats formatés
- **Validation** des fichiers d'entrée

#### **`ocr_processor.py`** (Couche Métier)
- **Logique OCR** pure (détection, prétraitement)
- **Algorithmes** de regroupement
- **Calculs** mathématiques et géométriques
- **Gestion** des moteurs OCR (EasyOCR/Tesseract)

### **Avantages de la séparation**

1. **Réutilisabilité** : `BookOCR` peut être utilisé dans d'autres scripts/interfaces
2. **Testabilité** : Logique métier testable indépendamment de l'interface
3. **Maintenabilité** : Changements d'interface sans toucher la logique OCR
4. **Évolutivité** : Possibilité d'ajouter une interface web sans changer `BookOCR`

### **Configuration des imports**

```python
# ocr_detect.py - Configuration des imports
script_dir = Path(__file__).parent      # /path/to/scripts/
src_dir = script_dir.parent / "src"     # /path/to/src/
sys.path.insert(0, str(src_dir))        # Ajoute /path/to/src/ au PYTHONPATH

from ocr_processor import BookOCR       # Import depuis src/ocr_processor.py
```

**Pourquoi cette configuration ?**
- Les scripts sont dans `scripts/`, la classe dans `src/`
- Python ne trouve pas automatiquement `src/` depuis `scripts/`
- `sys.path.insert(0, str(src_dir))` ajoute `src/` au chemin de recherche

---

## ⚡ **Flux d'exécution détaillé**

### **Scénario complet : Analyse d'une image**

```bash
python scripts/ocr_detect.py --gpu test_images/books1.jpg
```

#### **Phase 1 : Initialisation (ocr_detect.py)**

```python
# 1. Parsing arguments
args = parser.parse_args()
# Résultat : image_path="test_images/books1.jpg", gpu=True, tesseract=False

# 2. Validation fichier
if not os.path.exists("test_images/books1.jpg"):
    print("❌ Image introuvable")
    sys.exit(1)

# 3. Configuration imports
script_dir = Path(__file__).parent      # scripts/
src_dir = script_dir.parent / "src"     # src/
sys.path.insert(0, str(src_dir))        # PYTHONPATH += src/

# 4. Import classe
from ocr_processor import BookOCR

# 5. Création instance
processor = BookOCR(['en'], 0.2, use_gpu=True, use_tesseract=False)
# ↓ Appelle BookOCR.__init__()
```

#### **Phase 2 : Initialisation BookOCR**

```python
# BookOCR.__init__()
def __init__(self, languages, confidence_threshold, use_gpu=False, use_tesseract=False):
    self.use_tesseract = False
    self.confidence_threshold = 0.2
    
    # Initialisation EasyOCR avec GPU
    self.reader = easyocr.Reader(['en'], gpu=True)
    print("🔍 OCR initialisé - EasyOCR, Langues: ['en'], Seuil: 0.2, Device: GPU")
```

#### **Phase 3 : Chargement de l'image**

```python
# ocr_detect.py
pil_image = Image.open("test_images/books1.jpg")
# Résultat : Objet PIL.Image avec l'image chargée
```

#### **Phase 4 : Analyse OCR (get_text_and_confidence)**

```python
# ocr_detect.py
text, confidence = processor.get_text_and_confidence(pil_image, preprocess=False)

# ↓ Détail de l'appel
def get_text_and_confidence(self, pil_image, preprocess=False):
    # Conversion PIL → NumPy → BGR
    image_array = np.array(pil_image)
    bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    
    # PAS de prétraitement (preprocess=False)
    
    # Détection EasyOCR
    results = self.reader.readtext(bgr_image, rotation_info=[0, 90, 180, 270])
    
    # Filtrage
    filtered_results = [
        r for r in results
        if r[2] >= 0.2 and len(r[1].strip()) >= 2
    ]
    
    # Agrégation
    texts = [r[1] for r in filtered_results]
    confidences = [r[2] for r in filtered_results]
    
    full_text = ' '.join(texts)
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    
    return full_text, avg_confidence
```

#### **Phase 5 : Extraction des boîtes (get_boxes)**

```python
# ocr_detect.py
boxes = processor.get_boxes(pil_image, preprocess=False)

# ↓ Détail de l'appel
def get_boxes(self, pil_image, preprocess=False, vertical_only=False):
    # Même détection OCR que ci-dessus
    results = self.reader.readtext(bgr_image, rotation_info=[0, 90, 180, 270])
    
    boxes = []
    for bbox, text, confidence in results:
        if confidence >= 0.2 and len(text.strip()) >= 2:
            # Calcul dimensions
            x = min([p[0] for p in bbox])
            y = min([p[1] for p in bbox])
            width = max([p[0] for p in bbox]) - x
            height = max([p[1] for p in bbox]) - y
            font_size = self._calculate_font_size(bbox)
            
            # Détection verticale
            is_vertical = self._is_vertical_text(bbox)
            
            boxes.append({
                "text": text, "x": x, "y": y, "width": width, "height": height,
                "font_size": font_size, "is_vertical": is_vertical
            })
    
    return boxes
```

#### **Phase 6 : Regroupement par livres (get_books)**

```python
# ocr_detect.py
books = processor.get_books(pil_image, preprocess=False)

# ↓ Détail de l'appel
def get_books(self, pil_image, preprocess=True):
    # 1. Obtenir toutes les boîtes
    boxes = self.get_boxes(pil_image, preprocess=preprocess, vertical_only=False)
    
    # 2. Regrouper par livres
    books = self.group_by_books(boxes)
    
    return books

# ↓ group_by_books() en détail
def group_by_books(self, boxes, vertical_threshold=50):
    # 1. Filtrer vertical + grandes polices
    vertical_boxes = [b for b in boxes if b.get('is_vertical', False)]
    font_sizes = [b['font_size'] for b in vertical_boxes]
    median_font_size = sorted(font_sizes)[len(font_sizes) // 2]
    large_text_boxes = [b for b in vertical_boxes if b['font_size'] >= median_font_size * 0.8]
    
    # 2. Trier par position X
    sorted_boxes = sorted(large_text_boxes, key=lambda b: b['x'])
    
    # 3. Regrouper spatialement
    books = []
    current_book = [sorted_boxes[0]]
    current_x = sorted_boxes[0]['x']
    
    for box in sorted_boxes[1:]:
        if abs(box['x'] - current_x) <= 50:  # Seuil de 50px
            current_book.append(box)
        else:
            books.append(current_book)
            current_book = [box]
            current_x = box['x']
    
    if current_book:
        books.append(current_book)
    
    # 4. Extraire titres
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
```

#### **Phase 7 : Affichage des résultats**

```python
# ocr_detect.py
print(f"\n📊 Résultats:")
print(f"   Textes détectés: {len(boxes)}")
print(f"   Livres détectés: {len(books)}")
print(f"   Confiance: {confidence:.2f}")
print(f"   Texte: {text[:80]}{'...' if len(text) > 80 else ''}")

if books:
    print(f"\n📚 Livres détectés ({len(books)}):")
    for i, book in enumerate(books, 1):
        print(f"   {i:2d}. {book['title']}")
        if book['text_count'] > 1:
            other_texts = ', '.join(book['all_texts'][:3])
            print(f"       └─ (+{book['text_count']-1} textes: {other_texts})")

print("\n✅ Analyse terminée!")
```

### **Temps d'exécution approximatif**

- **Initialisation EasyOCR** : 5-10 secondes (chargement modèle)
- **Chargement image** : < 1 seconde
- **Détection OCR** : 2-5 secondes (dépend de la taille image/GPU)
- **Regroupement** : < 1 seconde
- **Affichage** : < 1 seconde

**Total** : 8-17 secondes pour une première analyse

---

## 🔄 **Résumé des interactions**

### **Hiérarchie des appels**
```
Utilisateur
    ↓
ocr_detect.py::main()
    ↓ (import + instanciation)
BookOCR.__init__()
    ↓ (utilisation)
BookOCR.get_books()
    ├── BookOCR.get_boxes()
    │   ├── BookOCR._is_vertical_text()
    │   ├── BookOCR._calculate_font_size()
    │   └── BookOCR.reader.readtext() [EasyOCR]
    └── BookOCR.group_by_books()
        └── BookOCR._extract_book_title()
```

### **Flux de données**
```
Arguments utilisateur → Parsing → Configuration → Instanciation BookOCR
                                                                    ↓
Image PIL → get_books() → get_boxes() → OCR Engine → Boxes filtrées
                                                                 ↓
Boxes filtrées → group_by_books() → Regroupement spatial → Livres
                                                                 ↓
Livres → Affichage formaté → Utilisateur
```

### **Points de décision**
- **Moteur OCR** : `use_tesseract` (Tesseract vs EasyOCR)
- **Accélération** : `use_gpu` (GPU vs CPU)
- **Prétraitement** : Paramètre `preprocess` dans certaines méthodes
- **Filtrage vertical** : Paramètre `vertical_only` dans `get_boxes()`

Cette architecture modulaire permet de **tester chaque composant indépendamment** et de **réutiliser** la logique OCR dans différents contextes (interface web, API, etc.).

## 🎯 **Comment utiliser le système**

Le système OCR modulaire de ShelfReader P1 offre **trois modes d'utilisation** :

### **Mode 1 : Script unifié (Recommandé)**
```bash
cd p1-MVP-Desktop

# EasyOCR (par défaut, recommandé)
python scripts/ocr_detect.py ../data/test_images/sample.jpg

# Avec GPU pour EasyOCR
python scripts/ocr_detect.py ../data/test_images/sample.jpg --engine easyocr --gpu

# Tesseract (rapide, CPU uniquement)
python scripts/ocr_detect.py ../data/test_images/sample.jpg --engine tesseract

# TrOCR (haute précision, GPU recommandé)
python scripts/ocr_detect.py ../data/test_images/sample.jpg --engine trocr --gpu
```

### **Mode 2 : Modules individuels (Développement/Test)**
```bash
# Tester EasyOCR seul
python src/ocr_easyocr.py --image ../data/test_images/sample.jpg --gpu

# Tester Tesseract seul
python src/ocr_tesseract.py --image ../data/test_images/sample.jpg --psm 6

# Tester TrOCR seul
python src/ocr_trocr.py --image ../data/test_images/sample.jpg --gpu
```

### **Mode 3 : Intégration dans votre code**
```python
from src.ocr_easyocr import EasyOCRProcessor

# Initialisation
processor = EasyOCRProcessor(confidence_threshold=0.2, use_gpu=True)

# Utilisation
text, confidence = processor.detect_text("path/to/image.jpg")
print(f"Texte: {text}, Confiance: {confidence:.2f}")
```

### **Structure des fichiers actuelle**
```
p1-MVP-Desktop/
├── src/
│   ├── ocr_easyocr.py      # Module EasyOCR
│   ├── ocr_tesseract.py    # Module Tesseract
│   ├── ocr_trocr.py        # Module TrOCR
│   ├── api_client.py       # Client Open Library
│   ├── app.py              # Interface Streamlit (futur)
│   └── __init__.py
├── scripts/
│   └── ocr_detect.py       # Script unifié
├── docs/
│   ├── README.md           # Documentation principale
│   ├── OCR_Code_Explanation.md  # Guide technique
│   └── Dependencies.md     # Dépendances
├── tests/
│   └── __init__.py
└── requirements.txt        # Dépendances Python
```

---

## 🎯 **Points clés pour réussir**

### 1. **Comprendre les défis**
- Texte vertical sur tranches de livres
- Contraste et qualité variables
- Petits caractères difficiles à détecter

### 2. **Choisir le bon moteur OCR**
- **EasyOCR** : Plus précis, supporte les rotations, GPU accéléré
- **Tesseract** : Plus rapide, configurations PSM avancées, CPU uniquement
- **TrOCR** : Haute précision, modèle transformer, GPU recommandé

### 3. **Architecture modulaire**
- **Séparation des responsabilités** : Chaque moteur dans son propre module
- **Interface commune** : Méthodes `detect_text()` et `get_text_and_confidence()`
- **CLI intégré** : Chaque module utilisable indépendamment
- **Testabilité** : Tests unitaires par moteur OCR

### 4. **Optimisation des performances**
- **GPU** : EasyOCR et TrOCR supportent l'accélération GPU
- **CPU** : Tesseract pour les environnements sans GPU
- **Prétraitement** : Améliore significativement la précision
- **Seuil de confiance** : Ajuster selon la qualité des images

### 5. **Gestion des erreurs**
- Validation des fichiers d'entrée
- Gestion des imports manquants
- Messages d'erreur informatifs
- Robustesse individuelle des modules

---

*Ce document explique l'architecture modulaire OCR de ShelfReader P1. Chaque module peut être utilisé indépendamment ou via le script unifié selon vos besoins.*</content>
<parameter name="filePath">/home/delart/Documents/dev/python/Shelfreader/p1-MVP-Desktop/docs/OCR_Code_Explanation.md