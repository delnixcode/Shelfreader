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
├── tests/               # Tests unitaires
├── docs/                # Documentation spécifique
└── requirements.txt     # Dépendances P1
```

### 🚀 **Démarrage rapide**
```bash
cd p1-MVP-Desktop
source env-p1/bin/activate  # Linux/Mac
# ou env-p1\Scripts\activate  # Windows
pip install -r requirements.txt
streamlit run src/app.py
```

### 🧪 **Tests**
```bash
# Activer l'environnement virtuel
source env-p1/bin/activate  # Linux/Mac

# Tests du projet P1
python -m pytest tests/

# Test du script de détection OCR
python scripts/ocr_detect.py
```
```
p1-MVP-Desktop/
├── src/                    # Code source P1
│   ├── __init__.py        # Package initialization
│   ├── ocr_processor.py   # Module OCR de base
│   ├── api_client.py      # Client Open Library
│   └── app.py             # Interface Streamlit
├── tests/                 # Tests unitaires
├── docs/                  # Documentation spécifique
└── requirements.txt       # Dépendances P1
```

### 🚀 **Fonctionnalités finales**
- ✅ OCR sur tranches de livres (EasyOCR)
- ✅ Recherche par titre exact
- ✅ Recherche par thématique
- ✅ Enrichissement Open Library API
- ✅ Interface web Streamlit

### 📋 **Phases de développement**
1. **Phase 1.1** : Configuration environnement
2. **Phase 1.2** : Module OCR de base
3. **Phase 1.3** : Client API Open Library
4. **Phase 1.4** : Interface Streamlit
5. **Phase 1.5** : Intégration et tests

### 🛠️ **Technologies**
- **OCR** : EasyOCR avec PyTorch
- **Computer Vision** : OpenCV
- **API** : requests (Open Library)
- **Interface** : Streamlit
- **Langage** : Python 3.8+

### 🚀 **Démarrage rapide**
```bash
cd p1-MVP-Desktop
pip install -r requirements.txt
streamlit run src/app.py
```

### 🔗 **Ressources Partagées**
- **Images de test** : `../../shared/data/test_images/`
- **Documentation** : `../../shared/docs/`
- **Scripts** : `../../shared/scripts/`

python scripts/ocr_detect.py --gpu test_images/books1.jpg
python scripts/ocr_detect.py --gpu --tesseract test_images/books1.jpg

### 🧪 **Tests**
```bash
# Tests du projet P1
python -m pytest tests/

# Tests avec images partagées
python src/ocr_processor.py ../../shared/data/test_images/books1.jpg
```