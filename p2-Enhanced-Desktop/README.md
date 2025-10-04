# 🚀 **P2 - Enhanced Desktop**
## YOLOv8 + Orientation + Cache intelligent

**ShelfReader Enhanced Desktop** transforme le MVP basique en application optimisée et professionnelle. Se concentre sur **l'automatisation et les performances** pour créer une expérience utilisateur fluide.

### 🎯 **Objectifs**
- ✅ **Automatisation** : Détection automatique des tranches (YOLOv8)
- ✅ **Performance** : Cache intelligent pour éviter recalculs
- ✅ **Robustesse** : Gestion automatique orientation et conditions difficiles
- ✅ **Métriques** : Monitoring performances et optimisation continue

### 📁 **Structure**
```
p2-Enhanced-Desktop/
├── src/                    # Code source P2
│   ├── __init__.py        # Package initialization
│   ├── ocr_processor.py   # OCR de base (hérité P1)
│   ├── api_client.py      # API client (hérité P1)
│   ├── yolo_detector.py   # 🆕 Détection YOLOv8
│   ├── orientation_fix.py # 🆕 Correction orientation automatique
│   ├── cache_manager.py   # 🆕 Cache intelligent
│   └── app_enhanced.py    # Interface améliorée
├── tests/                 # Tests P2
├── docs/                  # Documentation spécifique
└── requirements.txt       # Dépendances P2 (+ YOLOv8)
```

### 🚀 **Démarrage rapide**
```bash
cd p2-Enhanced-Desktop
source env-p2/bin/activate  # Linux/Mac
# ou env-p2\Scripts\activate  # Windows
pip install -r requirements.txt
python src/app_enhanced.py
```

### 🧪 **Tests**
```bash
# Activer l'environnement virtuel
source env-p2/bin/activate  # Linux/Mac

# Tests du projet P2
python -m pytest tests/

# Test du détecteur YOLOv8
python src/book_detector.py
```
```
p2-Enhanced-Desktop/
├── src/                    # Code source P2
│   ├── __init__.py        # Package initialization
│   ├── ocr_processor.py   # OCR de base (hérité P1)
│   ├── api_client.py      # API client (hérité P1)
│   ├── yolo_detector.py   # 🆕 Détection YOLOv8
│   ├── orientation_fix.py # 🆕 Correction orientation automatique
│   ├── cache_manager.py   # 🆕 Cache intelligent
│   └── app_enhanced.py    # Interface améliorée
├── tests/                 # Tests P2
├── docs/                  # Documentation spécifique
└── requirements.txt       # Dépendances P2 (+ YOLOv8)
```

### 🚀 **Évolution par rapport P1**
- **P1** : OCR manuel + API basique → Prouver viabilité
- **P2** : Détection auto + Cache intelligent → Optimiser expérience

### 📋 **Phases de développement**
1. **Phase 2.1** : Détection automatique tranches (YOLOv8)
2. **Phase 2.2** : Orientation automatique images
3. **Phase 2.3** : Cache intelligent
4. **Phase 2.4** : Métriques et optimisation

### 🛠️ **Technologies ajoutées**
- **Object Detection** : YOLOv8 (Ultralytics)
- **Orientation** : OpenCV Hough Transform
- **Cache System** : Redis/SQLite
- **Metrics** : psutil, cProfile
- **Async Processing** : asyncio

### 🎯 **Défis techniques**
- **Défi 4** : Entraînement/adaptation YOLOv8
- **Défi 5** : Orientation automatique intelligente
- **Défi 6** : Cache intelligent multi-niveau

### 🚀 **Démarrage rapide**
```bash
cd p2-Enhanced-Desktop
pip install -r requirements.txt
python src/app_enhanced.py
```

### 🔗 **Ressources Partagées**
- **Images de test** : `../../shared/data/test_images/`
- **Documentation** : `../../shared/docs/`
- **Scripts** : `../../shared/scripts/`

### 🧪 **Tests**
```bash
# Tests du projet P2
python -m pytest tests/

# Test du détecteur YOLOv8
python src/book_detector.py
```