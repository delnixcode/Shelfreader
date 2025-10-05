# 📚 ShelfReader - Guide des Dépendances

## Vue d'ensemble

Ce document détaille toutes les bibliothèques utilisées dans le projet **ShelfReader** et leur rôle dans chacun des 4 projets (P1-P4). Le fichier `requirements.txt` contient **118 dépendances** organisées par catégories pour garantir la compatibilité entre tous les projets.

## 📦 Organisation des Dépendances

### 🔄 Dépendances Existantes (Environnement de Base)

Ces dépendances étaient déjà présentes dans l'environnement et ont été préservées pour maintenir la compatibilité :

#### NVIDIA CUDA Libraries
- **`nvidia-cufile-cu12==1.13.1.3`** : Accès direct aux fichiers GPU pour optimiser les transferts de données
- **`nvidia-curand-cu12==10.3.9.90`** : Génération de nombres aléatoires sur GPU
- **`nvidia-cusolver-cu12==11.7.3.90`** : Résolution d'équations linéaires et décomposition matricielle sur GPU
- **`nvidia-cusparse-cu12==12.5.8.93`** : Opérations sur matrices creuses optimisées pour GPU
- **`nvidia-cusparselt-cu12==0.7.1`** : Support pour matrices creuses spécialisées
- **`nvidia-nccl-cu12==2.27.3`** : Communication collective multi-GPU
- **`nvidia-nvjitlink-cu12==12.8.93`** : Compilation JIT pour GPU
- **`nvidia-nvtx-cu12==12.8.90`** : Outils de profiling et débogage GPU

#### OpenCV Ecosystem
- **`opencv-python==4.12.0.88`** : Bibliothèque principale de computer vision
- **`opencv-python-headless==4.12.0.88`** : Version d'OpenCV sans interface graphique (serveur)

#### Data Science & Scientific Computing
- **`pandas==2.3.3`** : Manipulation et analyse de données tabulaires
- **`numpy>=1.24.0`** : Calculs numériques et tableaux multidimensionnels
- **`scipy>=1.11.0`** : Fonctions mathématiques avancées et optimisation

#### Web & Interface
- **`streamlit>=1.28.0`** : Framework pour créer des applications web de data science
- **`pydeck==0.9.1`** : Visualisation de cartes interactives (utilisé par Streamlit)

#### Image Processing
- **`Pillow>=10.0.0`** : Bibliothèque d'imagerie (PIL - Python Imaging Library)
- **`scikit-image==0.25.2`** : Algorithmes avancés de traitement d'images

#### Utilitaires & Outils
- **`packaging==25.0`** : Outils de gestion des versions de packages
- **`python-dateutil==2.9.0.post0`** : Extension de datetime pour parsing avancé
- **`pytz==2025.2`** : Gestion des fuseaux horaires
- **`PyYAML==6.0.3`** : Parsing et génération de fichiers YAML
- **`setuptools==80.9.0`** : Outils d'installation et distribution de packages
- **`typing_extensions==4.15.0`** : Extensions pour les annotations de type
- **`urllib3==2.5.0`** : Client HTTP pour Python

#### Autres Dépendances Système
- **`protobuf==6.32.1`** : Sérialisation de données structurées
- **`pyarrow==21.0.0`** : Format de données columnar (utilisé par pandas)
- **`shapely==2.1.2`** : Géométrie planaire et manipulation de formes
- **`sympy==1.14.0`** : Mathématiques symboliques
- **`tifffile==2025.9.30`** : Lecture/écriture de fichiers TIFF
- **`toml==0.10.2`** : Parsing de fichiers TOML
- **`watchdog==6.0.0`** : Surveillance de changements de fichiers

## 🆕 Dépendances Ajoutées par Projet

### 🎯 P1 - OCR Streamlit (OCR + API + Interface Web)

#### PyTorch Ecosystem (Deep Learning)
- **`torch>=2.0.0`** : Framework de deep learning principal
  - *Rôle* : Moteur d'inférence pour les modèles d'OCR et de computer vision
  - *Utilisation* : Traitement des images et reconnaissance de texte via EasyOCR

- **`torchvision>=0.15.0`** : Bibliothèque de computer vision pour PyTorch
  - *Rôle* : Transformations d'images et modèles pré-entraînés
  - *Utilisation* : Prétraitement des images avant OCR

- **`torchaudio>=2.0.0`** : Bibliothèque audio pour PyTorch
  - *Rôle* : Traitement audio (même si pas utilisé directement en P1)
  - *Utilisation* : Dépendance d'EasyOCR pour certains modèles

#### OCR (Optical Character Recognition)
- **`easyocr>=1.7.0`** : Bibliothèque OCR moderne et facile d'utilisation
  - *Rôle* : Extraction de texte à partir d'images de tranches de livres
  - *Utilisation* : Reconnaissance automatique des titres de livres
  - *Avantages* : Support multi-langues, modèles pré-entraînés, bonne précision

#### Computer Vision
- **`opencv-python>=4.8.0`** : Open Source Computer Vision
  - *Rôle* : Traitement d'images et manipulation de base
  - *Utilisation* : Redimensionnement, correction d'orientation, préprocessing

#### API & Réseau
- **`requests>=2.31.0`** : Bibliothèque HTTP pour Python
  - *Rôle* : Client pour effectuer des requêtes vers l'API Open Library
  - *Utilisation* : Récupération des métadonnées des livres

#### Interface Web
- **`streamlit>=1.28.0`** : Framework d'applications web pour data science
  - *Rôle* : Interface utilisateur pour upload d'images et affichage des résultats
  - *Utilisation* : Création d'une interface web simple pour l'application desktop

#### Outils de Développement
- **`pytest>=7.4.0`** : Framework de tests pour Python
  - *Rôle* : Écriture et exécution de tests unitaires et d'intégration
  - *Utilisation* : Validation du fonctionnement des modules API, OCR et interface

- **`black>=23.0.0`** : Formateur de code Python automatique
  - *Rôle* : Standardisation du style de code
  - *Utilisation* : Formatage automatique du code selon PEP 8

- **`flake8>=6.0.0`** : Outil de linting pour Python
  - *Rôle* : Détection d'erreurs de style et de bugs potentiels
  - *Utilisation* : Analyse statique du code pour maintenir la qualité

### 🚀 P2 - Enhanced Desktop (YOLOv8 + Cache Intelligent)

#### Object Detection
- **`ultralytics>=8.0.0`** : Framework YOLOv8 pour détection d'objets
  - *Rôle* : Détection automatique des tranches de livres dans les images
  - *Utilisation* : Localisation précise des livres avant l'OCR
  - *Avantages* : Modèles pré-entraînés, haute performance, API simple

#### Cache & Performance
- **`redis>=4.5.0`** : Base de données en mémoire pour le cache
  - *Rôle* : Système de cache intelligent pour OCR et API
  - *Utilisation* : Éviter de retraiter les mêmes images/livres
  - *Avantages* : Haute performance, persistence optionnelle

- **`psutil>=5.9.0`** : Bibliothèque de monitoring système
  - *Rôle* : Surveillance des performances et utilisation des ressources
  - *Utilisation* : Métriques de performance, profiling, optimisation

#### Computer Vision Avancé
- **`opencv-contrib-python>=4.8.0`** : Extensions OpenCV avec modules supplémentaires
  - *Rôle* : Fonctions avancées de computer vision
  - *Utilisation* : Correction d'orientation automatique, détection de contours

#### Tests Asynchrones
- **`pytest-asyncio>=0.21.0`** : Support pour tests asynchrones dans pytest
  - *Rôle* : Tests de fonctions async/await
  - *Utilisation* : Validation des opérations de cache asynchrones

### 📱 P3 - Mobile Static (Interface Native + Offline)

#### Mobile Python Framework
- **`kivy>=2.2.0`** : Framework open-source pour applications mobiles/multi-touch
  - *Rôle* : Création d'interfaces utilisateur natives pour mobile
  - *Utilisation* : Portage de l'application desktop vers mobile
  - *Avantages* : Cross-platform (iOS, Android, Desktop), interface tactile

- **`kivy-garden>=0.1.5`** : Extensions et widgets supplémentaires pour Kivy
  - *Rôle* : Composants UI avancés et fonctionnalités supplémentaires
  - *Utilisation* : Amélioration de l'interface utilisateur mobile

### ⚡ P4 - Mobile Real-time (AR + Performance Maximale)

#### Mobile AI & TensorFlow
- **`tensorflow>=2.13.0`** : Framework de machine learning de Google
  - *Rôle* : Conversion de modèles pour TensorFlow Lite
  - *Utilisation* : Optimisation des modèles pour mobile

- **`tensorflow-lite>=2.13.0`** : Version optimisée de TensorFlow pour mobile/edge
  - *Rôle* : Exécution de modèles ML sur appareils mobiles
  - *Utilisation* : Inference temps réel sur mobile avec faible latence

#### Calculs Scientifiques Avancés
- **`numpy>=1.24.0`** : Bibliothèque de calculs numériques (arrays, matrices)
  - *Rôle* : Calculs mathématiques et manipulation de tableaux
  - *Utilisation* : Traitement de signaux, calculs de performance

- **`scipy>=1.11.0`** : Bibliothèque scientifique pour Python
  - *Rôle* : Fonctions mathématiques avancées et optimisation
  - *Utilisation* : Traitement de signaux avancés, optimisation de performance

#### Tests de Performance
- **`pytest-benchmark>=4.0.0`** : Plugin pytest pour benchmarking
  - *Rôle* : Mesure des performances et optimisation
  - *Utilisation* : Tests de performance pour l'application temps réel

## 🎯 Rôles par Projet

### P1 - OCR Streamlit
**Focus** : Fonctionnalités de base OCR + API + Interface
**Bibliothèques clés** : EasyOCR, OpenCV, Streamlit, PyTorch
**Objectif** : Prouver la faisabilité technique

### P2 - Enhanced Desktop
**Focus** : Optimisation et intelligence
**Bibliothèques clés** : YOLOv8, Redis, OpenCV-contrib, psutil
**Objectif** : Améliorer les performances et la précision

### P3 - Mobile Static
**Focus** : Portage mobile avec interface native
**Bibliothèques clés** : Kivy, Kivy-garden, SQLite (built-in)
**Objectif** : Accessibilité mobile avec fonctionnalités offline

### P4 - Mobile Real-time
**Focus** : Performance maximale et réalité augmentée
**Bibliothèques clés** : TensorFlow Lite, NumPy, SciPy, Ultralytics
**Objectif** : Application temps réel avec AR et haute performance

## 📋 Installation

Pour installer toutes les dépendances :

```bash
pip install -r requirements.txt
```

## ⚠️ Notes Importantes

1. **GPU Support** : Les bibliothèques NVIDIA CUDA sont incluses pour l'accélération GPU
2. **Versions** : Certaines dépendances ont des versions fixes pour garantir la stabilité
3. **Cross-platform** : Toutes les bibliothèques sont compatibles Windows/Linux/macOS
4. **Mobile** : Pour le développement mobile natif, des outils supplémentaires peuvent être nécessaires

## 🔄 Mise à Jour des Dépendances

Pour mettre à jour les dépendances :

```bash
pip install --upgrade -r requirements.txt
```