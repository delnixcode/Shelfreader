# Scripts de lancement ShelfReader P1

## Scripts disponibles

### 🚀 startfront.sh
Lance l'application web Streamlit (interface utilisateur)
```bash
./startfront.sh
```

### 🔍 Scripts OCR Engines

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
**Paramètres par défaut :** `--gpu --confidence 0.1 --spine-method vertical_lines`

**Arguments disponibles :**
- `--gpu` : Utilise le GPU pour accélérer le traitement (beaucoup plus rapide)
- `--cpu` : Force l'utilisation du CPU (plus lent mais compatible partout)
- `--lang [langues]` : Langues à utiliser (ex: `--lang en fr de`) - défaut: `en`
- `--confidence 0.1` : Seuil de confiance minimum (0.0-1.0) - défaut: `0.1`
- `--spine-method [méthode]` : Méthode de détection des tranches - choix: `vertical_lines`, `horizontal_shelves` - défaut: `vertical_lines`
- `--debug` : Mode debug avec informations détaillées
- `--benchmark` : Afficher les métriques de performance
- `--output fichier.json` : Sauvegarder les résultats au format JSON

#### runtess.sh - Tesseract Engine
```bash
./runtess.sh image.jpg [--options]
```
**Paramètres par défaut :** `--confidence 0.5 --psm 6`

**Arguments disponibles :**
- `--gpu` : Utilise le GPU si disponible (non standard pour Tesseract)
- `--cpu` : Force l'utilisation du CPU (recommandé pour Tesseract)
- `--lang [langues]` : Langues à utiliser (ex: `--lang eng fra`) - défaut: `eng`
- `--confidence 0.5` : Seuil de confiance minimum (0.0-1.0) - défaut: `0.5`
- `--psm [mode]` : Page Segmentation Mode (voir détails ci-dessous) - défaut: `6`
- `--debug` : Mode debug avec informations détaillées
- `--benchmark` : Afficher les métriques de performance
- `--output fichier.json` : Sauvegarder les résultats au format JSON

#### runtrocr.sh - TrOCR Engine
```bash
./runtrocr.sh image.jpg [--options]
```
**Paramètres par défaut :** `--gpu --device auto`

**Arguments disponibles :**
- `--gpu` : Force l'utilisation du GPU NVIDIA
- `--cpu` : Force l'utilisation du CPU
- `--device [device]` : Choix du matériel - choix: `auto`, `cuda`, `cpu` - défaut: `auto`
- `--debug` : Mode debug avec informations détaillées
- `--benchmark` : Afficher les métriques de performance
- `--output fichier.json` : Sauvegarder les résultats au format JSON

### 📋 Modes PSM Tesseract (Page Segmentation Mode)

| PSM | Description | Usage recommandé |
|-----|-------------|------------------|
| 0 | Orientation and script detection only | Détection d'orientation uniquement |
| 1 | Automatic page segmentation with OSD | Segmentation automatique avec OSD |
| 2 | Automatic page segmentation, but no OSD, or OCR | Segmentation automatique sans OSD |
| 3 | Fully automatic page segmentation, but no OSD | Segmentation automatique complète |
| 4 | Assume a single column of text of variable sizes | Colonne unique de texte |
| 5 | Assume a single uniform block of vertically aligned text | Bloc uniforme vertical |
| **6** | Assume a single uniform block of text | **Bloc uniforme (défaut)** |
| 7 | Treat the image as a single text line | Ligne de texte unique |
| 8 | Treat the image as a single word | Mot unique |
| 9 | Treat the image as a single word in a circle | Mot dans un cercle |
| 10 | Treat the image as a single character | Caractère unique |
| 11 | Sparse text. Find as much text as possible in no particular order | Texte éparpillé |
| 12 | Sparse text with OSD | Texte éparpillé avec OSD |
| 13 | Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific | Ligne brute |

### 💡 Conseils d'utilisation

#### Choix du moteur OCR
- **EasyOCR** : Meilleur pour les tranches de livres, support multi-langues natif
- **Tesseract** : Rapide, fiable pour le texte standard, bon support langues
- **TrOCR** : Spécialisé dans les images de scènes, très précis mais lent

#### Optimisation des performances
- Utilisez `--gpu` quand disponible pour accélérer considérablement le traitement
- Pour les tests rapides, utilisez `--cpu` pour éviter les conflits GPU
- `--benchmark` permet de mesurer les performances de chaque moteur

#### Débogage
- `--debug` affiche des informations détaillées sur le processus
- `--output fichier.json` sauvegarde les résultats pour analyse ultérieure
- Vérifiez les seuils de confiance selon vos besoins (plus bas = plus de détections)

### 🔧 Dépannage

#### Problèmes courants
- **CUDA out of memory** : Utilisez `--cpu` ou réduisez la taille des images
- **Aucun texte détecté** : Baissez le seuil `--confidence` ou changez de `--spine-method`
- **Performance lente** : Vérifiez que `--gpu` fonctionne correctement avec `nvidia-smi`

#### Validation des résultats
- Comparez les résultats des 3 moteurs pour valider la précision
- Utilisez `--benchmark` pour identifier les goulots d'étranglement
- Les fichiers de résultats JSON permettent l'analyse détaillée

## 📚 Explication détaillée des paramètres

### --spine-method (EasyOCR uniquement)
Méthode de détection des séparations entre livres sur l'étagère :
- **`vertical_lines` (par défaut)** : détecte les séparations verticales entre livres
- **`horizontal_shelves`** : détecte les étagères horizontales (méthode ICCC2013)

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
./runeasy.sh test_images/books1.jpg --confidence 0.3 --spine-method horizontal_shelves
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