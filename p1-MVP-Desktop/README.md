# 🏗️ **ShelfReader P1 - MVP Desktop**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![EasyOCR](https://img.shields.io/badge/EasyOCR-1.7+-green.svg)](https://github.com/JaidedAI/EasyOCR)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Reconnaissance automatique de livres sur étagères avec OCR intelligent**

---

## 📋 **Sommaire**

- [🎯 Qu'est-ce que ShelfReader ?](#-quest-ce-que-shelfreader-)
- [🚀 Installation (5 minutes)](#-installation-5-minutes)
- [⚡ Démarrage rapide (3 étapes)](#-démarrage-rapide-3-étapes)
- [💻 Comment utiliser](#-comment-utiliser)
- [🎨 Interface web](#-interface-web)
- [🔧 Options avancées](#-options-avancées)
- [🛠️ Dépannage](#️-dépannage)
- [❓ Questions fréquentes](#-questions-fréquentes)
- [📚 Informations techniques](#-informations-techniques)

---

## 🎯 **Qu'est-ce que ShelfReader ?**

**ShelfReader** est une application qui reconnaît automatiquement les titres de livres sur des photos d'étagères.

### **Comment ça marche ?**
1. 📸 **Prenez une photo** d'une étagère de livres
2. 🤖 **L'IA analyse** l'image et détecte les textes
3. 📚 **Résultat** : Liste des livres identifiés avec leurs titres

### **Pour qui ?**
- 📖 **Particuliers** : Inventorier sa bibliothèque personnelle
- 🏪 **Libraires** : Gérer rapidement les stocks
- 📚 **Étudiants** : Trouver des livres dans les bibliothèques
- 🏛️ **Écoles** : Cataloguer automatiquement les collections

### **Points forts**
- ✅ **Facile à utiliser** : Interface simple et intuitive
- ✅ **Rapide** : Analyse une étagère en quelques secondes
- ✅ **Intelligent** : Détecte automatiquement les séparations entre livres
- ✅ **Précis** : Corrige automatiquement les erreurs de reconnaissance

---

## 🚀 **Installation (5 minutes)**

### **Prérequis**
- **Ordinateur** : Windows, macOS ou Linux
- **Python** : Version 3.8 ou supérieure
- **Connexion internet** : Pour télécharger les composants

### **Installation automatique**

#### **Étape 1 : Télécharger le projet**
```bash
# Copier cette commande dans votre terminal
git clone https://github.com/delnixcode/Shelfreader.git
cd Shelfreader/p1-MVP-Desktop
```

#### **Étape 2 : Activer l'environnement virtuel**
```bash
# Sur Linux/macOS
source env-p1/bin/activate

# Sur Windows
env-p1\Scripts\activate
```

#### **Étape 3 : Installer les dépendances**
```bash
# Cette commande installe tous les composants nécessaires
pip install -r requirements.txt
```

#### **Étape 4 : Vérifier l'installation**
```bash
# Tester que tout fonctionne
python --version  # Doit afficher Python 3.8+

# Tester les composants principaux
python -c "import easyocr, torch; print('✅ Installation réussie !')"
```

**🎉 Félicitations !** ShelfReader est maintenant installé sur votre ordinateur.

---

## ⚡ **Démarrage rapide (3 étapes)**

### **Étape 1 : Activer l'environnement**
```bash
# Toujours faire ça au début
source env-p1/bin/activate  # Linux/macOS
# ou
env-p1\Scripts\activate     # Windows
```

### **Étape 2 : Tester avec une image d'exemple**
```bash
# Cette commande analyse une photo d'exemple
python src/ocr_easyocr.py test_images/books1.jpg --gpu
```

**Résultat attendu :**
```
🔍 EasyOCR avec détection de tranches - Image: test_images/books1.jpg
📊 Résultats: 11 livres détectés
🎯 Confiance moyenne: 0.908
📝 Texte complet: Ada 95 | KERNICHAN THE SECOND EDITION PTR | ...
```

### **Étape 3 : Voir les résultats**
Les résultats sont automatiquement sauvegardés dans le dossier `result-ocr/`.

**🎯 Succès !** Vous venez d'analyser votre première étagère de livres !

---

## 💻 **Comment utiliser**

### **Analyser vos propres photos**

#### **Format des images**
- ✅ **JPG/JPEG** : Recommandé
- ✅ **PNG** : Fonctionne aussi
- 📏 **Taille** : Minimum 1000 pixels de largeur
- 💡 **Conseil** : Photos bien éclairées, perpendiculaires à l'étagère

#### **Commandes de base**

```bash
# Analyser une photo simple
python src/ocr_easyocr.py ma_photo.jpg

# Avec GPU pour aller plus vite (recommandé)
python src/ocr_easyocr.py ma_photo.jpg --gpu

# Sauvegarder les résultats dans un fichier spécifique
python src/ocr_easyocr.py ma_photo.jpg --output mes_resultats.txt
```

#### **Exemple complet**
```bash
# Analyser une étagère avec toutes les améliorations
python src/ocr_easyocr.py etagere_bibliotheque.jpg --gpu --validate --output resultats_etagere.txt
```

### **Comprendre les résultats**

Le fichier de résultats contient :
```
=== RÉSULTATS OCR ===
Titre détecté: "LE PETIT PRINCE"
Confiance: 0.892
Position: x=45, y=120

Titre détecté: "HARRY POTTER"
Confiance: 0.756
Position: x=45, y=160
```

- **Titre détecté** : Le nom du livre reconnu
- **Confiance** : Probabilité que ce soit correct (0.0 à 1.0)
- **Position** : Coordonnées sur l'image

### **Traiter plusieurs images**
```bash
# Analyser toutes les photos JPG d'un dossier
for photo in mes_photos/*.jpg; do
  echo "Analyse de $photo..."
  python src/ocr_easyocr.py "$photo" --gpu
done
```

---

## 🎨 **Interface web**

Pour une utilisation plus simple, ShelfReader propose une interface web moderne.

### **Démarrage**
```bash
# Lancer l'interface web
streamlit run src/app.py
```

Puis ouvrir http://localhost:8501 dans votre navigateur.

### **Fonctionnalités**
- 📤 **Glisser-déposer** : Déposez vos photos directement
- ⚙️ **Configuration** : Réglages simples pour l'analyse
- 👁️ **Aperçu** : Visualisez les zones détectées
- 📊 **Résultats** : Tableaux clairs des livres trouvés
- 💾 **Téléchargement** : Exportez les résultats

---

## 🔧 **Options avancées**

### **Améliorer la précision**

#### **Seuil de confiance**
```bash
# Très tolérant (beaucoup de résultats, peut-être des erreurs)
python src/ocr_easyocr.py image.jpg --confidence 0.1

# Équilibre recommandé (bon compromis)
python src/ocr_easyocr.py image.jpg --confidence 0.2

# Strict (haute précision, moins de résultats)
python src/ocr_easyocr.py image.jpg --confidence 0.5
```

#### **Validation intelligente**
```bash
# Activer la correction automatique des titres
python src/ocr_easyocr.py image.jpg --validate

# Combinaison optimale recommandée
python src/ocr_easyocr.py image.jpg --gpu --validate --confidence 0.3
```

### **Désactiver des fonctionnalités**
```bash
# Désactiver la détection intelligente de livres
python src/ocr_easyocr.py image.jpg --no-spine

# Mode debug (pour les développeurs)
python src/ocr_easyocr.py image.jpg --debug
```

### **Configuration recommandée**
```bash
# Pour débuter (simple et efficace)
python src/ocr_easyocr.py image.jpg --gpu

# Pour production (maximum de précision)
python src/ocr_easyocr.py image.jpg --gpu --validate --confidence 0.3 --output resultats.txt
```

---

## 🛠️ **Dépannage**

### **❌ "ModuleNotFoundError"**
**Problème :** Un composant n'est pas installé.

**Solution :**
```bash
# Réactiver l'environnement virtuel
source env-p1/bin/activate

# Réinstaller les dépendances
pip install -r requirements.txt
```

### **❌ "CUDA out of memory"**
**Problème :** Problème avec le GPU.

**Solution :**
```bash
# Utiliser le CPU à la place
python src/ocr_easyocr.py image.jpg  # Sans --gpu
```

### **❌ Aucun texte détecté**
**Problème :** L'image est trop sombre ou floue.

**Solutions :**
```bash
# Baisser le seuil de confiance
python src/ocr_easyocr.py image.jpg --confidence 0.1

# Essayer un autre moteur OCR
python src/ocr_tesseract.py image.jpg

# Vérifier la qualité de l'image
```

### **❌ Commande inconnue**
**Problème :** Erreur de frappe dans la commande.

**Solution :**
```bash
# Voir toutes les options disponibles
python src/ocr_easyocr.py --help
```

### **Vérifications système**
```bash
# Vérifier Python
python --version

# Vérifier l'environnement virtuel
which python  # Doit pointer vers env-p1/bin/python

# Vérifier espace disque
df -h
```

---

## ❓ **Questions fréquentes**

### **🤔 Quel moteur OCR choisir ?**
- **EasyOCR** (recommandé) : Bon équilibre vitesse/précision
- **Tesseract** : Ultra rapide, pour les tests
- **TrOCR** : Maximum précision, plus lent

### **💻 GPU obligatoire ?**
- **Non**, mais recommandé pour aller 3x plus vite
- Tous les moteurs fonctionnent en CPU
- Testez d'abord sans GPU, ajoutez `--gpu` après

### **📏 Quelle taille d'image ?**
- **Minimum** : 1000 pixels de largeur
- **Recommandé** : 2000+ pixels
- **Format** : JPG ou PNG de bonne qualité

### **⚡ C'est rapide ?**
- **Tesseract** : ~2 secondes
- **EasyOCR CPU** : ~5-10 secondes
- **EasyOCR GPU** : ~2-5 secondes
- **TrOCR GPU** : ~5-15 secondes

### **💾 Où sont sauvegardés les résultats ?**
- **Dossier** : `result-ocr/`
- **Format** : Fichiers texte (.txt)
- **Contenu** : Titres détectés + détails techniques

### **🌐 Internet nécessaire ?**
- **OCR** : Fonctionne hors ligne
- **Enrichissement** : Nécessite internet (optionnel)
- **Interface web** : Fonctionne en local

---

## 📚 **Informations techniques**

### **Architecture du projet**
```
p1-MVP-Desktop/
├── src/                    # Code source principal
│   ├── ocr_easyocr.py      # Moteur OCR principal
│   ├── ocr_tesseract.py    # Moteur rapide
│   ├── ocr_trocr.py        # Moteur haute précision
│   ├── app.py              # Interface web
│   └── api_client.py       # API externes
├── tests/                  # Tests et démonstrations
├── test_images/            # Photos d'exemple
├── result-ocr/             # Résultats (auto-créé)
└── requirements.txt        # Dépendances
```

### **Algorithmes utilisés**

#### **Détection Shelfie**
- Analyse des lignes de séparation entre livres
- Réduction de 81% des fragments de texte
- Groupement intelligent des textes par livre

#### **Validation Jaccard**
- Comparaison avec base de référence connue
- Correction automatique des erreurs OCR
- Précision de 93% sur les titres

#### **Support GPU**
- Accélération PyTorch CUDA
- Fallback automatique CPU
- Détection automatique du matériel

### **Dépendances principales**
- **easyocr** : Reconnaissance optique de caractères
- **torch** : Calcul GPU/CPU
- **streamlit** : Interface web
- **opencv-python** : Traitement d'images
- **Pillow** : Manipulation d'images

### **Performances mesurées**
| Moteur | Précision | Vitesse | GPU |
|--------|-----------|---------|-----|
| EasyOCR Pro | 90.8% | 3-5s | ✅ |
| Tesseract | 73.3% | 1-2s | ❌ |
| TrOCR | 80.7% | 8-15s | ✅ |

### **API externes**
- **Open Library** : Métadonnées des livres
- **Limite** : 100 requêtes/minute
- **Usage** : Enrichissement optionnel

---

## 🤝 **Contribuer**

### **Signaler un problème**
1. Vérifier que le problème n'existe pas déjà
2. Créer une "issue" sur GitHub avec :
   - Description claire du problème
   - Étapes pour reproduire
   - Version de Python et OS

### **Améliorer le code**
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Tester vos changements
4. Créer une Pull Request

### **Standards de développement**
- **Python** : Version 3.8 minimum
- **Style** : PEP 8
- **Tests** : Couverture minimum 80%
- **Documentation** : Commentaires en anglais

---

## 📈 **Évolution du projet**

### **✅ Version actuelle (P1 - MVP)**
- [x] Reconnaissance OCR basique
- [x] Interface web simple
- [x] Support GPU
- [x] Détection intelligente de livres
- [x] Validation des titres
- [x] Documentation complète

### **🔄 Prochaines étapes**
- [ ] Interface mobile
- [ ] Base de données locale
- [ ] Mode traitement par lot
- [ ] Export PDF/Excel
- [ ] API REST
- [ ] Synchronisation cloud

---

**🎉 Merci d'utiliser ShelfReader !**

Pour plus d'informations : [GitHub Issues](https://github.com/delnixcode/Shelfreader/issues)

*Développé avec ❤️ pour les amoureux des livres*reamlit.io/)
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

### **🚀 Améliorations Récentes (Octobre 2025)**

#### **🎯 OCR Intelligent avec Algorithme Shelfie**
- **Détection de lignes de dos** : Algorithme inspiré du projet "shelfie" pour identifier automatiquement les séparations entre livres
- **Groupement intelligent** : Regroupement des textes fragmentés par livre avec analyse statistique des gaps verticaux
- **Réduction fragmentation** : Passage de 59 textes à 11 livres identifiés (81% d'amélioration)

#### **⚡ Support GPU Optimisé**
- **PyTorch CUDA** : Accélération GPU complète avec fallback CPU automatique
- **Détection automatique** : Vérification disponibilité GPU au démarrage
- **Performance** : ~3x plus rapide sur GPU NVIDIA

#### **🎯 Validation de Similarité**
- **Algorithme Jaccard** : Validation des titres détectés contre base de référence
- **Correction automatique** : Correction de titres mal reconnus (ex: "Idman Softwgre Construction With Ada 95" → "Ada 95")
- **Précision** : 13/14 titres correctement identifiés avec validation

#### **🏗️ Réorganisation Architecturale**
- **Structure optimisée** : Tous les fichiers source dans `src/`, tests dans `tests/`
- **Code consolidé** : OCR EasyOCR unifié avec toutes les améliorations
- **CLI amélioré** : Interface commande ligne avec support multi-options

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

# 2. Tester avec une image d'exemple (avec toutes les améliorations)
python src/ocr_easyocr.py test_images/books1.jpg --gpu --validate

# 3. Lancer l'interface web (optionnel)
streamlit run src/app.py
```

**Résultat attendu** : Un fichier `result-ocr/easyocr_spine_results.txt` contenant les titres de livres détectés avec validation.

---

## 💻 **Utilisation détaillée**

### **Commandes de Base**

#### **Traitement d'une image avec EasyOCR**
```bash
# Analyse basique
python src/ocr_easyocr.py test_images/books1.jpg

# Avec GPU (recommandé)
python src/ocr_easyocr.py test_images/books1.jpg --gpu

# Avec seuil de confiance personnalisé
python src/ocr_easyocr.py test_images/books1.jpg --confidence 0.3

# Mode verbeux (détails complets)
python src/ocr_easyocr.py test_images/books1.jpg --verbose

# Avec détection de lignes shelfie (activée par défaut)
python src/ocr_easyocr.py test_images/books1.jpg --gpu

# Avec validation de similarité
python src/ocr_easyocr.py test_images/books1.jpg --gpu --validate

# Désactiver la détection shelfie si nécessaire
python src/ocr_easyocr.py test_images/books1.jpg --gpu --no-spine
```

#### **Utilisation des autres moteurs**
```bash
# Tesseract (rapide, CPU uniquement)
python src/ocr_tesseract.py test_images/books1.jpg

# TrOCR (haute précision, GPU recommandé)
python src/ocr_trocr.py test_images/books1.jpg --gpu
```

#### **Interface CLI unifiée**
```bash
# Utiliser l'interface unifiée
python src/cli.py easyocr --gpu --confidence 0.3 test_images/books1.jpg
python src/cli.py tesseract test_images/books1.jpg
python src/cli.py trocr --gpu test_images/books1.jpg
```

### **Options Avancées**

#### **Options Avancées (Nouvelles fonctionnalités)**

#### **Détection Shelfie**
```bash
# La détection de lignes de dos de livres est activée par défaut
python src/ocr_easyocr.py image.jpg --gpu

# Désactiver si nécessaire pour comparer
python src/ocr_easyocr.py image.jpg --gpu --no-spine
```

#### **Validation de Similarité**
```bash
# Activer la validation contre base de référence
python src/ocr_easyocr.py image.jpg --validate

# Combiné avec GPU pour performance optimale
python src/ocr_easyocr.py image.jpg --gpu --validate
```

#### **Configuration Combinée**
```bash
# Configuration optimale recommandée
python src/ocr_easyocr.py image.jpg \
  --gpu \
  --validate \
  --confidence 0.3 \
  --output result-ocr/optimized_results.txt
```

#### **Paramètres de Configuration**
```bash
# Liste complète des options
python src/ocr_easyocr.py --help

# Exemples d'options avancées
python src/ocr_easyocr.py image.jpg \
  --gpu \
  --confidence 0.3 \
  --validate \
  --output result-ocr/custom_results.txt
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

### **OCR Multi-Moteurs Avancé**
- 🔍 **EasyOCR Pro** : Moteur principal avec GPU, détection shelfie, validation similarité
- ⚡ **Tesseract** : Moteur rapide (CPU uniquement, vitesse optimale)
- 🎯 **TrOCR** : Moteur haute précision (GPU recommandé, IA avancée)

### **Algorithmes Intelligents**
- 📊 **Analyse statistique** : Détection des gaps verticaux entre livres
- 🎯 **Shelfie Algorithm** : Détection automatique des lignes de séparation
- 🔍 **Validation Jaccard** : Correction intelligente des titres mal reconnus
- 🎨 **Preprocessing avancé** : Amélioration qualité image pour OCR

### **Support Matériel**
- 🚀 **GPU NVIDIA** : Accélération CUDA avec PyTorch
- 💻 **CPU Fallback** : Fonctionnement dégradé sans GPU
- 🔄 **Auto-détection** : Choix automatique du meilleur matériel disponible

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
├── src/                    # Code source principal
│   ├── __init__.py
│   ├── api_client.py       # Client Open Library API
│   ├── app.py              # Interface web Streamlit
│   ├── cli.py              # Interface ligne de commande
│   ├── ocr_easyocr.py      # OCR EasyOCR avancé (GPU + shelfie)
│   ├── ocr_tesseract.py    # OCR Tesseract
│   └── ocr_trocr.py        # OCR TrOCR
├── tests/                  # Tests et démos
│   ├── __init__.py
│   ├── README.md           # Documentation des tests
│   ├── demo_ocr_improvements.py    # Démo améliorations OCR
│   ├── test_easyocr_improvements.py # Tests OCR avancés
│   ├── test_gpu_usage.py    # Tests performance GPU
│   └── test_separation.py   # Tests séparation textes
├── test_images/            # Images de test
│   ├── books1.jpg
│   └── books2.jpg
├── result-ocr/             # Résultats générés (auto-créé)
├── docs/                   # Documentation détaillée
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

#### **Benchmarks sur `test_images/books1.jpg` (Octobre 2025)**

| Moteur | Textes Détectés | Livres Identifiés | Confiance Moyenne | Temps | GPU Support | Améliorations |
|--------|-----------------|-------------------|-------------------|-------|-------------|---------------|
| **EasyOCR Pro** | 59 → 11 | 11 | 0.908 | ~3-5s | ✅ Excellent | Shelfie + Validation |
| **EasyOCR Classic** | 59 | - | 0.885 | ~3-5s | ✅ Excellent | Base |
| **Tesseract** | 15 | - | 0.733 | ~1.5s | ❌ Aucun | - |
| **TrOCR** | 14 | - | 0.807 | ~8-15s | ✅ Bon | - |

#### **Améliorations Mesurées**
- **📈 Réduction fragmentation** : 81% (59 → 11 textes)
- **🎯 Précision titres** : 93% (13/14 correctement identifiés avec validation)
- **⚡ Performance GPU** : ~3x plus rapide
- **🔍 Détection shelfie** : Identification automatique des séparations de livres

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

### **Suite de Tests Complète**

#### **Tests Disponibles**
```bash
# Test des améliorations OCR (recommandé)
python tests/demo_ocr_improvements.py

# Tests unitaires OCR avancés
python tests/test_easyocr_improvements.py

# Tests de performance GPU
python tests/test_gpu_usage.py

# Tests de séparation de textes
python tests/test_separation.py
```

#### **Documentation des Tests**
📖 Voir [`tests/README.md`](tests/README.md) pour la documentation complète des tests.

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

### **✅ Implémenté (Octobre 2025)**
- [x] OCR multi-moteurs (EasyOCR, Tesseract, TrOCR)
- [x] Interface web Streamlit
- [x] API Open Library
- [x] Sauvegarde automatique des résultats
- [x] Tests unitaires complets
- [x] Documentation complète
- [x] **Algorithme shelfie pour détection de livres**
- [x] **Support GPU PyTorch CUDA optimisé**
- [x] **Validation de similarité Jaccard**
- [x] **Réorganisation architecturale**
- [x] **CLI unifié avec options avancées**

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
