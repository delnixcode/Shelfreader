# 🏗️ **ShelfReader P1 - MVP Desktop**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io## 📚 Documentation

- [🏗️ Architecture & Documentation](docs/P1_Architecture_Documentation.md) - Vue d'ensemble complète du projet
- [📊 État d'Avancement](docs/P1_Status_Report.md) - Suivi du développement et métriques
- [🧪 Guide des Tests](docs/Testing_Guide.md) - Tests et validation
- [🔧 Dépendances](docs/Dependencies.md) - Gestion des dépendances détaillée
- [📖 Guide OCR](docs/OCR_Code_Explanation.md) - Explication technique du code OCR[EasyOCR](https://img.shields.io/badge/EasyOCR-1.7+-green.svg)](https://github.com/JaidedAI/EasyOCR)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Reconnaissance automatique de livres sur étagères avec OCR intelligent**

## 📦 Installation

### Prérequis
- Python 3.8+
- pip
- Un GPU (optionnel, recommandé)

### Étapes

#### 1. Cloner le dépôt
```bash
git clone https://github.com/delnixcode/Shelfreader.git
cd Shelfreader/p1-MVP-Desktop
```

#### 2. Activer l'environnement virtuel
```bash
# Linux/macOS
source env-p1/bin/activate
# Windows
env-p1\Scripts\activate
```

#### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

#### 4. Lancer l'application
```bash
streamlit run src/app.py
```

Ouvrir http://localhost:8501 dans votre navigateur.

## 🎯 **Deux façons d'utiliser ShelfReader**

### **💻 Mode Ligne de commande** (Pour développeurs/experts)
Utilisez directement les moteurs OCR depuis le terminal :
```bash
# Moteur EasyOCR (recommandé)
python src/ocr_easyocr.py test_images/books1.jpg --gpu --confidence 0.3

# Moteur Tesseract (rapide)
python src/ocr_tesseract.py test_images/books1.jpg

# Moteur TrOCR (haute précision)
python src/ocr_trocr.py test_images/books1.jpg --gpu
```

### **🖥️ Mode Interface Web** (Pour débutants)
Interface Streamlit intuitive avec upload et visualisation :
```bash
streamlit run src/app.py
# Puis ouvrir http://localhost:8501
```

## 🚀 Utilisation détaillée

### 💻 Mode Ligne de commande (Experts)

#### Moteurs OCR disponibles :
```bash
# EasyOCR (recommandé - précision 93%)
python src/ocr_easyocr.py test_images/books1.jpg --gpu --confidence 0.3

# Tesseract (ultra rapide)
python src/ocr_tesseract.py test_images/books1.jpg

# TrOCR (haute précision)
python src/ocr_trocr.py test_images/books1.jpg --gpu
```

#### 📁 Sauvegarde automatique des résultats
Les résultats OCR sont automatiquement sauvegardés dans le dossier **`result-ocr/`** :
- Fichiers texte avec les titres détectés
- Images annotées avec les bounding boxes
- Métriques de performance et statistiques

#### Options communes :
- `--gpu` : Accélération GPU (recommandé)
- `--confidence 0.3` : Seuil de confiance (0.1-1.0)
- `--output fichier.txt` : Sauvegarde résultats personnalisée

### 🖥️ Mode Interface Web (Débutants)

```bash
streamlit run src/app.py
# Ouvrir http://localhost:8501
```

#### Fonctionnalités :
- Upload d'images par glisser-déposer
- Choix du moteur OCR
- Comparaison multi-moteurs (page dédiée)
- Visualisations avec bounding boxes

### 💡 Conseils pour les images

- **Qualité** : Bien éclairées, perpendiculaires à l'étagère
- **Taille** : Minimum 1000px de largeur
- **Formats** : JPG, PNG
- **Contenu** : Titres de livres visibles

### ⚡ Performance par moteur

| Moteur | Précision | Vitesse | GPU |
|--------|-----------|---------|-----|
| EasyOCR | 93.3% | 3-5s | ✅ |
| Tesseract | 73.3% | 1-2s | ❌ |
| TrOCR | 80.7% | 8-15s | ✅ |

## 🚀 Démarrage rapide

```bash
# Cloner le projet
git clone https://github.com/delnixcode/Shelfreader.git
cd Shelfreader/p1-MVP-Desktop

# Activer l'environnement virtuel
source env-p1/bin/activate  # Linux/macOS
# ou
env-p1\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Choisir votre mode :
# Mode ligne de commande
python src/ocr_easyocr.py test_images/books1.jpg --gpu

# OU mode interface web
streamlit run src/app.py
```

## 🏗️ Architecture du projet

ShelfReader P1 utilise une **architecture modulaire** permettant le développement et le test indépendants de chaque composant OCR.

### Structure des dossiers
```
p1-MVP-Desktop/
├── src/                          # Code source principal
│   ├── __init__.py              # Package Python
│   ├── api_client.py            # Client API Open Library
│   ├── app.py                   # Interface Streamlit
│   ├── ocr_easyocr.py           # Module OCR EasyOCR
│   ├── ocr_tesseract.py         # Module OCR Tesseract
│   └── ocr_trocr.py             # Module OCR TrOCR
├── scripts/                      # Scripts utilitaires
│   └── ocr_detect.py            # Script de détection unifié
├── docs/                         # Documentation complète
│   ├── README.md                # Guide utilisateur
│   ├── P1_Architecture_Documentation.md # Architecture & Documentation
│   ├── P1_Status_Report.md      # État d'avancement & métriques
│   ├── Testing_Guide.md         # Guide des tests
│   ├── Dependencies.md          # Gestion dépendances
│   └── OCR_Code_Explanation.md  # Explication technique OCR
├── tests/                        # Tests unitaires
│   └── __init__.py              # Package de tests
├── test_images/                  # Images de test
│   ├── books1.jpg
│   └── books2.jpg
├── requirements.txt             # Dépendances Python
└── TODO.md                      # Liste des tâches
```

### Technologies utilisées

| Composant | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| **OCR Engine** | EasyOCR | 1.7+ | Reconnaissance optique de caractères |
| **Computer Vision** | OpenCV | 4.8+ | Traitement d'images et preprocessing |
| **Deep Learning** | PyTorch | 2.0+ | Backend EasyOCR (GPU support) |
| **API Client** | requests | 2.31+ | HTTP client pour Open Library API |
| **Interface** | Streamlit | 1.28+ | UI web pour upload et résultats |
| **Image Processing** | Pillow | 10.0+ | Gestion des formats d'images |

## 📈 **Évolution du projet**

### **Phase 1 : Moteurs OCR** ✅
- Implémentation EasyOCR, Tesseract, TrOCR
- Utilisation en ligne de commande
- Support GPU automatique

### **Phase 2 : Enrichissement** ✅
- Intégration Open Library
- Métadonnées des livres
- Liens vers informations complètes

### **Phase 3 : Interface Web** ✅
- Application Streamlit moderne
- Upload intuitif d'images
- Comparaison multi-moteurs
- Visualisations avancées

## ✨ Fonctionnalités principales
- 📤 **Upload intuitif** d'images
- ⚙️ **Paramètres avancés** (moteurs OCR, seuil de confiance, GPU)
- 📊 **Résultats détaillés** avec métriques et tableaux
- 👁️ **Visualisation des zones détectées**
- 🔍 **Comparaison multi-moteurs OCR** (nouvelle page)
- 📚 **Enrichissement Open Library** (optionnel)

## 🎯 Algorithme optimisé
- **Précision mesurée** : 93% (14/15 livres)
- **Détection adaptative multi-échelle**
- **Support GPU automatique**
- **3 moteurs OCR** : EasyOCR, Tesseract, TrOCR

## 📚 Documentation

- [🏗️ Architecture & Documentation](docs/P1_Architecture_Documentation.md) - Vue d'ensemble complète du projet
- [🔧 Dépendances](docs/Dependencies.md) - Gestion des dépendances détaillée
- [📖 Guide OCR](docs/OCR_Code_Explanation.md) - Explication technique du code OCR

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- Ouvrir une issue pour signaler un bug
- Proposer une amélioration via une Pull Request
- Partager vos idées dans les discussions

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

*Développé avec ❤️ pour les amoureux des livres*

Pour plus d'informations : [GitHub Issues](https://github.com/delnixcode/Shelfreader/issues)elfReader P1 - MVP Desktop**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![EasyOCR](https://img.shields.io/badge/EasyOCR-1.7+-green.svg)](https://github.com/JaidedAI/EasyOCR)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Reconnaissance automatique de livres sur étagères avec OCR intelligent**

## � Installation

### Prérequis
- Python 3.8+
- pip
- Un GPU (optionnel, recommandé)

### Étapes

#### 1. Cloner le dépôt
```bash
git clone https://github.com/delnixcode/Shelfreader.git
cd Shelfreader/p1-MVP-Desktop
```

#### 2. Activer l'environnement virtuel
```bash
# Linux/macOS
source env-p1/bin/activate
# Windows
env-p1\Scripts\activate
```

#### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

#### 4. Lancer l'application
```bash
streamlit run src/app.py
```

Ouvrir http://localhost:8501 dans votre navigateur.

## 🎯 **Deux façons d'utiliser ShelfReader**

### **� Mode Ligne de commande** (Pour développeurs/experts)
Utilisez directement les moteurs OCR depuis le terminal :
```bash
# Moteur EasyOCR (recommandé)
python src/ocr_easyocr.py test_images/books1.jpg --gpu --confidence 0.3

# Moteur Tesseract (rapide)
python src/ocr_tesseract.py test_images/books1.jpg

# Moteur TrOCR (haute précision)
python src/ocr_trocr.py test_images/books1.jpg --gpu
```

## 🚀 Utilisation détaillée

### � Mode Ligne de commande (Experts)

#### Moteurs OCR disponibles :
```bash
# EasyOCR (recommandé - précision 93%)
python src/ocr_easyocr.py test_images/books1.jpg --gpu --confidence 0.3

# Tesseract (ultra rapide)
python src/ocr_tesseract.py test_images/books1.jpg

# TrOCR (haute précision)
python src/ocr_trocr.py test_images/books1.jpg --gpu
```

#### Options communes :
- `--gpu` : Accélération GPU (recommandé)
- `--confidence 0.3` : Seuil de confiance (0.1-1.0)
- `--output fichier.txt` : Sauvegarde résultats

### 🖥️ Mode Interface Web (Débutants)

```bash
streamlit run src/app.py
# Ouvrir http://localhost:8501
```

#### Fonctionnalités :
- Upload d'images par glisser-déposer
- Choix du moteur OCR
- Comparaison multi-moteurs (page dédiée)
- Visualisations avec bounding boxes

### 💡 Conseils pour les images

- **Qualité** : Bien éclairées, perpendiculaires à l'étagère
- **Taille** : Minimum 1000px de largeur
- **Formats** : JPG, PNG
- **Contenu** : Titres de livres visibles

### ⚡ Performance par moteur

| Moteur | Précision | Vitesse | GPU |
|--------|-----------|---------|-----|
| EasyOCR | 93.3% | 3-5s | ✅ |
| Tesseract | 73.3% | 1-2s | ❌ |
| TrOCR | 80.7% | 8-15s | ✅ |

## �🚀 Démarrage rapide

```bash
# Cloner le projet
git clone https://github.com/delnixcode/Shelfreader.git
cd Shelfreader/p1-MVP-Desktop

# Activer l'environnement virtuel
source env-p1/bin/activate  # Linux/macOS
# ou
env-p1\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Choisir votre mode :
# Mode ligne de commande
python src/ocr_easyocr.py test_images/books1.jpg --gpu

# OU mode interface web
streamlit run src/app.py
```

## 📈 **Évolution du projet**

### **Phase 1 : Moteurs OCR** ✅
- Implémentation EasyOCR, Tesseract, TrOCR
- Utilisation en ligne de commande
- Support GPU automatique

### **Phase 2 : Enrichissement** ✅
- Intégration Open Library
- Métadonnées des livres
- Liens vers informations complètes

### **Phase 3 : Interface Web** ✅
- Application Streamlit moderne
- Upload intuitif d'images
- Comparaison multi-moteurs
- Visualisations avancées

## ✨ Fonctionnalités principales
- 📤 **Upload intuitif** d'images
- ⚙️ **Paramètres avancés** (moteurs OCR, seuil de confiance, GPU)
- 📊 **Résultats détaillés** avec métriques et tableaux
- 👁️ **Visualisation des zones détectées**
- 🔍 **Comparaison multi-moteurs OCR** (nouvelle page)
- 📚 **Enrichissement Open Library** (optionnel)

## 🎯 Algorithme optimisé
- **Précision mesurée** : 93% (14/15 livres)
- **Détection adaptative multi-échelle**
- **Support GPU automatique**
- **3 moteurs OCR** : EasyOCR, Tesseract, TrOCR

---

*Développé avec ❤️ pour les amoureux des livres*

Pour plus d'informations : [GitHub Issues](https://github.com/delnixcode/Shelfreader/issues)