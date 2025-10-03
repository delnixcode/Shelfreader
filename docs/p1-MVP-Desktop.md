# 🏗️ Projet 1 : MVP Desktop (OCR + API + Interface)

## 🎯 Vue d'ensemble - Projet 1

**ShelfReader Desktop MVP** est la première étape concrète du projet. C'est un prototype fonctionnel qui valide le concept de base : **extraire du texte des photos de tranches de livres et l'enrichir avec des données bibliographiques**.

**ShelfReader** combine plusieurs technologies :
1. **Computer Vision** : Détection des tranches de livres
2. **OCR** : Reconnaissance optique de caractères
3. **API REST** : Récupération des métadonnées
4. **IA/ML** : Recommandations personnalisées
5. **Mobile** : Application native temps réel

### 📋 Objectifs du Projet 1
- ✅ **Validation technique** : Prouver que l'OCR fonctionne sur des tranches de livres
- ✅ **Validation fonctionnelle** : Prouver que l'enrichissement API apporte de la valeur
- ✅ **Validation UX** : Prouver que l'interface est utilisable
- ✅ **Base réutilisable** : Créer du code qui sera repris dans les projets suivants

### 🎓 Objectifs pédagogiques
- ✅ Comprendre l'OCR avec EasyOCR (modèle PyTorch pré-entraîné)
- ✅ Structurer un projet Python propre et modulaire
- ✅ Interroger une API REST (Open Library) avec gestion d'erreurs
- ✅ Créer une interface web moderne avec Streamlit
- ✅ Gérer les formats d'images (PIL, NumPy, OpenCV)

### 🚀 Vision finale du Projet 1
```
👤 Utilisateur desktop
     ↓
📸 Upload photo d'étagère
     ↓
🔍 OCR analyse tranches de livres
     ↓
🌐 API enrichit avec métadonnées
     ↓
📊 Interface affiche résultats enrichis
```

**Résultat** : Un prototype qui prouve la viabilité technique et fonctionnelle !

---

## 📋 Roadmap & Phases - Projet 1

Le projet est divisé en **5 phases progressives** pour apprendre étape par étape :

### Phase 1.1 : Configuration et environnement
**Objectif** : Mettre en place l'environnement de développement
- Installation des dépendances (EasyOCR, OpenCV, Streamlit)
- Configuration de l'environnement virtuel
- Tests des installations
- **Durée** : 1-2 jours

### Phase 1.2 : Module OCR de base
**Objectif** : Implémenter l'extraction de texte basique
- Création de la classe `BookOCR`
- Méthode `extract_text_from_pil()` avec TODOs
- Tests avec images simples
- **Durée** : 2-3 jours

### Phase 1.3 : Client API Open Library
**Objectif** : Interroger l'API pour enrichir les données
- Méthodes `search_books()`, `get_book_details()`, `get_book_cover_url()`
- Gestion des erreurs et rate limiting
- Tests unitaires
- **Durée** : 3-4 jours

### Phase 1.4 : Interface Streamlit
**Objectif** : Créer l'interface utilisateur web
- Upload d'images
- Affichage des résultats OCR
- Recherche par titre/thématique
- **Durée** : 2-3 jours

### Phase 1.5 : Intégration et tests
**Objectif** : Assembler tous les composants
- Pipeline complet : OCR → API → Interface
- Tests end-to-end
- Débogage et optimisation
- **Durée** : 2-3 jours

---

## 🏛️ Architecture - Projet 1

```
ShelfReader/
├── src/
│   ├── ocr_module.py      # ← EN COURS : Classe BookOCR
│   ├── api_client.py      # TODO : Client Open Library
│   ├── app.py             # TODO : Interface Streamlit
│   └── torch_utils.py     # TODO : Utilitaires PyTorch (Phase 2)
├── data/
│   └── test_images/       # Images de test
├── requirements.txt       # ✅ Dépendances installées
└── docs/                  # Documentation
```

**Flux de données** :
```
Photo utilisateur → OCR Processing → Texte extrait → API Enrichment → Résultats affichés
```

---

## 🔧 Technologies - Projet 1

| Composant | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| **OCR Engine** | EasyOCR | 1.7+ | Reconnaissance optique de caractères |
| **Computer Vision** | OpenCV | 4.8+ | Traitement d'images et preprocessing |
| **Deep Learning** | PyTorch | 2.0+ | Backend EasyOCR (GPU support) |
| **API Client** | requests | 2.31+ | HTTP client pour Open Library API |
| **Interface** | Streamlit | 1.28+ | UI web pour upload et résultats |
| **Image Processing** | Pillow | 10.0+ | Gestion des formats d'images |

### Installation Commands
```bash
# Environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Dépendances principales
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118  # GPU
pip install easyocr opencv-python pillow streamlit requests

# Vérification GPU (optionnel)
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

### Environment Requirements
- **Python** : 3.8+ (recommandé 3.10+)
- **GPU** : NVIDIA avec CUDA 11.8+ (optionnel, mais recommandé)
- **RAM** : 8GB minimum, 16GB recommandé
- **Stockage** : 2GB pour modèles + données

---

## 🎯 Défis techniques - Projet 1

### Défi 1 : Précision OCR sur tranches de livres
**Problème** : Les tranches de livres sont souvent verticales, avec du texte courbé et des conditions d'éclairage variables
- **Contraintes** : Texte vertical, courbure, éclairage inégal, ombres
- **Solutions** : Rotation automatique, preprocessing adaptatif, seuillage intelligent
- **Métriques** : Taux de reconnaissance > 85% sur photos de tranches
- **Technologies** : OpenCV preprocessing, EasyOCR avec GPU

### Défi 2 : Gestion des erreurs et robustesse
**Problème** : L'application doit gérer les photos de mauvaise qualité, les livres non détectés, les erreurs réseau
- **Contraintes** : Photos floues, livres obstrués, API indisponible, timeouts
- **Solutions** : Validation des inputs, fallback modes, retry logic, user feedback
- **Métriques** : Taux d'erreur < 5%, temps de réponse < 3 secondes
- **Technologies** : Exception handling, logging, async processing

### Défi 3 : Performance et optimisation
**Problème** : Pipeline OCR + API doit être rapide pour une bonne UX desktop
- **Contraintes** : Modèle OCR lourd (~100MB), appels API réseau, traitement d'images
- **Solutions** : Cache intelligent, preprocessing optimisé, GPU acceleration
- **Métriques** : Temps de traitement < 2 secondes, utilisation mémoire < 500MB
- **Technologies** : PyTorch GPU, multiprocessing, LRU cache

---

## 🔄 Architecture d'intégration - Projet 1

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROJET 1 : MVP DESKTOP                       │
│                    OCR + API + Interface                        │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. CAPTURE IMAGE                                                │
│    📸 Upload via Streamlit                                     │
│    ✅ Validation format (JPG/PNG)                              │
│    ✅ Redimensionnement si nécessaire                          │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. PIPELINE OCR                                                 │
│    🔍 BookOCR.extract_text_from_pil()                          │
│    ├── Conversion PIL → NumPy → BGR                            │
│    ├── Preprocessing (gris + égalisation)                      │
│    ├── EasyOCR detection                                       │
│    ├── Filtrage par confidence                                 │
│    └── Retour (texte, confiance)                               │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. ENRICHISSEMENT API                                           │
│    🌐 OpenLibrary.search_books()                                │
│    ├── Recherche par titre/auteur                              │
│    ├── Récupération métadonnées                                │
│    ├── Gestion erreurs réseau                                  │
│    └── Cache local des résultats                               │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. AFFICHAGE RÉSULTATS                                          │
│    📊 Interface Streamlit                                       │
│    ├── Texte OCR détecté                                       │
│    ├── Score de confiance                                      │
│    ├── Métadonnées livres                                      │
│    └── Images de couverture                                    │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                 MVP FONCTIONNEL                                 │
│  ✅ OCR précis • ✅ API enrichie • ✅ Interface intuitive       │
│  ✅ Performance optimisée • ✅ Gestion d'erreurs                │
└─────────────────────────────────────────────────────────────────┘
```

**Flux de données détaillé** :
```
Photo upload (Streamlit)
    ↓
PIL Image (RGB)
    ↓ np.array()
NumPy array (RGB)
    ↓ cv2.cvtColor()
NumPy array (BGR)
    ↓ preprocess_image()
Image optimisée (gris + contraste)
    ↓ reader.readtext()
[(bbox, text, confidence), ...]
    ↓ filtrage confidence
Texte nettoyé + score confiance
    ↓ API search
Métadonnées enrichies
    ↓ Streamlit display
Résultats utilisateur
```

**Fonctionnalités finales Projet 1** :
- ✅ OCR sur tranches de livres
- ✅ Recherche par titre exact
- ✅ Recherche par thématique
- ✅ Enrichissement Open Library
- ✅ Interface web fonctionnelle