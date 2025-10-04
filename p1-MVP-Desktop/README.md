# 🏗️ **P1 - MVP Desktop**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![EasyOCR](https://img.shields.io/badge/EasyOCR-1.7+-green.svg)](https://github.com/JaidedAI/EasyOCR)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

### 📋 **Table des Matières**
- [🎯 Vue d'ensemble](#-vue-densemble)
- [🚀 Installation](#-installation)
- [⚡ Démarrage rapide](#-démarrage-rapide)
- [💻 Utilisation détaillée](#-utilisation-détaillée)
- [🏗️ Architecture](#️-architecture)
- [📁 Structure du projet](#-structure-du-projet)
- [🎨 Interface Web](#-interface-web)
- [📊 Résultats & Métriques](#-résultats--métriques)
- [🧪 Tests](#-tests)
- [🔧 Dépannage](#-dépannage)
- [📚 API & Dépendances](#-api--dépendances)
- [❓ FAQ](#-faq)
- [🤝 Contribution](#-contribution)
- [📈 Roadmap P1](#-roadmap-p1)
- [📞 Support](#-support)

---

## 🎯 **Vue d'ensemble**

**ShelfReader P1** est la première phase d'une application multi-étapes pour la reconnaissance automatique de livres sur des étagères via OCR (Optical Character Recognition) et intelligence artificielle.

### **Objectif Principal**
Détecter et identifier automatiquement les titres de livres sur des photos d'étagères, avec enrichissement des données via des APIs externes pour obtenir des informations détaillées sur chaque livre (auteur, résumé, couverture, etc.).

### **Cas d'usage**
- 📚 **Bibliophiles** : Inventorier sa bibliothèque personnelle
- 🏪 **Libraires** : Gestion rapide des stocks
- 📖 **Étudiants** : Recherche de livres dans les bibliothèques
- 🏛️ **Institutions** : Catalogage automatique de collections

---

## 🚀 **Installation**

### **Prérequis Système**
- **Python** : 3.8 ou supérieur
- **RAM** : Minimum 4GB, recommandé 8GB+
- **GPU** : NVIDIA avec CUDA (optionnel, accélère l'OCR)
- **OS** : Linux, macOS, Windows

### **Installation automatique**
```bash
# Cloner le repository
git clone https://github.com/delnixcode/Shelfreader.git
cd Shelfreader/p1-MVP-Desktop

# Activer l'environnement virtuel
source env-p1/bin/activate  # Linux/macOS
# ou env-p1\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### **Vérification de l'installation**
```bash
# Tester Python
python --version  # Doit afficher Python 3.8+

# Tester les imports principaux
python -c "import easyocr, torch, streamlit; print('✅ OK')"

# Tester GPU (optionnel)
python -c "import torch; print('GPU:', torch.cuda.is_available())"
```

---

## ⚡ **Démarrage rapide**

### **3 étapes pour commencer**
```bash
# 1. Activer l'environnement virtuel
source env-p1/bin/activate

# 2. Tester avec une image d'exemple
python ocr_easyocr.py test_images/books1.jpg --gpu

# 3. Lancer l'interface web (optionnel)
streamlit run app.py
```

**Résultat attendu** : Un fichier `result-ocr/easyocr_results.txt` contenant les titres de livres détectés.

---

## 💻 **Utilisation détaillée**

### **Commandes de Base**

#### **Traitement d'une image avec EasyOCR**
```bash
# Analyse basique
python ocr_easyocr.py test_images/books1.jpg

# Avec GPU (recommandé)
python ocr_easyocr.py test_images/books1.jpg --gpu

# Avec seuil de confiance personnalisé
python ocr_easyocr.py test_images/books1.jpg --confidence 0.3

# Mode verbeux (détails complets)
python ocr_easyocr.py test_images/books1.jpg --verbose
```

#### **Utilisation des autres moteurs**
```bash
# Tesseract (rapide, CPU uniquement)
python ocr_tesseract.py test_images/books1.jpg

# TrOCR (haute précision, GPU recommandé)
python ocr_trocr.py test_images/books1.jpg --gpu
```

### **Options Avancées**

#### **Paramètres de Configuration**
```bash
# Liste complète des options
python ocr_easyocr.py --help

# Exemples d'options avancées
python ocr_easyocr.py image.jpg \
  --confidence 0.2 \
  --gpu \
  --output-format json \
  --save-annotated
```

#### **Traitement par Lot**
```bash
# Traiter toutes les images d'un dossier
for img in test_images/*.jpg; do
  python ocr_easyocr.py "$img" --gpu
done

# Avec sauvegarde des résultats
mkdir -p results_batch
for img in test_images/*.jpg; do
  python ocr_easyocr.py "$img" --gpu --output-dir results_batch
done
```

### **Formats de Sortie**

#### **Fichier Texte (.txt)**
```
=== RÉSULTATS OCR ===
Titre détecté: "LE PETIT PRINCE"
Confiance: 0.892
Position: x=45, y=120

Titre détecté: "HARRY POTTER"
Confiance: 0.756
Position: x=45, y=160
```

#### **Format JSON**
```json
{
  "image": "books1.jpg",
  "timestamp": "2025-01-04T12:34:56",
  "engine": "EasyOCR",
  "results": [
    {
      "text": "LE PETIT PRINCE",
      "confidence": 0.892,
      "bbox": [45, 120, 180, 25]
    }
  ]
}
```

---

## 🏗️ **Architecture**

### **OCR Multi-Moteurs**
- 🔍 **EasyOCR** : Moteur principal (GPU/CPU, précision élevée)
- ⚡ **Tesseract** : Moteur rapide (CPU uniquement, vitesse optimale)
- 🎯 **TrOCR** : Moteur haute précision (GPU recommandé, IA avancée)

### **Interface Utilisateur**
- 🌐 **Web App** : Interface Streamlit moderne et intuitive
- 📱 **Responsive** : Fonctionne sur desktop et mobile
- 🎨 **Visualisation** : Aperçu des images avec zones détectées

### **Enrichissement de Données**
- � **Open Library API** : Métadonnées complètes des livres
- 🔗 **ISBN Detection** : Recherche par numéro ISBN
- 📊 **Statistiques** : Métriques de confiance et performance

### **Gestion des Résultats**
- 💾 **Sauvegarde automatique** : Dossier `result-ocr/` organisé
- 📄 **Formats multiples** : JSON, TXT, CSV
- 📈 **Historique** : Traçabilité des analyses

---

## 📁 **Structure du projet**

```
p1-MVP-Desktop/
├── scripts/                 # Scripts OCR individuels
│   ├── ocr_easyocr.py      # Moteur EasyOCR
│   ├── ocr_tesseract.py    # Moteur Tesseract
│   └── ocr_trocr.py        # Moteur TrOCR
├── src/                    # Code source principal
│   ├── app.py              # Interface web Streamlit
│   ├── api_client.py       # Client Open Library API
│   ├── ocr_easyocr.py      # Classe EasyOCRProcessor
│   ├── ocr_tesseract.py    # Classe TesseractProcessor
│   └── ocr_trocr.py        # Classe TrOCRProcessor
├── tests/                  # Tests unitaires
│   ├── __init__.py
│   └── test_*.py
├── test_images/            # Images de test
│   ├── books1.jpg
│   └── books2.jpg
├── result-ocr/             # Résultats générés (auto-créé)
├── env-p1/                 # Environnement virtuel
├── requirements.txt        # Dépendances Python
├── pyrightconfig.json      # Configuration Pyright
└── README.md              # Cette documentation
```

### **Flux de Données**
1. **Input** : Image JPG/PNG d'étagère de livres
2. **OCR Processing** : Extraction du texte avec moteur choisi
3. **Filtrage** : Application du seuil de confiance
4. **Enrichissement** : Recherche métadonnées via API
5. **Output** : Sauvegarde résultats + affichage interface

---

## 🎨 **Interface Web**

### **Démarrage**
```bash
streamlit run app.py
```
Puis ouvrir http://localhost:8501 dans votre navigateur.

### **Fonctionnalités de l'Interface**
- 📤 **Upload d'images** : Glisser-déposer ou sélection de fichiers
- ⚙️ **Configuration OCR** : Choix du moteur, paramètres de confiance
- 👁️ **Visualisation** : Aperçu des zones détectées
- 📊 **Résultats** : Affichage structuré des textes extraits
- 💾 **Export** : Téléchargement des résultats (JSON/TXT)

### **Captures d'écran**
*L'interface propose une expérience utilisateur intuitive avec :*
- Formulaire de configuration simple
- Aperçu temps réel des images
- Tableaux de résultats organisés
- Métriques de performance

---

## 📊 **Résultats & Métriques**

### **Format des Résultats**
Chaque analyse génère automatiquement un fichier dans `result-ocr/` :

```
=== RÉSULTATS OCR - test_images/books1.jpg ===
Date: 2025-10-04 12:34:56
Moteur: EasyOCR (GPU)
Nombre de textes détectés: 11
Confiance moyenne: 0.885
Temps de traitement: 3.2s

TEXTE COMPLET:
[Titre Livre 1] | [Titre Livre 2] | [Titre Livre 3] | ...

DÉTAIL PAR TEXTE:
--- Texte 1 ---
Confiance: 0.703
Texte: "LE PETIT PRINCE"
Position: x=45, y=120, w=180, h=25

--- Texte 2 ---
Confiance: 0.892
Texte: "HARRY POTTER"
Position: x=45, y=160, w=195, h=28

[... suite pour tous les textes ...]
```

### **Métriques de Performance**

#### **Benchmarks sur `test_images/books1.jpg`**

| Moteur | Textes Détectés | Confiance Moyenne | Temps | GPU Support |
|--------|-----------------|-------------------|-------|-------------|
| **EasyOCR** | 11 | 0.885 | ~3-5s | ✅ Excellent |
| **Tesseract** | 15 | 0.733 | ~1.5s | ❌ Aucun |
| **TrOCR** | 14 | 0.807 | ~8-15s | ✅ Bon |

#### **Interprétation des Métriques**
- **Confiance** : Probabilité que le texte détecté soit correct (0.0-1.0)
- **Temps** : Durée totale de l'analyse
- **Textes détectés** : Nombre de zones de texte trouvées

### **Optimisation des Résultats**

#### **Réglage du Seuil de Confiance**
```bash
# Très tolérant (beaucoup de résultats)
python ocr_easyocr.py image.jpg --confidence 0.1

# Équilibre recommandé
python ocr_easyocr.py image.jpg --confidence 0.2

# Strict (haute précision)
python ocr_easyocr.py image.jpg --confidence 0.5

# Très strict (seulement les meilleurs)
python ocr_easyocr.py image.jpg --confidence 0.7
```

#### **Choix du Moteur par Cas d'Usage**
- **📚 Tests rapides** → Tesseract (`--confidence 0.3`)
- **🏭 Production** → EasyOCR (`--gpu --confidence 0.2`)
- **🔬 Recherche** → TrOCR (`--gpu --confidence 0.7`)

---

## 🧪 **Tests**

### **Problèmes Courants**

#### **❌ Erreur GPU/CUDA**
```
RuntimeError: CUDA out of memory
```
**Solutions :**
```bash
# Désactiver GPU temporairement
python ocr_easyocr.py image.jpg  # Sans --gpu

# Réduire la taille d'image
# Ou installer CUDA correctement
```

#### **❌ Import Error**
```
ModuleNotFoundError: No module named 'easyocr'
```
**Solutions :**
```bash
# Réactiver environnement virtuel
source env-p1/bin/activate

# Réinstaller dépendances
pip install -r requirements.txt
```

#### **❌ Pas de texte détecté**
**Solutions :**
```bash
# Baisser le seuil de confiance
python ocr_easyocr.py image.jpg --confidence 0.1

# Vérifier la qualité de l'image
# Essayer un autre moteur OCR
python ocr_tesseract.py image.jpg
```

### **Logs et Debug**
```bash
# Activer logs détaillés
export PYTHONPATH=$PYTHONPATH:.
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
# Votre code OCR ici
"
```

### **Vérifications Système**
```bash
# Vérifier Python
python --version

# Vérifier GPU
python -c "import torch; print('CUDA:', torch.cuda.is_available())"

# Vérifier espace disque
df -h

# Vérifier RAM
free -h
```

---

## 📚 **API & Dépendances**

### **APIs Externes**

#### **Open Library API**
- **URL** : https://openlibrary.org/developers/api
- **Usage** : Enrichissement métadonnées livres
- **Limites** : 100 requêtes/minute
- **Format** : JSON

```python
# Exemple d'utilisation
from api_client import OpenLibraryClient
client = OpenLibraryClient()
book_data = client.search_book("Le Petit Prince")
```

### **Dépendances Python**

| Package | Version | Usage |
|---------|---------|-------|
| `easyocr` | 1.7+ | OCR principal |
| `pytesseract` | 0.3+ | OCR Tesseract |
| `transformers` | 4.21+ | TrOCR |
| `torch` | 1.12+ | PyTorch |
| `streamlit` | 1.28+ | Interface web |
| `requests` | 2.28+ | API HTTP |
| `Pillow` | 9.3+ | Traitement images |

### **Installation des Dépendances**
```bash
# Installation complète
pip install -r requirements.txt

# Installation sélective
pip install easyocr torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## ❓ **FAQ**

### **🤔 Quel moteur OCR choisir ?**
- **EasyOCR** : Équilibre parfait précision/vitesse, recommandé pour débuter
- **Tesseract** : Ultra rapide, parfait pour tests ou CPU limité
- **TrOCR** : Maximum précision, recommandé pour production critique

### **💻 GPU obligatoire ?**
- **Non** : Tous les moteurs fonctionnent en CPU
- **Recommandé** : GPU accélère considérablement EasyOCR et TrOCR
- **Conseil** : Testez d'abord en CPU, activez GPU pour production

### **�� Formats d'images supportés ?**
- **JPG/JPEG** ✅
- **PNG** ✅
- **BMP** ✅
- **TIFF** ✅
- **Conseil** : JPG de bonne qualité (minimum 1000px largeur)

### **⚡ Performance attendue ?**
- **Tesseract** : ~1-2 secondes
- **EasyOCR CPU** : ~5-10 secondes
- **EasyOCR GPU** : ~2-5 secondes
- **TrOCR CPU** : ~15-30 secondes
- **TrOCR GPU** : ~5-15 secondes

### **💾 Taille des résultats ?**
- **Fichiers texte** : ~1-5KB par analyse
- **Images traitées** : Taille originale préservée
- **Base de données** : Non implémentée (P1 = fichiers plats)

### **🌐 Connexion internet ?**
- **OCR local** : Fonctionne hors ligne
- **Enrichissement** : Nécessite internet pour Open Library API
- **Interface web** : Fonctionne en local

---

## 🤝 **Contribution**

### **Signaler un Bug**
1. Vérifier que le bug n'est pas déjà reporté
2. Créer une issue avec :
   - Description détaillée
   - Étapes de reproduction
   - Logs d'erreur
   - Version Python/OS

### **Proposer une Amélioration**
1. Créer une issue décrivant la fonctionnalité
2. Discuter avec la communauté
3. Implémenter si approuvé

### **Développement Local**
```bash
# Fork le repository
# Cloner votre fork
git clone https://github.com/YOUR_USERNAME/Shelfreader.git

# Créer une branche
git checkout -b feature/nouvelle-fonctionnalite

# Commiter vos changements
git commit -m "Ajout: Nouvelle fonctionnalité"

# Push et créer une PR
git push origin feature/nouvelle-fonctionnalite
```

### **Standards de Code**
- **PEP 8** : Style Python
- **Type hints** : Annotations de types
- **Docstrings** : Documentation des fonctions
- **Tests** : Couverture minimum 80%

---

## 📈 **Roadmap P1**

### **✅ Implémenté**
- [x] OCR multi-moteurs (EasyOCR, Tesseract, TrOCR)
- [x] Interface web Streamlit
- [x] API Open Library
- [x] Sauvegarde automatique des résultats
- [x] Tests unitaires
- [x] Documentation complète

### **🔄 En Cours**
- [ ] Amélioration précision OCR
- [ ] Interface desktop native (PyQt/Tkinter)
- [ ] Base de données locale
- [ ] Export PDF/Excel

### **📋 Planifié**
- [ ] Mode batch (traitement multiple)
- [ ] API REST interne
- [ ] Interface mobile responsive
- [ ] Synchronisation cloud

---

## 📞 **Support**

- **📧 Email** : [votre.email@exemple.com]
- **🐛 Issues** : [GitHub Issues](https://github.com/delnixcode/Shelfreader/issues)
- **📖 Wiki** : [Documentation complète](https://github.com/delnixcode/Shelfreader/wiki)

---
