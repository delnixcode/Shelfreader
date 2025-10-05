# Scripts de lancement ShelfReader P1

## Scripts disponibles

### 🚀 startfront.sh
Lance l'application web Streamlit (interface utilisateur)
```bash
./startfront.sh
```

### 🔍 Scripts OCR Engines

#### runeasy.sh - EasyOCR Engine
```bash
./runeasy.sh image.jpg [--options]
```
**Paramètres par défaut :** `--gpu --confidence 0.1 --spine-method shelfie`

**Explication des paramètres :**
- `--gpu` : Utilise le GPU pour accélérer le traitement (beaucoup plus rapide)
- `--confidence 0.1` : Seuil de confiance minimum bas (0.1 = 10%) pour détecter plus de texte
- `--spine-method shelfie` : Utilise l'algorithme "Shelfie" pour détecter les séparations entre livres

#### runtess.sh - Tesseract Engine
```bash
./runtess.sh image.jpg [--options]
```
**Paramètres par défaut :** `--confidence 0.5 --psm 6`

**Explication des paramètres :**
- `--confidence 0.5` : Seuil de confiance minimum moyen (0.5 = 50%) pour filtrer le bruit
- `--psm 6` : Page Segmentation Mode 6 - traite l'image comme un bloc uniforme de texte

#### runtrocr.sh - TrOCR Engine
```bash
./runtrocr.sh image.jpg [--options]
```
**Paramètres par défaut :** `--gpu --device auto`

**Explication des paramètres :**
- `--gpu` : Utilise le GPU pour accélérer le traitement du modèle de deep learning
- `--device auto` : Détection automatique du device (GPU si disponible, sinon CPU)

## 📚 Explication détaillée des paramètres

### --spine-method (EasyOCR uniquement)
Méthode de détection des séparations entre livres sur l'étagère :
- **`shelfie`** : Algorithme avancé qui analyse les bords verticaux pour trouver les espaces entre livres
- **`iccc2013`** : Méthode plus simple basée sur la détection d'étagères horizontales

### --psm (Tesseract uniquement)
Page Segmentation Mode - comment Tesseract analyse la structure de la page :
- **`6`** : Traite l'image comme un bloc uniforme de texte (idéal pour les tranches de livres)
- **`3`** : Analyse complète automatique (plus lent)
- **`8`** : Traite comme une seule ligne de texte
- **`13`** : Ligne brute (pas de segmentation)

### --device (TrOCR uniquement)
Choix du matériel pour exécuter le modèle :
- **`auto`** : Détection automatique (recommandé)
- **`cuda`** : Force l'utilisation du GPU NVIDIA
- **`cpu`** : Force l'utilisation du CPU

### --confidence (Tous les engines)
Seuil de confiance minimum pour accepter un résultat OCR :
- **0.1-0.3** : Faible (détecte beaucoup de texte, peut inclure du bruit)
- **0.5-0.7** : Moyen (bon équilibre qualité/précision)
- **0.8-0.9** : Élevé (seulement les meilleurs résultats, peut manquer du texte)

## Exemples d'utilisation

```bash
# Test rapide avec paramètres par défaut
./runeasy.sh test_images/books1.jpg
./runtess.sh test_images/books1.jpg
./runtrocr.sh test_images/books1.jpg

# Mode debug pour voir les détails du traitement
./runeasy.sh test_images/books1.jpg --debug
./runtess.sh test_images/books1.jpg --debug
./runtrocr.sh test_images/books1.jpg --debug

# Benchmark pour mesurer les performances
./runeasy.sh test_images/books1.jpg --benchmark
./runtess.sh test_images/books1.jpg --benchmark
./runtrocr.sh test_images/books1.jpg --benchmark

# Changer les paramètres par défaut
./runeasy.sh test_images/books1.jpg --confidence 0.3 --spine-method iccc2013
./runtess.sh test_images/books1.jpg --psm 3 --confidence 0.7
./runtrocr.sh test_images/books1.jpg --device cpu

# Lancer l'interface web
./startfront.sh
```

## 📁 Résultats

Les résultats OCR sont automatiquement sauvegardés dans le dossier `result-ocr/` :
- `easyocr_spine_results.txt` : Résultats détaillés avec positions des livres
- `tesseract_results.txt` : Résultats Tesseract avec confiance
- `trocr_results.txt` : Résultats TrOCR avec confiance

Chaque fichier contient :
- Date et heure du traitement
- Nombre d'éléments détectés
- Confiance moyenne
- Texte complet avec niveaux de confiance
- Détail par "livre" détecté