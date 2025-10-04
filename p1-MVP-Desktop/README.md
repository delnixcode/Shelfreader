# 🏗️ **P1 - MVP Desktop**
## OCR + API + Interface Web

**ShelfReader MVP Desktop** est la première étape concrète du projet. Prototype fonctionnel validant le concept de base : **extraire du texte des photos de tranches de livres et l'enrichir avec des données bibliographiques**.

### 🎯 **Objectifs**
- ✅ Validation technique : OCR sur tranches de livres (3 moteurs : EasyOCR, TrOCR, Tesseract)
- ✅ Validation fonctionnelle : Enrichissement API Open Library
- ✅ Validation UX : Interface web fonctionnelle
- ✅ **Sauvegarde automatique** : Résultats OCR dans `result-ocr/` avec fichiers par moteur
- ✅ Base réutilisable : Code repris dans projets suivants

### 📁 **Structure**
```
p1-MVP-Desktop/
├── env-p1/              # Environnement virtuel P1
├── backup_ocr_v1/       # 🗂️ BACKUP - Version finale OCR P1
│   ├── README.md        # Documentation du backup
│   ├── ocr_easyocr.py   # Moteur EasyOCR (sauvegardé)
│   ├── ocr_tesseract.py # Moteur Tesseract (sauvegardé)
│   ├── ocr_trocr.py     # Moteur TrOCR (sauvegardé)
│   └── ocr_detect.py    # Script principal (sauvegardé)
├── result-ocr/          # 📁 RÉSULTATS OCR (auto-généré)
│   ├── easyocr_results.txt
│   ├── tesseract_results.txt
│   └── trocr_results.txt
├── scripts/             # Scripts utilitaires
│   └── ocr_detect.py    # Script de détection OCR (multi-moteurs)
├── src/                 # Code source P1
│   ├── __init__.py      # Package initialization
│   ├── ocr_easyocr.py   # Module OCR EasyOCR (GPU/CPU)
│   ├── ocr_tesseract.py # Module OCR Tesseract
│   ├── ocr_trocr.py     # Module OCR TrOCR (Transformers)
│   ├── api_client.py    # Client Open Library
│   └── app.py           # Interface Streamlit
├── test_images/         # Images de test pour l'OCR
├── tests/               # Tests unitaires
├── docs/                # Documentation spécifique
├── requirements.txt     # Dépendances P1
├── README.md           # Cette documentation
└── TODO.md             # Tâches en cours
```

### 🚀 **Installation & Configuration**

#### 1. Activer l'environnement virtuel
```bash
cd p1-MVP-Desktop
source env-p1/bin/activate  # Linux/Mac
# ou env-p1\Scripts\activate  # Windows
```

#### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

#### 3. Vérifier l'installation
```bash
python -c "import torch; print('PyTorch OK' if torch.cuda.is_available() else 'PyTorch OK (CPU only)')"
```

### 🖥️ **Interface Web (Streamlit)**

#### Démarrage rapide
```bash
streamlit run src/app.py
```

L'interface s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`.

### 🔍 **Script OCR - Commandes**

Le script `scripts/ocr_detect.py` permet de tester l'OCR directement en ligne de commande.

#### Utilisation de base
```bash
# Analyse avec EasyOCR (par défaut) et CPU
python scripts/ocr_detect.py test_images/books1.jpg

# Analyse avec GPU (recommandé pour de meilleures performances)
python scripts/ocr_detect.py --gpu test_images/books1.jpg
```

#### Options avancées
```bash
# Utiliser Tesseract au lieu d'EasyOCR
python scripts/ocr_detect.py --tesseract test_images/books1.jpg

# Tesseract avec GPU
python scripts/ocr_detect.py --gpu --tesseract test_images/books1.jpg

# Utiliser TrOCR (Transformers-based OCR) - Plus précis mais plus lent
python scripts/ocr_detect.py --trocr test_images/books1.jpg

# TrOCR avec GPU (recommandé)
python scripts/ocr_detect.py --gpu --trocr test_images/books1.jpg

# EasyOCR explicite (équivalent au défaut)
python scripts/ocr_detect.py --easyocr test_images/books1.jpg
```

#### Images de test disponibles
```bash
# Lister les images de test
ls test_images/

# Analyser toutes les images de test
for img in test_images/*.jpg; do
    echo "=== Analyse de $img ==="
    python scripts/ocr_detect.py --gpu "$img"
    echo
done
```

### � **Scripts OCR individuels**

Chaque moteur OCR peut être utilisé indépendamment. **Les résultats sont automatiquement sauvegardés dans le dossier `result-ocr/`**.

#### **EasyOCR (Recommandé - GPU/CPU)**
```bash
# Test de base avec GPU (recommandé)
python src/ocr_easyocr.py test_images/books1.jpg --gpu

# Test avec CPU seulement
python src/ocr_easyocr.py test_images/books1.jpg

# Avec seuil de confiance personnalisé
python src/ocr_easyocr.py test_images/books1.jpg --gpu --confidence 0.3

# Combinaison d'options
python src/ocr_easyocr.py test_images/books1.jpg --gpu --confidence 0.5 --output mes_resultats.txt
# Résultat : result-ocr/mes_resultats.txt
```

#### **Tesseract (Rapide - CPU seulement)**
```bash
# Test de base (optimisé pour la vitesse ~1.5s)
python src/ocr_tesseract.py test_images/books1.jpg

# Avec langue française
python src/ocr_tesseract.py test_images/books1.jpg --lang fra

# Avec seuil de confiance plus élevé pour moins de faux positifs
python src/ocr_tesseract.py test_images/books1.jpg --confidence 0.5

# Combinaison complète
python src/ocr_tesseract.py test_images/books1.jpg --lang eng --confidence 0.3 --output tesseract_detaille.txt
# Résultat : result-ocr/tesseract_detaille.txt
```

#### **TrOCR (Précis - GPU recommandé)**
```bash
# Test avec GPU (recommandé pour les performances)
python src/ocr_trocr.py test_images/books1.jpg --gpu --confidence 0.5

# Test CPU (fonctionne mais plus lent)
python src/ocr_trocr.py test_images/books1.jpg --confidence 0.5

# Avec seuil de confiance plus strict pour haute précision
python src/ocr_trocr.py test_images/books1.jpg --gpu --confidence 0.7

# Combinaison complète
python src/ocr_trocr.py test_images/books1.jpg --gpu --confidence 0.6 --output trocr_precision.txt
# Résultat : result-ocr/trocr_precision.txt
```

### 📁 **Dossier des résultats - `result-ocr/`**

Tous les résultats OCR sont automatiquement sauvegardés dans ce dossier :

```
result-ocr/
├── easyocr_results.txt      # Résultats EasyOCR (par défaut)
├── trocr_results.txt        # Résultats TrOCR (par défaut)
├── tesseract_results.txt    # Résultats Tesseract (par défaut)
└── [nom_personnalisé].txt   # Fichiers avec --output
```

**Format des fichiers de résultats :**
```
=== RÉSULTATS OCR - test_images/books1.jpg ===
Date: 2025-10-04 12:34:56
Nombre de textes détectés: 11
Confiance moyenne: 0.885

TEXTE COMPLET:
[Tous les textes détectés séparés par |]

DÉTAIL PAR LIVRE:
--- Livre 1 ---
Confiance: 0.703
Texte: [Titre du livre 1]
--- Livre 2 ---
...
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

### 📖 **Explication détaillée des commandes**

#### **Pourquoi 3 moteurs OCR ?**
Chaque moteur a ses forces et faiblesses pour différents types d'images de livres :

1. **EasyOCR** : Le plus équilibré
   - ✅ Meilleure précision sur les dos de livres verticaux
   - ✅ Support GPU excellent
   - ✅ Segmentation automatique des livres
   - ⚠️ Un peu plus lent que Tesseract

2. **Tesseract** : Le plus rapide
   - ✅ Ultra rapide (~1.5 secondes)
   - ✅ Support multi-langues
   - ✅ Parfait pour tests rapides
   - ⚠️ Moins précis sur texte vertical
   - ⚠️ Pas de support GPU

3. **TrOCR** : Le plus précis
   - ✅ Meilleure précision sur texte imprimé
   - ✅ Basé sur Transformers (IA moderne)
   - ✅ Bon support GPU
   - ⚠️ Plus lent (~8-15 secondes)
   - ⚠️ Moins adapté au texte manuscrit

#### **Quand utiliser chaque moteur ?**
- **Tests rapides** → Tesseract
- **Production/Précision** → EasyOCR
- **Maximum précision** → TrOCR
- **Images difficiles** → Tester les 3 et comparer

#### **Le seuil de confiance (`--confidence`)**
Le seuil de confiance filtre les résultats OCR :
- **Faible (0.1-0.2)** : Plus de résultats, plus de bruit
- **Moyen (0.3-0.5)** : Équilibre idéal
- **Élevé (0.6-0.8)** : Moins de résultats, plus fiables

**Exemple pratique :**
```bash
# Pour commencer (recommandé)
python src/ocr_easyocr.py test_images/books1.jpg --gpu --confidence 0.2

# Pour haute précision
python src/ocr_trocr.py test_images/books1.jpg --gpu --confidence 0.7

# Pour tests ultra-rapides
python src/ocr_tesseract.py test_images/books1.jpg --confidence 0.3
```

#### **Sauvegarde automatique**
Chaque commande crée automatiquement un fichier dans `result-ocr/` :
- Format structuré avec date, statistiques, texte complet et détail par livre
- Fichier remplacé à chaque exécution (pas d'accumulation)
- Nom personnalisable avec `--output`

#### **Exemples pratiques d'utilisation**

```bash
# 📚 SCÉNARIO 1 : Découverte rapide d'une étagère
# Tester tous les moteurs pour voir lequel fonctionne le mieux
python src/ocr_easyocr.py test_images/books1.jpg --gpu --confidence 0.2
python src/ocr_tesseract.py test_images/books1.jpg --confidence 0.3
python src/ocr_trocr.py test_images/books1.jpg --gpu --confidence 0.5

# 📊 Comparer les résultats
cat result-ocr/easyocr_results.txt | head -10
cat result-ocr/tesseract_results.txt | head -10
cat result-ocr/trocr_results.txt | head -10

# 🎯 SCÉNARIO 2 : Analyse de précision pour un livre spécifique
# Utiliser TrOCR avec seuil élevé pour maximum de précision
python src/ocr_trocr.py test_images/books1.jpg --gpu --confidence 0.7 --output livre_difficile.txt

# ⚡ SCÉNARIO 3 : Traitement en lot rapide
# Traiter plusieurs images avec Tesseract (le plus rapide)
for img in test_images/*.jpg; do
    echo "=== Analyse de $(basename "$img") ==="
    python src/ocr_tesseract.py "$img" --confidence 0.4
done

# 💾 SCÉNARIO 4 : Sauvegarde organisée par projet
# Créer des fichiers nommés par projet/usage
python src/ocr_easyocr.py test_images/books1.jpg --gpu --output projet_etude_livres.txt
python src/ocr_easyocr.py test_images/books2.jpg --gpu --output projet_bibliotheque.txt

# 🔍 SCÉNARIO 5 : Debug et optimisation
# Tester différents seuils de confiance
for conf in 0.1 0.2 0.3 0.4 0.5; do
    echo "=== Seuil de confiance: $conf ==="
    python src/ocr_easyocr.py test_images/books1.jpg --gpu --confidence $conf --output test_conf_$conf.txt
done
```

#### **Comparaison des moteurs OCR**

| Moteur | GPU Support | Vitesse | Précision | Sauvegarde auto | Usage recommandé |
|--------|-------------|---------|-----------|-----------------|------------------|
| **EasyOCR** | ✅ Excellent | 🚀 ~3-5s | 🟢🟢 Excellente | `result-ocr/easyocr_results.txt` | **Défaut - Tous usages** |
| **Tesseract** | ❌ Aucun | ⚡ ~1.5s | 🟡 Moyenne | `result-ocr/tesseract_results.txt` | Tests rapides, CPU limité |
| **TrOCR** | ✅ Bon | 🐌 ~8-15s | 🟢 Bonne | `result-ocr/trocr_results.txt` | Précision maximale |

**📊 Benchmarks sur `test_images/books1.jpg` :**
- **EasyOCR** : 11 livres détectés, confiance 0.885, temps ~3s
- **Tesseract** : 15 textes détectés, confiance 0.733, temps ~1.5s  
- **TrOCR** : 14 textes détectés, confiance 0.807, temps ~12s

### 🖥️ **Interface Web (Streamlit)**
```

### 🧪 **Tests**

#### Tests unitaires
```bash
# Activer l'environnement virtuel d'abord
source env-p1/bin/activate

# Lancer tous les tests
python -m pytest tests/

# Tests avec couverture
python -m pytest tests/ --cov=src --cov-report=html
```

#### Tests OCR manuels
```bash
# Test rapide avec image de démo - Script principal
python scripts/ocr_detect.py --gpu test_images/books1.jpg

# Test de chaque module individuellement (avec sauvegarde automatique)
python src/ocr_easyocr.py test_images/books1.jpg --gpu
python src/ocr_tesseract.py test_images/books1.jpg
python src/ocr_trocr.py test_images/books1.jpg --gpu --confidence 0.5

# Vérifier les résultats sauvegardés
ls -la result-ocr/
cat result-ocr/easyocr_results.txt

# Test avec vos propres images
python src/ocr_easyocr.py --gpu chemin/vers/votre/image.jpg --output mes_livres.txt
```

### 🔗 **Ressources Partagées**

- **Images de test supplémentaires** : `../../shared/data/test_images/`
- **Documentation générale** : `../../shared/docs/`
- **Scripts partagés** : `../../shared/scripts/`

### 📋 **Phases de développement**

1. **Phase 1.1** ✅ : Configuration environnement
2. **Phase 1.2** ✅ : Module OCR de base
3. **Phase 1.3** ✅ : Client API Open Library
4. **Phase 1.4** ✅ : Interface Streamlit
5. **Phase 1.5** 🔄 : Intégration et tests (en cours)

### 🛠️ **Technologies**

| Composant | Technologie | Version | Support GPU |
|-----------|-------------|---------|-------------|
| **OCR Principal** | EasyOCR + PyTorch | GPU/CPU | ✅ Excellent |
| **OCR Alternative** | Tesseract | 5.0+ | ❌ Aucun |
| **OCR Avancé** | TrOCR (Transformers) | microsoft/trocr-base-printed | ✅ Bon |
| **Computer Vision** | OpenCV | 4.8+ | ✅ |
| **API Client** | requests | 2.31+ | - |
| **Interface** | Streamlit | 1.28+ | - |
| **Langage** | Python | 3.8+ | - |

### ⚠️ **Limitations connues**

- **Précision OCR** : La reconnaissance des titres de livres peut nécessiter des améliorations
- **Performance** : L'analyse GPU est recommandée pour de meilleures performances
- **Interface** : L'interface Streamlit est temporaire - une vraie app desktop est prévue

### 🚀 **Prochaines étapes**

- Améliorer la précision de l'OCR
- Développer l'interface desktop native (remplacer Streamlit)
- Optimiser les performances
- Ajouter plus de tests automatisés