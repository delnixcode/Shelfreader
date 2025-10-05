# 📂 **Structure du projet ShelfReader P1**

## Vue d'ensemble

ShelfReader P1 est organisé selon une architecture modulaire permettant le développement et le test indépendants de chaque composant OCR.

## Structure des dossiers

```
p1-MVP-Desktop/
├── src/                          # Code source principal
│   ├── __init__.py              # Package Python
│   ├── api_client.py            # Client API Open Library
│   ├── app.py                   # Interface Streamlit (futur)
│   ├── ocr_easyocr.py           # Module OCR EasyOCR
│   ├── ocr_tesseract.py         # Module OCR Tesseract
│   └── ocr_trocr.py             # Module OCR TrOCR
├── scripts/                      # Scripts utilitaires
│   └── ocr_detect.py            # Script de détection unifié
├── docs/                         # Documentation
│   ├── README.md                # Guide utilisateur
│   ├── OCR_Code_Explanation.md  # Guide technique détaillé
│   ├── Dependencies.md          # Gestion des dépendances
│   └── Structure.md             # Ce fichier
├── tests/                        # Tests unitaires
│   └── __init__.py              # Package de tests
├── requirements.txt             # Dépendances Python
└── TODO.md                      # Liste des tâches
```

## Description des modules

### 🔧 **Modules OCR** (`src/ocr_*.py`)

#### `ocr_easyocr.py`
- **Classe** : `EasyOCRProcessor`
- **Spécialisation** : Détection précise avec support GPU
- **Dépendances** : `easyocr`, `torch`, `torchvision`
- **Usage** : Texte complexe, rotations, haute précision

#### `ocr_tesseract.py`
- **Classe** : `TesseractOCRProcessor`
- **Spécialisation** : Performance et configurations PSM
- **Dépendances** : `pytesseract`, `tesseract` (system)
- **Usage** : Texte simple, rapidité, CPU uniquement

#### `ocr_trocr.py`
- **Classe** : `TrOCRProcessor`
- **Spécialisation** : Modèle transformer avancé
- **Dépendances** : `transformers`, `torch`
- **Usage** : Haute précision, GPU recommandé

### 🌐 **API Client** (`src/api_client.py`)
- **Classe** : `OpenLibraryClient`
- **Responsabilités** : Requêtes vers Open Library API
- **Dépendances** : `requests`
- **Usage** : Récupération des métadonnées de livres


### 🎨 **Interface** (`src/app.py`)
- **Framework** : Streamlit
- **Responsabilités** : Interface utilisateur web verticale desktop
- **Layout** : 1ère ligne (image+paramètres), 2ème ligne (résultats+livres), 3ème ligne (détails+visualisation)
- **État** : Finalisée (Phase 3)

### 🚀 **Script unifié** (`scripts/ocr_detect.py`)
- **Responsabilités** : Orchestration des modules OCR
- **Arguments** : Sélection du moteur, options GPU, seuils
- **Usage** : Point d'entrée principal pour les tests


## Flux de données (layout vertical desktop)

```
Image upload → Interface Streamlit verticale
        ↓
Image originale + paramètres (1ère ligne)
        ↓
Résultats + livres détectés (2ème ligne)
        ↓
Détails par livre + visualisation zones (3ème ligne)
        ↓
API Client → Métadonnées Open Library
```

## Architecture modulaire

### Avantages
1. **Indépendance** : Chaque module testable séparément
2. **Maintenabilité** : Modifications isolées
3. **Évolutivité** : Nouveaux moteurs faciles à ajouter
4. **Performance** : Choix optimal selon les besoins

### Interface commune
Tous les modules OCR implémentent :
- `__init__(confidence_threshold, use_gpu=False)`
- `detect_text(image_path)`
- `get_text_and_confidence(pil_image)`
- CLI intégré avec `argparse`

## Dépendances

### Core
- `opencv-python` : Traitement d'images
- `Pillow` : Manipulation d'images
- `numpy` : Calculs numériques

### OCR Engines
- `easyocr` : Moteur EasyOCR
- `pytesseract` : Interface Tesseract
- `transformers` : Modèles TrOCR
- `torch` : Framework deep learning

### Interface
- `streamlit` : Interface web (futur)

### API
- `requests` : Requêtes HTTP

## Phases de développement

- ✅ **Phase 1** : API Client Open Library
- ✅ **Phase 2** : OCR Modulaire (3 moteurs)
- ⏳ **Phase 3** : Interface Streamlit
- ⏳ **Phase 4** : Tests et validation

## Utilisation

### Mode unifié
```bash
python scripts/ocr_detect.py image.jpg --engine easyocr --gpu
```

### Mode individuel
```bash
python src/ocr_easyocr.py --image image.jpg --gpu
```

### Développement
```python
from src.ocr_easyocr import EasyOCRProcessor
processor = EasyOCRProcessor(0.2, use_gpu=True)
text, confidence = processor.detect_text("image.jpg")
```