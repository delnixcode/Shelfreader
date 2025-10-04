# 🏗️ **P1 - MVP Desktop**
## OCR + API + Interface Web

**ShelfReader MVP Desktop** est la première étape concrète du projet. Prototype fonctionnel validant le concept de base : **extraire du texte des photos de tranches de livres et l'enrichir avec des données bibliographiques**.

### 🎯 **Objectifs**
- ✅ Validation technique : OCR sur tranches de livres
- ✅ Validation fonctionnelle : Enrichissement API Open Library
- ✅ Validation UX : Interface web fonctionnelle
- ✅ Base réutilisable : Code repris dans projets suivants

### 📁 **Structure**
```
p1-MVP-Desktop/
├── env-p1/              # Environnement virtuel P1
├── scripts/             # Scripts utilitaires
│   └── ocr_detect.py    # Script de détection OCR
├── src/                 # Code source P1
│   ├── __init__.py      # Package initialization
│   ├── ocr_processor.py # Module OCR de base
│   ├── api_client.py    # Client Open Library
│   └── app.py           # Interface Streamlit
├── test_images/         # Images de test pour l'OCR
├── tests/               # Tests unitaires
├── docs/                # Documentation spécifique
├── requirements.txt     # Dépendances P1
├── README.md           # Cette documentation
└── TODO.md             # Tâches en cours
```

### 🚀 **Installation & Configuration**

#### 1. Activer l'environnement virtuel
```bash
cd p1-MVP-Desktop
source env-p1/bin/activate  # Linux/Mac
# ou env-p1\Scripts\activate  # Windows
```

#### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

#### 3. Vérifier l'installation
```bash
python -c "import torch; print('PyTorch OK' if torch.cuda.is_available() else 'PyTorch OK (CPU only)')"
```

### 🖥️ **Interface Web (Streamlit)**

#### Démarrage rapide
```bash
streamlit run src/app.py
```

L'interface s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`.

### 🔍 **Script OCR - Commandes**

Le script `scripts/ocr_detect.py` permet de tester l'OCR directement en ligne de commande.

#### Utilisation de base
```bash
# Analyse avec EasyOCR (par défaut) et CPU
python scripts/ocr_detect.py test_images/books1.jpg

# Analyse avec GPU (recommandé pour de meilleures performances)
python scripts/ocr_detect.py --gpu test_images/books1.jpg
```

#### Options avancées
```bash
# Utiliser Tesseract au lieu d'EasyOCR
python scripts/ocr_detect.py --tesseract test_images/books1.jpg

# Tesseract avec GPU
python scripts/ocr_detect.py --gpu --tesseract test_images/books1.jpg

# EasyOCR explicite (équivalent au défaut)
python scripts/ocr_detect.py --easyocr test_images/books1.jpg
```

#### Images de test disponibles
```bash
# Lister les images de test
ls test_images/

# Analyser toutes les images de test
for img in test_images/*.jpg; do
    echo "=== Analyse de $img ==="
    python scripts/ocr_detect.py --gpu "$img"
    echo
done
```

### 🧪 **Tests**

#### Tests unitaires
```bash
# Activer l'environnement virtuel d'abord
source env-p1/bin/activate

# Lancer tous les tests
python -m pytest tests/

# Tests avec couverture
python -m pytest tests/ --cov=src --cov-report=html
```

#### Tests OCR manuels
```bash
# Test rapide avec image de démo
python scripts/ocr_detect.py --gpu test_images/books1.jpg

# Test avec vos propres images
python scripts/ocr_detect.py --gpu chemin/vers/votre/image.jpg
```

### 🔗 **Ressources Partagées**

- **Images de test supplémentaires** : `../../shared/data/test_images/`
- **Documentation générale** : `../../shared/docs/`
- **Scripts partagés** : `../../shared/scripts/`

### 📋 **Phases de développement**

1. **Phase 1.1** ✅ : Configuration environnement
2. **Phase 1.2** ✅ : Module OCR de base
3. **Phase 1.3** ✅ : Client API Open Library
4. **Phase 1.4** ✅ : Interface Streamlit
5. **Phase 1.5** 🔄 : Intégration et tests (en cours)

### 🛠️ **Technologies**

| Composant | Technologie | Version |
|-----------|-------------|---------|
| **OCR** | EasyOCR + PyTorch | GPU/CPU |
| **OCR Alternative** | Tesseract | 5.0+ |
| **Computer Vision** | OpenCV | 4.8+ |
| **API Client** | requests | 2.31+ |
| **Interface** | Streamlit | 1.28+ |
| **Langage** | Python | 3.8+ |

### ⚠️ **Limitations connues**

- **Précision OCR** : La reconnaissance des titres de livres peut nécessiter des améliorations
- **Performance** : L'analyse GPU est recommandée pour de meilleures performances
- **Interface** : L'interface Streamlit est temporaire - une vraie app desktop est prévue

### 🚀 **Prochaines étapes**

- Améliorer la précision de l'OCR
- Développer l'interface desktop native (remplacer Streamlit)
- Optimiser les performances
- Ajouter plus de tests automatisés