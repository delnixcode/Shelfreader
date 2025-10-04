# 📚 ShelfReader - Détection intelligente de livres

Application multi-phases pour détecter et identifier des livres sur des étagères via OCR et IA.

## 🎯 **But Principal**
Développer une application capable de reconnaître automatiquement les titres de livres sur des photos d'étagères, avec enrichissement via APIs externes pour obtenir des informations détaillées sur chaque livre.

## 🏗️ **Architecture - 4 Phases**

```
ShelfReader/
├── shared/                 # 📁 Ressources communes (images test, docs)
├── p1-MVP-Desktop/        # 🏗️ Phase 1: OCR de base (EN COURS)
├── p2-Enhanced-Desktop/   # 🚀 Phase 2: YOLOv8 + Cache
├── p3-Mobile-Static/      # 📱 Phase 3: Mobile statique
└── p4-Mobile-Real-time/   # ⚡ Phase 4: Mobile temps réel
```

## 📋 **Les 4 Phases**

### 🏗️ **P1 - MVP Desktop** 🔄 EN COURS
- **OCR** : EasyOCR + Tesseract ✅ (détection basique)
- **Interface** : Streamlit web (temporaire)
- **API** : Open Library pour enrichissement ✅
- **Résultats** : Détection de texte brute (précision à améliorer)
- **À faire** : Application desktop native + amélioration OCR

### 🚀 **P2 - Enhanced Desktop** 🔄 EN COURS
- **IA** : YOLOv8 pour détection précise
- **Cache** : Redis pour performances
- **Monitoring** : Métriques temps réel
- **Interface** : Application desktop native complète

### 📱 **P3 - Mobile Static** ⏳ PLANIFIÉ
- **TinyML** : IA légère pour mobile
- **Offline** : Fonctionnement sans réseau
- **Interface** : Optimisée mobile

### ⚡ **P4 - Mobile Real-time** ⏳ PLANIFIÉ
- **Streaming** : Analyse vidéo en direct
- **Edge AI** : Traitement sur device
- **Recommandations** : Suggestions intelligentes

## 🚀 **Démarrage Rapide (P1)**

```bash
cd p1-MVP-Desktop
source env-p1/bin/activate
pip install -r requirements.txt
python ocr_easyocr.py test_images/books1.jpg --gpu
streamlit run app.py
```

## 🎯 **Technologies Clés**

| Phase | OCR | IA | Interface | Cache |
|-------|-----|----|-----------|-------|
| **P1** | EasyOCR | - | Streamlit* | - |
| **P2** | EasyOCR | YOLOv8 | Desktop App | Redis |
| **P3** | TinyML | TensorFlow | Kivy | SQLite |
| **P4** | Edge AI | ONNX | React Native | Distributed |

*Interface temporaire - application desktop native à développer
**Application desktop native complète

## 📊 **État Actuel**
- 🔄 **P1** : OCR fonctionnel, interface web temporaire (app desktop à développer)
- 🔄 **P2** : En développement
- ⏳ **P3-P4** : Architecture planifiée

## 📖 **Ressources**
- **Images test** : `shared/data/test_images/`
- **Documentation** : `shared/docs/` et `*/docs/`
- **Scripts** : `p1-MVP-Desktop/ocr_easyocr.py`, `ocr_tesseract.py`, `ocr_trocr.py`

---

**ShelfReader** - De l'OCR simple à l'IA mobile temps réel 📚🤖
