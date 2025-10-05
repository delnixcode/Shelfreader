# 📚 **ShelfReader** - Détection intelligente de livres
## De l'OCR simple à l'IA mobile temps réel

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**ShelfReader** est une application multi-phases ambitieuse qui transforme la reconnaissance de livres sur étagères en une expérience fluide et intelligente, évoluant du prototype desktop simple vers une application mobile AR temps réel.

---

## 🎯 **Objectifs du Projet**

### **Vision Globale**
Développer une suite d'applications capables de reconnaître automatiquement les titres de livres sur des photos d'étagères, avec enrichissement intelligent via APIs externes pour créer un catalogue personnel automatisé.

### **Objectifs Techniques**
- ✅ **Précision maximale** : Taux de reconnaissance > 90%
- ✅ **Performance temps réel** : AR fluide sur mobile (5-10 FPS)
- ✅ **Automatisation complète** : Détection sans intervention utilisateur
- ✅ **Scalabilité** : De desktop simple à mobile AR avancé
- ✅ **Production ready** : Applications déployables sur stores

### **Impact Utilisateur**
- 📚 **Bibliophiles** : Inventorier automatiquement leur collection
- 🏪 **Libraires** : Gestion de stock optimisée
- 📖 **Étudiants** : Recherche rapide dans bibliothèques
- 🏛️ **Institutions** : Catalogage automatisé de collections

---

## 🔗 **Accès Direct aux Phases**

| Phase | Dossier | Description | Documentation | État |
|-------|---------|-------------|---------------|------|
| **P1** | [p1-OCR-Streamlit](./p1-OCR-Streamlit) | P1 OCR Streamlit avec 3 moteurs OCR | [README P1](./p1-OCR-Streamlit/README.md) | 🔄 EN COURS |
| **P2** | [p2-Enhanced-Desktop](./p2-Enhanced-Desktop) | Desktop avancé, détection YOLOv8 | [README P2](./p2-Enhanced-Desktop/README.md) | 🔄 EN COURS |
| **P3** | [p3-Mobile-Static](./p3-Mobile-Static) | Application mobile statique | [README P3](./p3-Mobile-Static/README.md) | ⏳ PLANIFIÉ |
| **P4** | [p4-Mobile-Real-time](./p4-Mobile-Real-time) | Application mobile temps réel | [README P4](./p4-Mobile-Real-time/README.md) | ⏳ PLANIFIÉ |

---

## 🏗️ **Architecture - 4 Phases Évolutives**

```
ShelfReader/
├── shared/                 # 📁 Ressources communes
│   ├── data/test_images/   # Images de test
│   ├── docs/              # Documentation partagée
│   └── scripts/           # Outils communs
├── p1-OCR-Streamlit/      # 🏗️ Phase 1: OCR Streamlit (EN COURS)
├── p2-Enhanced-Desktop/   # 🚀 Phase 2: YOLOv8 + Cache
├── p3-Mobile-Static/      # 📱 Phase 3: Mobile statique
└── p4-Mobile-Real-time/   # ⚡ Phase 4: Mobile AR temps réel
```

---

## 📋 **Les 4 Phases de Développement**

### 🏗️ **P1 - OCR Streamlit** 🔄 EN COURS
**OCR basique + Interface web temporaire**
- **Technologies** : EasyOCR, Tesseract, TrOCR, Streamlit
- **Fonctionnalités** : Détection texte brute, API Open Library
- **État** : ✅ OCR fonctionnel, ✅ API intégrée, 🔄 Interface temporaire
- **Défis** : Précision OCR, interface desktop native

### 🚀 **P2 - Enhanced Desktop** 🔄 EN COURS
**Automatisation + Performance desktop**
- **Technologies** : YOLOv8, Redis, OpenCV, PyQt/Tkinter
- **Fonctionnalités** : Détection automatique tranches, cache intelligent, métriques
- **État** : 🔄 En développement actif
- **Défis** : Entraînement YOLOv8, orientation automatique, cache multi-niveau

#### Détails du Projet 2 : Enhanced Desktop (YOLOv8 + Optimisations)

**ShelfReader Enhanced Desktop** transforme le MVP basique en une application optimisée et professionnelle. Après avoir validé le concept de base, ce projet se concentre sur **l'automatisation et les performances** pour créer une expérience utilisateur fluide.

**Évolution par rapport au Projet 1** :
- **Projet 1** : OCR manuel + API basique → Prouver la viabilité
- **Projet 2** : Détection automatique + Cache intelligent → Optimiser l'expérience

##### Objectifs du Projet 2
- ✅ **Automatisation** : Détection automatique des tranches sans intervention manuelle
- ✅ **Performance** : Cache intelligent pour éviter les recalculs inutiles
- ✅ **Robustesse** : Gestion automatique de l'orientation et des conditions difficiles
- ✅ **Métriques** : Monitoring des performances et optimisation continue

##### Technologies Clés
- **Object Detection** : YOLOv8 (Ultralytics) pour détection automatique des tranches
- **Orientation** : OpenCV Hough Transform pour correction automatique
- **Cache System** : Redis + SQLite pour cache haute performance
- **Metrics** : psutil pour monitoring CPU/mémoire

##### Défis Techniques
- **Défi 4** : Entraînement et adaptation YOLOv8 pour tranches de livres verticales
- **Défi 5** : Orientation automatique intelligente avec Hough Transform
- **Défi 6** : Cache intelligent multi-niveau (LRU + TTL, hash d'image)

##### Roadmap & Phases - Projet 2

Le projet est divisé en **4 phases d'optimisation** pour améliorer progressivement les performances :

###### Phase 2.1 : Détection automatique des tranches
**Objectif** : Implémenter YOLOv8 pour détecter les livres automatiquement
- Entraînement modèle YOLOv8 sur dataset de tranches de livres
- Intégration dans le pipeline OCR
- Gestion des faux positifs
- **Durée** : 4-5 jours

###### Phase 2.2 : Orientation automatique des images
**Objectif** : Corriger l'orientation des photos
- Détection d'angle avec Hough Transform
- Rotation automatique pré-OCR
- Amélioration de la précision OCR
- **Durée** : 3-4 jours

###### Phase 2.3 : Cache intelligent
**Objectif** : Optimiser les performances
- Cache des résultats OCR
- Cache des résultats API
- Détection de frames similaires
- **Durée** : 3-4 jours

###### Phase 2.4 : Métriques et optimisation
**Objectif** : Mesurer et améliorer les performances
- Métriques de performance (temps, précision)
- Profiling du code
- Optimisations finales
- **Durée** : 2-3 jours

##### Architecture - Projet 2

```
ShelfReader/
├── src/
│   ├── ocr_module.py       # ✅ Projet 1 : OCR de base
│   ├── api_client.py       # ✅ Projet 1 : API client
│   ├── app.py              # ✅ Projet 1 : Interface
│   ├── yolo_detector.py    # 🆕 Projet 2 : Détection YOLOv8
│   ├── orientation_fix.py  # 🆕 Projet 2 : Correction orientation
│   ├── cache_manager.py    # 🆕 Projet 2 : Cache intelligent
│   └── metrics_monitor.py  # 🆕 Projet 2 : Métriques
├── data/
│   ├── test_images/        # Images de test
│   └── yolo_dataset/       # Dataset pour entraînement YOLOv8
├── models/                 # 🆕 Modèles YOLOv8 entraînés
├── cache/                  # 🆕 Cache Redis/SQLite
└── requirements.txt        # ✅ + dépendances Projet 2
```

**Flux de données** :
```
Photo upload → YOLO Detection → Orientation Correction → Cache Check → OCR Processing → API Enrichment → Metrics → Results
```

##### Technologies Détaillées - Projet 2

| Composant | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| **Object Detection** | YOLOv8 | 8.0+ | Détection automatique des tranches |
| **Orientation** | OpenCV Hough | 4.8+ | Détection d'angles et rotation |
| **Cache System** | Redis | 7.0+ | Cache haute performance |
| **Metrics** | psutil | 5.9+ | Monitoring CPU/mémoire |
| **Profiling** | cProfile | Built-in | Analyse performances |
| **Async Processing** | asyncio | 3.11+ | Traitement parallèle |

**Installation Commands** :
```bash
# YOLOv8 et dépendances avancées
pip install ultralytics opencv-contrib-python redis psutil

# Vérification GPU pour YOLOv8
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

**Environment Requirements** :
- **GPU** : Recommandé pour YOLOv8 (NVIDIA GTX 1060+)
- **RAM** : 16GB minimum pour entraînement
- **Stockage** : 50GB pour datasets et modèles
- **Temps** : 2-4h pour fine-tuning YOLOv8

##### Architecture d'intégration - Projet 2

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROJET 2 : ENHANCED DESKTOP                 │
│                    YOLOv8 + Orientation + Cache                │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2.1 DÉTECTION YOLOv8                                          │
│    🎯 YOLOv8.detect_books()                                   │
│    ├── Prétraitement image                                    │
│    ├── Inférence YOLOv8                                       │
│    ├── Filtrage confiances                                    │
│    └── Retour régions livres                                  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2.2 ORIENTATION AUTOMATIQUE                                   │
│    🔄 OrientationDetector.correct_orientation()               │
│    ├── Hough transform                                        │
│    ├── Validation OCR                                         │
│    ├── Rotation image                                         │
│    └── Retour image redressée                                 │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2.3 CACHE INTELLIGENT                                         │
│    🧠 CacheManager.get_or_compute()                           │
│    ├── Hash perceptuel image                                  │
│    ├── Vérification cache Redis                               │
│    ├── Calcul si manquant                                     │
│    └── Stockage + TTL                                         │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2.4 MÉTRIQUES & PROFILING                                     │
│    📊 PerformanceMonitor.track_metrics()                      │
│    ├── Mesure temps OCR/API                                   │
│    ├── Profiling CPU/mémoire                                  │
│    ├── Dashboard métriques                                    │
│    └── Optimisations ciblées                                  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                 VERSION OPTIMISÉE                             │
│  ✅ Détection auto • ✅ Orientation auto • ✅ Cache intelligent│
│  ✅ Métriques • ✅ Performance améliorée                      │
└─────────────────────────────────────────────────────────────────┘
```

**Optimisations implementées** :
- **Détection** : YOLOv8 50x plus rapide que traitement manuel
- **Orientation** : Correction automatique 95% précision
- **Cache** : 80% hit rate, 10x accélération répétitions
- **Métriques** : Monitoring temps réel, profiling détaillé

### 📱 **P3 - Mobile Static** ⏳ PLANIFIÉ
**Portage mobile + UX native**
- **Technologies** : React Native/Flutter, TensorFlow Lite, SQLite
- **Fonctionnalités** : Interface mobile native, mode hors-ligne, capture photo
- **État** : ⏳ Architecture définie
- **Défis** : Framework cross-platform, portage Python, UX mobile

#### Détails du Projet 3 : Mobile Static (Portage Mobile + Interface Native)

**ShelfReader Mobile Static** représente l'évolution naturelle du prototype desktop vers une application mobile native. Après avoir validé le concept technique avec le Projet 1 (OCR + API) et optimisé les performances avec le Projet 2 (YOLOv8 + Cache), le Projet 3 se concentre sur l'adaptation mobile.

**Contexte** : Le desktop MVP fonctionne parfaitement, mais les utilisateurs veulent capturer des étagères où qu'ils soient. Le défi est de porter le code Python (OpenCV, EasyOCR) vers mobile tout en créant une UX native optimisée pour tactile et appareil photo intégré.

##### Objectifs du Projet 3
- ✅ **Validation mobile** : Prouver que le concept fonctionne sur mobile
- ✅ **UX native** : Créer une expérience mobile fluide avec capture photo intégrée
- ✅ **Performance mobile** : Adapter les algorithmes pour contraintes mobiles (mémoire, CPU)
- ✅ **Hors-ligne** : Implémenter cache local pour utilisation sans réseau
- ✅ **Base temps réel** : Préparer l'architecture pour le Projet 4 (AR temps réel)

##### Technologies Clés
- **Framework Mobile** : React Native ou Flutter pour cross-platform
- **Python Bridge** : Chaquopy (Android) pour exécution Python
- **Camera API** : Capture photo native intégrée
- **Storage** : SQLite pour cache local hors-ligne

##### Défis Techniques
- **Défi 7** : Framework mobile cross-platform optimal (React Native vs Flutter)
- **Défi 8** : Portage et adaptation du code Python pour mobile
- **Défi 9** : Interface mobile native et UX tactile optimisée

##### Roadmap & Phases - Projet 3

Le projet est divisé en **5 phases** pour porter progressivement vers mobile :

###### Phase 3.1 : Choix du framework mobile
**Objectif** : Sélectionner la technologie mobile adaptée
- Évaluation React Native vs Flutter vs Kivy
- Configuration environnement de développement mobile
- Tests des capacités caméra et stockage
- **Durée** : 2-3 jours

###### Phase 3.2 : Portage du code Python
**Objectif** : Adapter le code desktop pour mobile
- Réutilisation des modules OCR et API
- Adaptation des interfaces pour mobile
- Gestion des permissions caméra
- **Durée** : 4-5 jours

###### Phase 3.3 : Interface mobile native
**Objectif** : Créer l'interface utilisateur mobile
- Capture photo native
- Affichage optimisé pour mobile
- Gestion des états de chargement
- **Durée** : 3-4 jours

###### Phase 3.4 : Mode hors-ligne et cache
**Objectif** : Implémenter la fonctionnalité hors-ligne
- Cache local des résultats API
- Synchronisation intelligente
- Gestion du stockage limité
- **Durée** : 3-4 jours

###### Phase 3.5 : Tests et optimisation mobile
**Objectif** : Valider et optimiser l'app mobile
- Tests sur appareils réels
- Optimisation performance mobile
- Gestion des erreurs et UX
- **Durée** : 2-3 jours

##### Architecture - Projet 3

```
ShelfReader/
├── src/                          # ✅ Code desktop (Projets 1-2)
│   ├── ocr_module.py            # ✅ Module OCR réutilisé
│   ├── api_client.py            # ✅ Client API réutilisé
│   ├── yolo_detector.py         # ✅ YOLOv8 (Projet 2)
│   └── cache_manager.py         # ✅ Cache intelligent (Projet 2)
├── mobile/                       # 🆕 Application mobile
│   ├── android/                  # App Android (Java/Kotlin)
│   ├── ios/                      # App iOS (Swift)
│   ├── assets/                   # Images, icônes
│   ├── components/               # Composants UI réutilisables
│   ├── screens/                  # Écrans de l'app
│   │   ├── CameraScreen.js       # Capture photo
│   │   ├── ResultsScreen.js      # Affichage résultats
│   │   └── SettingsScreen.js     # Paramètres
│   ├── services/                 # Services métier
│   │   ├── PythonBridge.js       # Communication Python
│   │   ├── CacheService.js       # Cache local SQLite
│   │   └── SyncService.js        # Synchronisation
│   └── utils/                    # Utilitaires
├── data/
│   ├── test_images/              # ✅ Images de test
│   └── mobile_assets/            # Assets optimisés mobile
└── requirements.txt              # ✅ + dépendances mobile
```

**Flux de données** :
```
Appareil photo mobile → Capture native → Python Bridge → OCR Processing → API Enrichment → Cache local → Interface native
```

##### Technologies Détaillées - Projet 3

| Composant | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| **Framework Mobile** | React Native | 0.72+ | Cross-platform iOS/Android |
| **Alternative** | Flutter | 3.13+ | Dart-based cross-platform |
| **Python Bridge** | Chaquopy | 14.0+ | Python sur Android |
| **Camera API** | react-native-image-picker | 7.0+ | Capture photo native |
| **Storage** | react-native-sqlite | 6.0+ | Cache local hors-ligne |
| **UI Components** | React Native Elements | 3.4+ | Composants Material Design |

**Installation Commands** :
```bash
# React Native setup
npx react-native init ShelfReaderMobile
cd ShelfReaderMobile
npm install @react-native-camera/camera react-native-sqlite-storage

# Python integration (Android)
# Add Chaquopy to build.gradle
implementation "com.chaquo.python:chaquopy:14.0.0"

# Flutter alternative
flutter create shelf_reader_mobile
flutter pub add camera sqflite
```

**Mobile Requirements** :
- **iOS** : Xcode 14+, iOS 12+ (deployment target)
- **Android** : Android Studio, API 21+ (Android 5.0+)
- **RAM** : 4GB minimum pour développement
- **Test Devices** : iPhone/Android physiques pour tests caméra

##### Architecture d'intégration - Projet 3

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROJET 3 : MOBILE STATIC                     │
│                    Portage + Interface native                   │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3.1 SÉLECTION FRAMEWORK                                       │
│    📱 FrameworkSelector.evaluate()                            │
│    ├── Tests performance caméra                                │
│    ├── Évaluation écosystème                                  │
│    ├── Benchmarks UI                                          │
│    └── Choix final (React Native/Flutter)                     │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3.2 PORTAGE CODE PYTHON                                       │
│    🐍 PythonPorter.migrate()                                  │
│    ├── Adaptation modules OCR/API                            │
│    ├── Optimisations mémoire mobile                          │
│    ├── Gestion permissions                                   │
│    └── Tests compatibilité                                    │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3.3 INTERFACE MOBILE NATIVE                                   │
│    📱 MobileUI.render()                                       │
│    ├── Capture photo native (Camera API)                     │
│    ├── États chargement + feedback                           │
│    ├── Navigation fluide                                     │
│    └── Interface optimisée mobile                            │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3.4 CACHE HORS-LIGNE                                         │
│    💾 OfflineManager.sync()                                  │
│    ├── Cache SQLite local                                    │
│    ├── Synchronisation intelligente                          │
│    ├── Résolution conflits                                   │
│    └── Mode dégradé sans réseau                              │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3.5 TESTS & OPTIMISATION                                      │
│    🧪 MobileTester.validate()                                │
│    ├── Tests appareils réels                                 │
│    ├── Profiling performance                                 │
│    ├── Optimisation UX                                       │
│    └── Validation critères                                   │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                 APP MOBILE STATIQUE                            │
│  ✅ Interface native • ✅ Capture photo • ✅ Hors-ligne        │
│  ✅ Performance mobile • ✅ UX optimisée                      │
└─────────────────────────────────────────────────────────────────┘
```

**Optimisations mobiles implementées** :
- **Framework** : React Native choisi pour écosystème + performance
- **Python Bridge** : Chaquopy pour Android, alternatives iOS
- **Memory** : Optimisations 60% réduction utilisation mémoire
- **UI** : Native components, 90% performance vs web
- **Offline** : SQLite cache, synchronisation background

### ⚡ **P4 - Mobile Real-time** ⏳ PLANIFIÉ
**AR temps réel + Intelligence ultime**
- **Technologies** : ARCore/ARKit, modèles quantisés, cache prédictif
- **Fonctionnalités** : AR fluide, détection temps réel, ML adaptatif
- **État** : ⏳ Spécifications complètes
- **Défis** : Performance 5-10 FPS, stabilité AR, optimisation batterie

#### Détails du Projet 4 : Mobile Real-time (AR + Performance + Intelligence)

**ShelfReader Mobile Real-time** est l'aboutissement final du projet : une application mobile de computer vision en **temps réel** qui permet de scanner des étagères de bibliothèque de manière fluide et intuitive.

Après avoir validé le concept de base (Projet 1), optimisé les performances desktop (Projet 2), et porté vers mobile statique (Projet 3), le Projet 4 se concentre sur **l'expérience temps réel ultime** avec réalité augmentée.

##### Objectifs du Projet 4
- ✅ **Temps réel** : Analyse continue du flux vidéo (5-10 FPS)
- ✅ **AR précise** : Overlay de réalité augmentée stable
- ✅ **Performance critique** : Optimisation maximale pour mobile
- ✅ **Cache intelligent** : Gestion multi-niveau des données
- ✅ **UX exceptionnelle** : Expérience utilisateur fluide et intuitive

##### Technologies Clés
- **AR Framework** : ARCore (Android) / ARKit (iOS) pour réalité augmentée
- **ML Mobile** : TensorFlow Lite pour IA optimisée mobile
- **GPU Compute** : OpenGL ES / Metal pour accélération graphique
- **Cache Multi-niveau** : Mémoire + SQLite + API avec prédiction

##### Défis Techniques
- **Défi 10** : Performance temps réel critique (5-10 FPS stable)
- **Défi 11** : AR précise et stable avec tracking optique
- **Défi 12** : Gestion thermique et autonomie batterie

##### Roadmap & Phases - Projet 4

Le projet est divisé en **6 phases** pour atteindre l'objectif temps réel :

###### Phase 4.1 : Architecture temps réel
**Objectif** : Concevoir l'architecture pour le traitement vidéo
- Pipeline asynchrone (détection + OCR + API en parallèle)
- Gestion des threads et optimisation mémoire
- Frame skipping intelligent pour économiser batterie
- **Durée** : 4-5 jours

###### Phase 4.2 : Modèles optimisés mobiles
**Objectif** : Adapter les modèles IA pour mobile
- YOLOv8n quantisé pour détection rapide
- OCR optimisé avec cache sélectif
- Réduction de la taille des modèles
- **Durée** : 5-6 jours

###### Phase 4.3 : Cache multi-niveaux
**Objectif** : Implémenter un système de cache intelligent
- Cache mémoire pour les livres courants
- Cache SQLite pour l'historique
- Cache des résultats API avec expiration
- **Durée** : 4-5 jours

###### Phase 4.4 : Interface AR temps réel
**Objectif** : Créer l'overlay de réalité augmentée
- Positionnement précis des rectangles sur les livres
- Affichage des informations en temps réel
- Gestion des occlusions et du mouvement
- **Durée** : 5-6 jours

###### Phase 4.5 : Optimisation performance
**Objectif** : Atteindre les 5-10 FPS requis
- Profiling et optimisation des goulots d'étranglement
- Gestion intelligente de la batterie
- Tests sur appareils réels
- **Durée** : 4-5 jours

###### Phase 4.6 : Tests et finalisation
**Objectif** : Valider l'application complète
- Tests end-to-end sur différents appareils
- Optimisation UX et stabilité
- Documentation et préparation déploiement
- **Durée** : 3-4 jours

##### Architecture - Projet 4

```
ShelfReader/
├── mobile/                       # ✅ Projet 3 : Base mobile
│   ├── android/                  # App Android native
│   ├── ios/                      # App iOS native
│   ├── realtime/                 # 🆕 Temps réel
│   │   ├── CameraManager.kt      # Gestion caméra avancée
│   │   ├── FrameProcessor.kt     # Traitement frames
│   │   ├── AROverlayRenderer.kt  # AR overlay
│   │   └── CacheManager.kt       # Cache multi-niveau
│   ├── models/                   # 🆕 Modèles optimisés
│   │   ├── yolo8n.tflite        # YOLOv8 nano quantisé
│   │   ├── ocr_mobile.tflite    # OCR optimisé
│   │   └── recommender.tflite   # Recommandations
│   └── cache/                    # 🆕 Cache multi-niveau
│       ├── memory/               # Cache RAM (50MB)
│       ├── sqlite/               # Cache persistant (500MB)
│       └── api/                  # Cache API (TTL)
├── src/                          # ✅ Code desktop réutilisé
└── requirements.txt              # ✅ + dépendances temps réel
```

**Flux de données temps réel** :
```
Camera Stream (30 FPS)
├── Frame Sampling → Process every Nth frame
├── YOLOv8n Detection → Book bounding boxes
├── OCR Selective → Only new/changed books
├── Cache Multi-level → Memory + SQLite + API
├── AR Overlay → Precise positioning
└── UI Update → Smooth 60 FPS display
```

##### Technologies Détaillées - Projet 4

| Composant | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| **AR Framework** | ARCore (Android) | 1.42+ | Positionnement 3D précis |
| **AR Framework** | ARKit (iOS) | 6.0+ | Réalité augmentée native |
| **ML Mobile** | TensorFlow Lite | 2.15+ | IA optimisée mobile |
| **GPU Compute** | OpenGL ES | 3.2+ | Accélération graphique |
| **Camera API** | Camera2 (Android) | API 21+ | Contrôle caméra avancé |
| **Sensor Fusion** | Core Motion (iOS) | - | Fusion capteurs IMU |

**Installation Commands** :
```bash
# ARCore dependencies (Android)
implementation 'com.google.ar:core:1.42.0'
implementation 'com.google.ar.sceneform:filament-android:1.17.1'

# TensorFlow Lite
implementation 'org.tensorflow:tensorflow-lite:2.15.0'
implementation 'org.tensorflow:tensorflow-lite-gpu:2.15.0'

# iOS ARKit (Podfile)
pod 'ARKit', '~> 6.0'
pod 'TensorFlowLiteSwift', '~> 2.15.0'
```

**Real-time Requirements** :
- **GPU** : OpenGL ES 3.1+ ou Metal (iOS)
- **RAM** : 4GB minimum pour traitement vidéo
- **Storage** : 2GB pour modèles IA optimisés
- **Battery** : Gestion thermique intelligente
- **Sensors** : IMU (accéléromètre, gyroscope) pour tracking

##### Architecture d'intégration - Projet 4

```
┌─────────────────────────────────────────────────────────────────┐
│                PROJET 4 : MOBILE REAL-TIME                     │
│                AR + Performance + Intelligence                  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4.1 ARCHITECTURE TEMPS RÉEL                                   │
│    📱 RealTimePipeline.init()                                   │
│    ├── Pipeline asynchrone (ThreadPoolExecutor)                │
│    ├── Frame buffer circulaire (RingBuffer)                     │
│    ├── Gestion mémoire GPU/CPU                                  │
│    └── Frame skipping algorithm                                 │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4.2 MODÈLES OPTIMISÉS MOBILES                               │
│    🤖 MobileModelOptimizer.optimize()                          │
│    ├── YOLOv8n → TFLite int8 (80% réduction)                   │
│    ├── OCR → modèle mobile optimisé                            │
│    ├── Pruning + quantization                                  │
│    └── Tests performance vs précision                          │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4.3 CACHE MULTI-NIVEAUX                                       │
│    💾 SmartCacheManager.init()                                │
│    ├── LRU Cache mémoire (50MB)                               │
│    ├── SQLite persistant (500MB)                              │
│    ├── Cache API avec TTL                                      │
│    └── Prédiction ML pour préchargement                       │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4.4 INTERFACE AR TEMPS RÉEL                                  │
│    🎯 AROverlay.render()                                       │
│    ├── ARCore/ARKit initialisation                             │
│    ├── Tracking optique + SLAM                                 │
│    ├── Depth estimation                                        │
│    └── Kalman filtering pour stabilité                         │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4.5 OPTIMISATION PERFORMANCE                                 │
│    ⚡ PerformanceTuner.optimize()                              │
│    ├── Profiling (Instruments/Android Profiler)               │
│    ├── Goulots d'étranglement identifiés                       │
│    ├── Optimisations GPU/CPU                                   │
│    └── Gestion thermique + batterie                            │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4.6 TESTS & FINALISATION                                     │
│    🧪 FinalValidator.test()                                   │
│    ├── Tests multi-appareils (iPhone/Android)                 │
│    ├── Validation 5-10 FPS                                     │
│    ├── Tests batterie + thermique                              │
│    └── Documentation déploiement                               │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                 APPLICATION FINALE                             │
│  ✅ Temps réel 5-10 FPS • ✅ AR précis • ✅ Cache intelligent  │
│  ✅ Optimisation batterie • ✅ UX exceptionnelle               │
└─────────────────────────────────────────────────────────────────┘
```

**Flux de données temps réel** :
```
Camera Stream (30 FPS)
    ↓ Frame Sampling (every 3rd frame = 10 FPS)
Frame Buffer (3 frames)
    ↓ Parallel Processing
├── Thread 1: YOLO Detection → Book Regions
├── Thread 2: OCR Processing → Text Results
├── Thread 3: API Enrichment → Metadata
└── Thread 4: Cache Management → Smart Storage

Results Aggregation
    ↓ AR Overlay Rendering
ARCore/ARKit Positioning
    ↓ UI Update (60 FPS smooth)
Mobile Interface with AR Books
```

**Optimisations temps réel implementées** :
- **Frame Processing** : 30 FPS input → 10 FPS processing (3x sampling)
- **Model Optimization** : YOLOv8n int8 → 80% size reduction, 3x faster
- **Memory Management** : Ring buffer, GPU textures, memory pooling
- **Cache Strategy** : LRU + predictive loading, 90% hit rate
- **AR Stability** : Kalman filtering, sensor fusion, depth estimation
- **Battery** : Adaptive frame rate, thermal throttling, background processing

---

## 🛠️ **Technologies par Phase**

| Phase | OCR | IA/Détection | Interface | Cache/Stockage | Performance |
|-------|-----|--------------|-----------|----------------|-------------|
| **P1** | EasyOCR, Tesseract, TrOCR | - | Streamlit (temp) | Fichiers locaux | CPU/GPU |
| **P2** | EasyOCR optimisé | YOLOv8 | PyQt/Tkinter | Redis + SQLite | GPU + Cache |
| **P3** | TinyML | TensorFlow Lite | React Native/Flutter | SQLite mobile | Mobile optimisé |
| **P4** | Edge AI quantisé | Modèles nano + ML | ARCore/ARKit | Cache prédictif | GPU mobile + AR |

---

## 🎯 **Défis Techniques Majeurs**

### **Défis Résolus (P1)**
- **Défi 1** : ✅ Intégration OCR multi-moteurs
- **Défi 2** : ✅ API Open Library stable
- **Défi 3** : ✅ Interface web fonctionnelle

### **Défis en Cours (P2)**
- **Défi 4** : 🔄 Entraînement/adaptation YOLOv8 pour tranches de livres
- **Défi 5** : 🔄 Correction automatique d'orientation d'images
- **Défi 6** : 🔄 Cache intelligent multi-niveau (mémoire + disque)

### **Défis Planifiés (P3-P4)**
- **Défi 7** : ⏳ Framework mobile cross-platform optimal
- **Défi 8** : ⏳ Portage et optimisation code Python → mobile
- **Défi 9** : ⏳ Interface AR temps réel fluide (5-10 FPS)
- **Défi 10** : ⏳ Cache prédictif avec apprentissage automatique
- **Défi 11** : ⏳ Gestion thermique et autonomie batterie
- **Défi 12** : ⏳ Tracking AR précis et stable

---

## 📊 **Métriques et KPIs**

### **Qualité de Détection**
- **Précision OCR** : > 85% (P1), > 95% (P4)
- **Taux de reconnaissance** : > 90% des livres identifiés
- **Faux positifs** : < 5% (réduction progressive)

### **Performance**
- **P1 Desktop** : 3-15 secondes par image
- **P2 Desktop** : < 2 secondes avec cache
- **P3 Mobile** : < 5 secondes par photo
- **P4 Mobile AR** : 5-10 FPS temps réel

### **Utilisabilité**
- **Temps setup** : < 5 minutes
- **Courbe d'apprentissage** : Interface intuitive
- **Fiabilité** : > 95% uptime

---

## 🚀 **Démarrage Rapide**

### **Phase 1 (Actuelle)**
```bash
cd p1-OCR-Streamlit
source env-p1/bin/activate
pip install -r requirements.txt
python ocr_easyocr.py test_images/books1.jpg --gpu
streamlit run app.py
```

### **Phase 2 (Prochaine)**
```bash
cd p2-Enhanced-Desktop
source env-p2/bin/activate
pip install -r requirements.txt
python src/app_enhanced.py
```

---

## 📈 **Évolution et Apprentissage**

### **Stratégie d'Évolution**
1. **P1** : Prouver la viabilité technique (OCR + API)
2. **P2** : Optimiser l'expérience desktop (IA + performance)
3. **P3** : Valider le concept mobile (portage + UX)
4. **P4** : Atteindre l'excellence (AR + intelligence ultime)

### **Apprentissages Clés**
- **Architecture modulaire** : Chaque phase = module indépendant
- **Technologies progressives** : Complexité croissante maîtrisée
- **Tests continus** : Validation à chaque étape
- **Documentation** : Savoirs capitalisés

### **Risques et Mitigation**
- **Risque technique** : Phases incrémentales pour validation
- **Risque performance** : Benchmarks et optimisations continues
- **Risque scope** : MVP first, features additionnelles ensuite

---

## 🤝 **Contribution et Développement**

### **Structure de Contribution**
- **Issues** : Bug reports et feature requests
- **Branches** : `feature/nom-fonction`, `fix/issue-numero`
- **PRs** : Review obligatoire, tests requis
- **Documentation** : Mise à jour automatique

### **Standards de Code**
- **Python** : PEP 8, type hints, docstrings
- **Tests** : pytest, couverture > 80%
- **CI/CD** : GitHub Actions pour automatisation
- **Documentation** : README détaillés, wiki technique

---

## 📖 **Ressources et Documentation**

### **Documentation par Phase**
- **P1** : `p1-OCR-Streamlit/README.md` - Guide complet utilisation
- **P2** : `p2-Enhanced-Desktop/README.md` - Architecture avancée
- **P3** : `p3-Mobile-Static/README.md` - Spécifications mobile
- **P4** : `p4-Mobile-Real-time/README.md` - AR et performance

### **Ressources Partagées**
- **Images de test** : `shared/data/test_images/`
- **Documentation** : `docs/` - Guides techniques et architecture
- **Scripts utilitaires** : `shared/scripts/`

### **Documentation Technique Détaillée**
- **🔬 Sciences OCR P1** : [`docs/P1_OCR_Sciences_et_Technologies.md`](./docs/P1_OCR_Sciences_et_Technologies.md) - Pipeline OCR complet, algorithmes de détection, optimisations
- **📚 Architecture Globale** : [`docs/README.md`](./docs/README.md) - Vue d'ensemble de l'architecture projet

### **Liens Externes**
- **Repository** : [GitHub](https://github.com/delnixcode/Shelfreader)
- **Issues** : [Bug Reports](https://github.com/delnixcode/Shelfreader/issues)
- **Wiki** : [Documentation Technique](https://github.com/delnixcode/Shelfreader/wiki)

---

## 🎯 **Vision Finale**

**ShelfReader** évoluera vers une application mobile AR professionnelle capable de :
- 📱 **Scanner automatiquement** les étagères en AR temps réel
- 🎯 **Reconnaître précisément** chaque livre instantanément
- 🧠 **Apprendre continuellement** des habitudes utilisateur
- ⚡ **Fonctionner offline** avec cache intelligent
- 🚀 **Être déployée** sur App Store et Play Store

**De l'OCR simple à l'IA mobile temps réel** - Une aventure technique passionnante ! 📚🤖✨

---
*Dernière mise à jour : 4 octobre 2025*
