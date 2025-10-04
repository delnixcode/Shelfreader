# 🏗️ **P1 - MVP Desktop**
## OCR + API + Interface Web

**ShelfReader MVP Desktop** - Extraire du texte des photos de tranches de livres avec intelligence artificielle.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![EasyOCR](https://img.shields.io/badge/EasyOCR-1.7+-green.svg)](https://github.com/JaidedAI/EasyOCR)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 **Table des Matières**
- [🎯 Vue d'ensemble](#-vue-densemble)
- [✨ Fonctionnalités](#-fonctionnalités)
- [🏗️ Architecture](#️-architecture)
- [📁 Structure du projet](#-structure-du-projet)
- [🚀 Installation](#-installation)
- [💻 Utilisation](#-utilisation)
- [🎨 Interface Web](#-interface-web)
- [📊 Résultats & Métriques](#-résultats--métriques)
- [🧪 Tests](#-tests)
- [🔧 Dépannage](#-dépannage)
- [📚 API & Dépendances](#-api--dépendances)
- [❓ FAQ](#-faq)
- [🤝 Contribution](#-contribution)

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

## ✨ **Fonctionnalités**

### **OCR Multi-Moteurs**
- 🔍 **EasyOCR** : Moteur principal (GPU/CPU, précision élevée)
- ⚡ **Tesseract** : Moteur rapide (CPU uniquement, vitesse optimale)
- 🎯 **TrOCR** : Moteur haute précision (GPU recommandé, IA avancée)

### **Interface Utilisateur**
- 🌐 **Web App** : Interface Streamlit moderne et intuitive
- 📱 **Responsive** : Fonctionne sur desktop et mobile
- 🎨 **Visualisation** : Aperçu des images avec zones détectées

### **Enrichissement de Données**
- 📖 **Open Library API** : Métadonnées complètes des livres
- 🔗 **ISBN Detection** : Recherche par numéro ISBN
- 📊 **Statistiques** : Métriques de confiance et performance

### **Gestion des Résultats**
- 💾 **Sauvegarde automatique** : Dossier `result-ocr/` organisé
- 📄 **Formats multiples** : JSON, TXT, CSV
- 📈 **Historique** : Traçabilité des analyses

---

## 🏗️ **Architecture**

```
📁 P1-MVP-Desktop/
├── 🔧 Scripts OCR (ocr_*.py)
│   ├── ocr_easyocr.py     # Moteur principal
│   ├── ocr_tesseract.py   # Moteur rapide
│   └── ocr_trocr.py       # Moteur précision
├── 🌐 Interface Web
│   └── app.py            # Application Streamlit
├── 🔗 API Clients
│   └── api_client.py     # Open Library API
├── 📊 Résultats
│   └── result-ocr/       # Sorties automatiques
└── 🧪 Tests
    └── tests/            # Suite de tests
```

### **Flux de données**
1. **Input** : Photo d'étagère (JPG/PNG)
2. **OCR** : Extraction du texte par IA
3. **Filtrage** : Seuil de confiance configurable
4. **Enrichissement** : APIs externes (Open Library)
5. **Output** : Résultats structurés + interface web

---

## 📁 **Structure du projet**

```
p1-MVP-Desktop/
├── 📂 env-p1/              # Environnement virtuel Python
├── 📂 result-ocr/          # Résultats OCR (auto-généré)
│   ├── easyocr_results.txt
│   ├── tesseract_results.txt
│   └── trocr_results.txt
├── 🔧 ocr_easyocr.py       # Script OCR EasyOCR (principal)
├── 🔧 ocr_tesseract.py     # Script OCR Tesseract (rapide)
├── 🔧 ocr_trocr.py         # Script OCR TrOCR (précis)
├── 🔗 api_client.py        # Client API Open Library
├── 🌐 app.py               # Interface web Streamlit
├── 🖼️ test_images/         # Images de test
│   ├── books1.jpg
│   └── books2.jpg
├── 📋 requirements.txt     # Dépendances Python
├── 📋 README.md           # Cette documentation
└── 🧪 tests/              # Tests unitaires
    ├── __init__.py
    └── test_*.py
```

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

## 💻 **Utilisation**

### **🚀 Démarrage Rapide**
```bash
# Activer l'environnement
source env-p1/bin/activate

# Test simple avec EasyOCR
python ocr_easyocr.py test_images/books1.jpg --gpu

# Interface web
streamlit run app.py
```

### **📋 Arguments et Options Détaillés**

#### **Syntaxe Générale**
```bash
python [script_ocr].py [image] [options]
```

#### **Arguments Positionnels**
- `image` : Chemin vers l'image à analyser (obligatoire)
  - Formats supportés : JPG, PNG, BMP, TIFF
  - Exemples : `test_images/books1.jpg`, `photos/etagere.jpg`, `/chemin/absolu/image.png`

#### **Options Communes à Tous les Scripts**
| Option | Type | Défaut | Description | Exemple |
|--------|------|--------|-------------|---------|
| `--gpu` | flag | `False` | Utiliser GPU NVIDIA (accélère EasyOCR/TrOCR) | `--gpu` |
| `--confidence X.X` | float | `0.2` | Seuil de confiance (0.0-1.0) | `--confidence 0.5` |
| `--output FILE` | string | `[moteur]_results.txt` | Fichier de sortie personnalisé | `--output mes_livres.txt` |
| `--lang CODE` | string | `eng` | Langue pour Tesseract uniquement | `--lang fra` |

#### **Valeurs du Seuil de Confiance**
- `0.1` : **Très tolérant** - Beaucoup de résultats, plus de faux positifs
- `0.2` : **Équilibre recommandé** - Bon compromis pour débuter
- `0.3` : **Moyen** - Moins de bruit, bonne précision
- `0.5` : **Strict** - Résultats fiables, moins de détections
- `0.7` : **Très strict** - Seulement les meilleurs résultats

### **🔧 Scripts OCR Individuels - Utilisation Directe**

#### **🔍 EasyOCR (Recommandé - GPU/CPU)**
```bash
# USAGE DE BASE (sans options)
python ocr_easyocr.py test_images/books1.jpg

# AVEC GPU (recommandé - accélère considérablement)
python ocr_easyocr.py test_images/books1.jpg --gpu

# SEUIL DE CONFIANCE PERSONNALISÉ
python ocr_easyocr.py test_images/books1.jpg --gpu --confidence 0.3

# FICHIER DE SORTIE PERSONNALISÉ
python ocr_easyocr.py test_images/books1.jpg --gpu --output mes_resultats_easyocr.txt

# COMBINAISON COMPLÈTE
python ocr_easyocr.py test_images/books1.jpg --gpu --confidence 0.4 --output analyse_etagere.txt

# EXEMPLES AVANCÉS
python ocr_easyocr.py photos/ma_bibliotheque.jpg --gpu --confidence 0.2
python ocr_easyocr.py /home/user/images/livres_scan.jpg --gpu --confidence 0.5 --output scan_bibliotheque.txt
```

#### **⚡ Tesseract (Rapide - CPU seulement)**
```bash
# USAGE DE BASE (CPU uniquement, très rapide)
python ocr_tesseract.py test_images/books1.jpg

# AVEC LANGUE FRANÇAISE
python ocr_tesseract.py test_images/books1.jpg --lang fra

# AVEC LANGUE ALLEMANDE
python ocr_tesseract.py test_images/books1.jpg --lang deu

# SEUIL DE CONFIANCE ÉLEVÉ (moins de faux positifs)
python ocr_tesseract.py test_images/books1.jpg --confidence 0.5

# FICHIER DE SORTIE PERSONNALISÉ
python ocr_tesseract.py test_images/books1.jpg --output tesseract_rapide.txt

# COMBINAISON COMPLÈTE
python ocr_tesseract.py test_images/books1.jpg --lang eng --confidence 0.4 --output scan_anglais.txt

# EXEMPLES AVANCÉS
python ocr_tesseract.py photos/livres_francais.jpg --lang fra --confidence 0.3
python ocr_tesseract.py images/bibliotheque_allemande.jpg --lang deu --confidence 0.5 --output livres_de.txt
```

#### **🎯 TrOCR (Haute Précision - GPU recommandé)**
```bash
# USAGE DE BASE
python ocr_trocr.py test_images/books1.jpg

# AVEC GPU (recommandé pour les performances)
python ocr_trocr.py test_images/books1.jpg --gpu

# HAUTE PRÉCISION (seuil strict)
python ocr_trocr.py test_images/books1.jpg --gpu --confidence 0.7

# SEUIL MOYEN (bon équilibre)
python ocr_trocr.py test_images/books1.jpg --gpu --confidence 0.5

# FICHIER DE SORTIE PERSONNALISÉ
python ocr_trocr.py test_images/books1.jpg --gpu --output trocr_precision.txt

# COMBINAISON COMPLÈTE
python ocr_trocr.py test_images/books1.jpg --gpu --confidence 0.6 --output haute_precision.txt

# EXEMPLES AVANCÉS
python ocr_trocr.py photos/textes_difficiles.jpg --gpu --confidence 0.8 --output textes_complexes.txt
python ocr_trocr.py images/livres_anciens.jpg --gpu --confidence 0.7 --output livres_anciens.txt
```

### **📊 Comparaisons Pratiques**

#### **Par Usage**
```bash
# 🧪 TESTS RAPIDES (Tesseract - CPU seulement)
python ocr_tesseract.py image.jpg --confidence 0.3

# 🏭 PRODUCTION STANDARD (EasyOCR + GPU)
python ocr_easyocr.py image.jpg --gpu --confidence 0.2

# 🔬 PRÉCISION MAXIMALE (TrOCR + GPU)
python ocr_trocr.py image.jpg --gpu --confidence 0.7
```

#### **Par Performance**
```bash
# ⚡ LE PLUS RAPIDE (Tesseract)
python ocr_tesseract.py image.jpg

# 🚀 RAPIDE ET PRÉCIS (EasyOCR GPU)
python ocr_easyocr.py image.jpg --gpu

# 🐌 LE PLUS LENT MAIS ULTRA-PRÉCIS (TrOCR GPU)
python ocr_trocr.py image.jpg --gpu --confidence 0.7
```

### **🔄 Utilisation Avancée**

#### **Traitement par Lot (Bash)**
```bash
# Traiter toutes les images JPG du dossier
for img in test_images/*.jpg; do
    echo "=== Analyse de $(basename "$img") ==="
    python ocr_easyocr.py "$img" --gpu --confidence 0.3
done

# Avec noms de fichiers personnalisés
for img in photos/*.jpg; do
    filename=$(basename "$img" .jpg)
    python ocr_easyocr.py "$img" --gpu --output "resultats_${filename}.txt"
done
```

#### **Comparaison de Moteurs**
```bash
# Tester tous les moteurs sur la même image
IMAGE="test_images/books1.jpg"

echo "=== EASYOCR (GPU) ==="
python ocr_easyocr.py "$IMAGE" --gpu --confidence 0.2

echo "=== TESSERACT (CPU) ==="
python ocr_tesseract.py "$IMAGE" --confidence 0.3

echo "=== TROCR (GPU) ==="
python ocr_trocr.py "$IMAGE" --gpu --confidence 0.5
```

#### **Scripts Personnalisés**
```bash
# Script de traitement automatique
#!/bin/bash
IMAGE=$1
CONFIDENCE=${2:-0.2}

echo "Traitement de $IMAGE avec confiance $CONFIDENCE"
python ocr_easyocr.py "$IMAGE" --gpu --confidence "$CONFIDENCE" --output "auto_$(basename "$IMAGE" .jpg).txt"
```

### **📁 Gestion des Résultats**

#### **Dossier de Sortie Automatique**
```
result-ocr/
├── easyocr_results.txt      # Résultats EasyOCR par défaut
├── tesseract_results.txt    # Résultats Tesseract par défaut
├── trocr_results.txt        # Résultats TrOCR par défaut
└── [nom_personnalisé].txt   # Fichiers avec --output
```

#### **Format des Résultats Détaillé**
```
=== RÉSULTATS OCR - test_images/books1.jpg ===
Date: 2025-10-04 12:34:56
Moteur: EasyOCR (GPU)
Nombre de textes détectés: 11
Confiance moyenne: 0.885
Temps de traitement: 3.2s

TEXTE COMPLET:
[LE PETIT PRINCE] | [HARRY POTTER] | [1984] | ...

DÉTAIL PAR TEXTE:
--- Texte 1 ---
Confiance: 0.703
Texte: "LE PETIT PRINCE"
Position: x=45, y=120, w=180, h=25

--- Texte 2 ---
Confiance: 0.892
Texte: "HARRY POTTER"
Position: x=45, y=160, w=195, h=28

[... détails pour chaque texte détecté ...]
```

### **🎯 Recommandations d'Usage**

| Scénario | Script Recommandé | Arguments | Raison |
|----------|-------------------|-----------|---------|
| **Premiers tests** | `ocr_easyocr.py` | `--gpu --confidence 0.2` | Équilibre parfait |
| **Traitement rapide** | `ocr_tesseract.py` | `--confidence 0.3` | Ultra rapide |
| **Haute précision** | `ocr_trocr.py` | `--gpu --confidence 0.7` | Maximum de fiabilité |
| **CPU limité** | `ocr_tesseract.py` | `--lang fra --confidence 0.4` | Pas de GPU requis |
| **Images difficiles** | `ocr_trocr.py` | `--gpu --confidence 0.8` | IA avancée |
| **Traitement par lot** | `ocr_easyocr.py` | `--gpu --confidence 0.3` | Bon compromis |

---

## 🎨 **Interface Web**

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

### **Tests Unitaires**
```bash
# Activer l'environnement virtuel
source env-p1/bin/activate

# Lancer tous les tests
python -m pytest tests/

# Tests avec couverture de code
python -m pytest tests/ --cov=. --cov-report=html

# Tests verbeux
python -m pytest tests/ -v
```

### **Tests d'Intégration**
```bash
# Test complet pipeline OCR
python -c "
from ocr_easyocr import EasyOCRProcessor
processor = EasyOCRProcessor()
results = processor.process_image('test_images/books1.jpg')
print(f'Détecté {len(results)} textes')
"
```

### **Tests de Performance**
```bash
# Benchmark des moteurs
python -c "
import time
from ocr_easyocr import EasyOCRProcessor

start = time.time()
processor = EasyOCRProcessor()
results = processor.process_image('test_images/books1.jpg')
end = time.time()

print(f'EasyOCR: {len(results)} textes en {end-start:.2f}s')
"
```

---

## 🔧 **Dépannage**

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

### **📷 Formats d'images supportés ?**
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

**ShelfReader P1** - *De la photo d'étagère au catalogue intelligent* 📚🤖

---
*Dernière mise à jour : 4 octobre 2025*

### 🚀 **Installation**
```bash
cd p1-MVP-Desktop
source env-p1/bin/activate
pip install -r requirements.txt
```

### � **Utilisation**

#### **Scripts OCR individuels**
Chaque moteur OCR peut être utilisé indépendamment. **Les résultats sont automatiquement sauvegardés dans le dossier `result-ocr/`**.

##### **EasyOCR (Recommandé - GPU/CPU)**
```bash
# Test de base avec GPU (recommandé)
python ocr_easyocr.py test_images/books1.jpg --gpu

# Test avec CPU seulement
python ocr_easyocr.py test_images/books1.jpg

# Avec seuil de confiance personnalisé
python ocr_easyocr.py test_images/books1.jpg --gpu --confidence 0.3
```

##### **Tesseract (Rapide - CPU seulement)**
```bash
# Test de base (optimisé pour la vitesse ~1.5s)
python ocr_tesseract.py test_images/books1.jpg

# Avec langue française
python ocr_tesseract.py test_images/books1.jpg --lang fra

# Avec seuil de confiance plus élevé
python ocr_tesseract.py test_images/books1.jpg --confidence 0.5
```

##### **TrOCR (Précis - GPU recommandé)**
```bash
# Test avec GPU (recommandé pour les performances)
python ocr_trocr.py test_images/books1.jpg --gpu --confidence 0.5

# Test CPU (fonctionne mais plus lent)
python ocr_trocr.py test_images/books1.jpg --confidence 0.5

# Avec seuil de confiance plus strict
python ocr_trocr.py test_images/books1.jpg --gpu --confidence 0.7
```

#### **Options communes**
- `--gpu` : Utiliser le GPU (si disponible) - Accélère considérablement EasyOCR et TrOCR
- `--confidence X.X` : Seuil de confiance minimum (0.0 à 1.0) - Défaut: 0.2
  - `0.1` : Très tolérant (beaucoup de résultats, plus de faux positifs)
  - `0.2` : Équilibre (recommandé pour débuter)
  - `0.5` : Strict (moins de résultats, plus précis)
  - `0.7` : Très strict (seulement les meilleurs résultats)
- `--output fichier.txt` : Nom du fichier de sortie (défaut: `[moteur]_results.txt`)

#### **Options spécifiques par moteur**
- **EasyOCR** : `--gpu`, `--confidence`, `--output`
- **Tesseract** : `--lang [eng|fra|deu|...]`, `--confidence`, `--output`
- **TrOCR** : `--gpu`, `--confidence`, `--output`

### �️ **Interface Web**
```bash
streamlit run app.py
```

---

## 🎨 **Interface Web**

### 🧪 **Tests**
```bash
# Activer l'environnement virtuel d'abord
source env-p1/bin/activate

# Lancer tous les tests
python -m pytest tests/

# Tests avec couverture
python -m pytest tests/ --cov=. --cov-report=html
```

### 📊 **Comparaison des moteurs OCR**

| Moteur | GPU Support | Vitesse | Précision | Usage recommandé |
|--------|-------------|---------|-----------|------------------|
| **EasyOCR** | ✅ Excellent | 🚀 ~3-5s | 🟢🟢 Excellente | **Défaut - Tous usages** |
| **Tesseract** | ❌ Aucun | ⚡ ~1.5s | 🟡 Moyenne | Tests rapides, CPU limité |
| **TrOCR** | ✅ Bon | 🐌 ~8-15s | 🟢 Bonne | Précision maximale |

**📊 Benchmarks sur `test_images/books1.jpg` :**
- **EasyOCR** : 11 livres détectés, confiance 0.885, temps ~3s
- **Tesseract** : 15 textes détectés, confiance 0.733, temps ~1.5s  
- **TrOCR** : 14 textes détectés, confiance 0.807, temps ~12s

