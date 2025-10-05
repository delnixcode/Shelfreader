# 🔬 Sciences et Technologies derrière ShelfReader OCR

## 📋 Sommaire

### 1. [Principes Fondamentaux de l'OCR](#1-principes-fondamentaux-de-locr)
   - 1.1 [Qu'est-ce que l'OCR ?](#11-quest-ce-que-locr)
   - 1.2 [Défis Spécifiques aux Tranches de Livres](#12-défis-spécifiques-aux-tranches-de-livres)
   - 1.3 [Pipeline OCR Classique](#13-pipeline-ocr-classique)

### 2. [Moteurs OCR Disponibles](#2-moteurs-ocr-disponibles)
   - 2.1 [EasyOCR - Moteur Principal](#21-easyocr---moteur-principal)
   - 2.2 [Tesseract - Moteur Rapide](#22-tesseract---moteur-rapide)
   - 2.3 [TrOCR - Moteur Spécialisé Manuscrit](#23-trocr---moteur-spécialisé-manuscrit)

### 3. [Algorithmes de Détection de Tranches](#3-algorithmes-de-détection-de-tranches)
   - 3.1 [Méthode SHELFIE (vertical_lines)](#31-méthode-shelfie-vertical_lines)
   - 3.2 [Méthode ICCV2013 (horizontal_shelves)](#32-méthode-iccv2013-horizontal_shelves)
   - 3.3 [Comparaison des Approches](#33-comparaison-des-approches)

### 4. [Prétraitement d'Images](#4-prétraitement-dimages)
   - 4.1 [Amélioration du Contraste](#41-amélioration-du-contraste)
   - 4.2 [Réduction du Bruit](#42-réduction-du-bruit)
   - 4.3 [Normalisation](#43-normalisation)

### 5. [Algorithmes de Regroupement](#5-algorithmes-de-regroupement)
   - 5.1 [Regroupement par Lignes de Tranches](#51-regroupement-par-lignes-de-tranches)
   - 5.2 [Fallback Adaptatif (vertical_lines)](#52-fallback-adaptatif-vertical_lines)
   - 5.3 [Fallback Simple (horizontal_shelves)](#53-fallback-simple-horizontal_shelves)
   - 5.4 [Comparaison Détaillée des Fallbacks](#54-comparaison-détaillée-des-fallbacks)
   - 5.5 [Exemples Pratiques de Comportement](#55-exemples-pratiques-de-comportement)

### 6. [Paramètres et Configuration](#6-paramètres-et-configuration)
   - 6.1 [Paramètres de Détection](#61-paramètres-de-détection)
   - 6.2 [Paramètres OCR](#62-paramètres-ocr)
   - 6.3 [Paramètres de Regroupement](#63-paramètres-de-regroupement)

### 7. [Optimisations et Performance](#7-optimisations-et-performance)
   - 7.1 [Accélération GPU](#71-accélération-gpu)
   - 7.2 [Traitement Multi-échelle](#72-traitement-multi-échelle)
   - 7.3 [Filtrage de Confiance](#73-filtrage-de-confiance)

---

## 1. Principes Fondamentaux de l'OCR

### 1.1 Qu'est-ce que l'OCR ?

L'**OCR (Optical Character Recognition)** est une technologie qui permet de convertir des images contenant du texte en texte numérique exploitable par les ordinateurs.

**Principe scientifique :**
- Analyse des pixels pour identifier des motifs correspondant à des caractères
- Utilise des algorithmes de vision par ordinateur et d'intelligence artificielle
- Combine traitement d'image et apprentissage automatique

**Équation fondamentale :**
```
Image(pixels) → Analyse morphologique → Classification caractères → Texte structuré
```

### 1.2 Défis Spécifiques aux Tranches de Livres

Les tranches de livres posent des défis uniques pour l'OCR :

| Défi | Description | Impact |
|------|-------------|--------|
| **Orientation verticale** | Texte écrit verticalement | Algorithmes classiques inefficaces |
| **Éclairage variable** | Ombres et reflets sur les tranches | Contraste irrégulier |
| **Déformation géométrique** | Courbure des dos de livres | Distorsion des caractères |
| **Multi-polices** | Différentes tailles et styles | Complexité de reconnaissance |
| **Bruit visuel** | Grain du papier, poussière | Faux positifs de détection |

### 1.3 Pipeline OCR Classique

```
1. Acquisition d'image
2. Prétraitement (contraste, bruit, normalisation)
3. Détection de régions de texte
4. Segmentation en caractères/lignes
5. Classification des caractères
6. Post-traitement et correction
```

**Dans ShelfReader :** Nous ajoutons une étape de détection de tranches avant la segmentation.

---

## 2. Moteurs OCR Disponibles

### 2.1 EasyOCR - Moteur Principal

**Technologie :** Réseaux de neurones convolutionnels (CNN) + RNN + CTC Loss

**Spécialisation :** Texte imprimé, multi-langues, orientations variables

**Architecture :**
```
Image → CNN Feature Extraction → BiLSTM Sequence Modeling → CTC Decoding → Texte
```

**Avantages :**
- ✅ Précision élevée (93% sur tranches)
- ✅ Support multi-langues natif
- ✅ Gestion des orientations complexes
- ✅ Robuste aux variations d'éclairage

**Limites :**
- ❌ Lent sans GPU
- ❌ Consommation mémoire importante
- ❌ Moins efficace sur manuscrit

### 2.2 Tesseract - Moteur Rapide

**Technologie :** Moteur OCR traditionnel + LSTM (depuis v4.0)

**Spécialisation :** Texte imprimé standard, traitement rapide

**Modes de fonctionnement :**
- **Legacy Engine** : Règles linguistiques + templates
- **Neural nets LSTM** : Réseaux de neurones pour séquence

**Avantages :**
- ✅ Ultra-rapide (CPU uniquement)
- ✅ Faible consommation ressources
- ✅ Installation système simple
- ✅ Support PSM (Page Segmentation Modes)

**Limites :**
- ❌ Moins précis que EasyOCR
- ❌ Sensible aux orientations complexes
- ❌ Moins robuste aux images bruitées

### 2.3 TrOCR - Moteur Spécialisé Manuscrit

**Technologie :** Transformers (Vision Encoder + Text Decoder)

**Spécialisation :** Texte manuscrit, documents historiques

**Architecture :**
```
Image → Vision Transformer → Cross-attention → Text Generation (Beam Search)
```

**Modèle :** microsoft/trocr-base-handwritten (333M paramètres)

**Avantages :**
- ✅ Excellente reconnaissance manuscrit
- ✅ Génération de texte naturel
- ✅ Robuste aux variations stylistiques

**Limites :**
- ❌ Très lent sans GPU
- ❌ Consommation mémoire énorme
- ❌ Moins efficace sur texte imprimé
- ❌ Modèle volumineux à charger

---

## 3. Algorithmes de Détection de Tranches

### 3.1 Méthode SHELFIE (vertical_lines)

**Principe :** Détection des lignes de séparation verticales entre livres

**Algorithme détaillé :**

1. **Downsampling** : Réduction résolution (facteur 3) pour optimisation
2. **Filtrage Gaussien** : Réduction bruit (σ=3)
3. **Détection de bords horizontaux** : Sobel X² pour accentuer transitions verticales
4. **Standardisation** : Normalisation statistique (μ=0, σ=1)
5. **Binarisation** : Seuil adaptatif (max/100)
6. **Érosion verticale** : Suppression bruit (kernel 1×50)
7. **Analyse composantes connectées** : Identification clusters verticaux
8. **Filtrage hauteur** : Suppression lignes trop courtes (<30% hauteur max)
9. **Upsampling** : Retour résolution originale
10. **Extraction lignes** : Régression linéaire sur clusters

**Mathématiques :**
```python
# Détection de bords horizontaux
sobel_x = cv2.Sobel(image, CV_64F, 1, 0, ksize=3)
edges = sobel_x²

# Standardisation
edges_std = (edges - edges.mean()) / edges.std()

# Binarisation adaptative
threshold = edges_std.max() / 100
binary = (edges_std > threshold) * 255
```

**Cas d'usage optimal :** Rayonnages verticaux, tranches bien alignées

### 3.2 Méthode ICCV2013 (horizontal_shelves)

**Principe :** Détection des étagères horizontales dans les rayonnages

**Algorithme détaillé :**

1. **Détection de bords** : Canny (seuils 50-150)
2. **Balayage horizontal** : Analyse densité bords par ligne
3. **Filtrage étagères** : Seulement lignes avec >50% pixels bords
4. **Dilatation morphologique** : Extension lignes (kernel large horizontal)
5. **Analyse composantes** : Identification régions étagères
6. **Filtrage hauteur** : Régions >5% hauteur image
7. **Extraction lignes** : Conversion régions → lignes horizontales

**Mathématiques :**
```python
# Détection Canny
edges = cv2.Canny(gray, 50, 150)

# Analyse densité par ligne horizontale
for y in range(height):
    pixel_count = sum(edges[y, :] > 0)
    if pixel_count >= width * 0.5:  # 50% seuil
        shelf_lines[y, :] = 255

# Dilatation morphologique
kernel = cv2.getStructuringElement(MORPH_RECT, (width//10, 3))
dilated = cv2.dilate(shelf_lines, kernel)
```

**Cas d'usage optimal :** Rayonnages horizontaux, étagères visibles

### 3.3 Comparaison des Approches

| Critère | SHELFIE (vertical_lines) | ICCV2013 (horizontal_shelves) |
|---------|------------------------|------------------------------|
| **Orientation** | Verticales (tranches) | Horizontales (étagères) |
| **Complexité** | Élevée (14 étapes) | Moyenne (7 étapes) |
| **Robustesse** | Haute (filtrage multi-niveau) | Moyenne (seuils fixes) |
| **Performance** | Plus lent | Plus rapide |
| **Précision** | Excellente | Bonne |
| **Fallback** | Regroupement adaptatif | Regroupement proximité |

---

## 4. Prétraitement d'Images

### 4.1 Amélioration du Contraste

**CLAHE (Contrast Limited Adaptive Histogram Equalization) :**
- Division image en tuiles 6×6
- Égalisation histogramme locale
- Limitation contraste (clip limit = 3.0)
- Fusion tuiles pour éviter artefacts

**Avantages :** Améliore lisibilité sans amplifier bruit

### 4.2 Réduction du Bruit

**Filtrage bilatéral :**
```python
blurred = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
```

**Propriétés :**
- Préserve les bords
- Réduit le bruit gaussien
- Paramètres adaptatifs selon image

### 4.3 Normalisation

**Standardisation statistique :**
```python
normalized = (image - mean) / std
```

**Objectif :** Rendre les images comparables pour les algorithmes de détection

---

## 5. Algorithmes de Regroupement

### 5.1 Regroupement par Lignes de Tranches

**Principe :** Utiliser les lignes détectées pour créer des groupes logiques

**Pour vertical_lines :**
- Tri lignes par position X
- Création blocs entre lignes verticales
- Regroupement horizontal des textes dans chaque bloc

**Pour horizontal_shelves :**
- Tri lignes par position Y
- Création blocs entre lignes horizontales
- Regroupement vertical des textes dans chaque bloc

### 5.2 Fallback Adaptatif (vertical_lines)

**Principe :** Analyse intelligente des données pour déterminer le meilleur seuil de regroupement

**Algorithme multi-échelle :**
1. **Analyse statistique** : Calcul des écarts entre toutes les boîtes de texte consécutives
2. **Calcul du seuil adaptatif** : `(Q25 + médiane) / 2` des écarts, borné entre 10-35px
3. **Test multi-seuils** : Évaluation avec 3 seuils (0.6×, 1.0×, 1.4× du seuil adaptatif)
4. **Sélection optimale** : Choix du seuil donnant le plus de groupes (max 20 groupes)

**Exemple concret :**
```python
# Écarts mesurés entre boîtes: [15px, 25px, 8px, 30px, 12px]
# Q25 = 12px, médiane = 15px
# Seuil adaptatif = (12 + 15) / 2 = 13.5px
# Tests: 8.1px, 13.5px, 18.9px
# Résultat: seuil 8.1px donne 15 groupes → sélectionné
```

**Avantages :**
- ✅ S'adapte automatiquement aux caractéristiques de l'image
- ✅ Robuste aux variations d'espacement des livres
- ✅ Optimise le nombre de groupes détectés

**Inconvénients :**
- ❌ Plus lent (3 calculs au lieu d'1)
- ❌ Plus complexe à déboguer
- ❌ Comportement non-déterministe

### 5.3 Fallback Simple (horizontal_shelves)

**Principe :** Regroupement déterministe avec seuil fixe, privilégiant la séparation

**Algorithme de proximité :**
1. **Tri horizontal** : Classement des boîtes par position X croissante
2. **Regroupement itératif** : Fusion des boîtes si écart < seuil fixe (25px)
3. **Combinaison finale** : Fusion des textes et calcul des boîtes englobantes

**Seuil fixe actuel :** 25px (configurable via `HORIZONTAL_GROUP_THRESHOLD_BASE`)

**Exemple concret :**
```python
# Boîtes: [x=10, x=35, x=70, x=110, x=160]
# Écarts: 25px, 35px, 40px, 50px
# Seuil: 25px
# Résultat: [10+35], [70], [110], [160] → 4 groupes
```

**Avantages :**
- ✅ Ultra-rapide (un seul passage)
- ✅ Comportement prévisible et déterministe
- ✅ Simple à comprendre et déboguer

**Inconvénients :**
- ❌ Ne s'adapte pas aux caractéristiques spécifiques de l'image
- ❌ Peut créer trop de groupes séparés ou trop de fusions
- ❌ Sensible au choix du seuil fixe

### 5.4 Comparaison Détaillée des Fallbacks

| Aspect | Adaptatif (vertical_lines) | Simple (horizontal_shelves) |
|--------|---------------------------|----------------------------|
| **Approche** | Analyse statistique des données | Seuil fixe prédéfini |
| **Complexité** | Élevée (multi-échelle) | Faible (un seul seuil) |
| **Performance** | Plus lent | Plus rapide |
| **Robustesse** | Excellente (s'adapte) | Moyenne (seuil fixe) |
| **Prédictibilité** | Variable selon image | Constante |
| **Nombre groupes** | Optimisé automatiquement | Dépend du seuil fixe |
| **Cas optimal** | Images variées, espacement irrégulier | Images standardisées |

**Quand utiliser chaque méthode :**

**vertical_lines (adaptatif) :**
- Images avec espacement irrégulier des livres
- Quand on veut maximiser le nombre de livres détectés
- Applications où la précision compte plus que la vitesse

**horizontal_shelves (simple) :**
- Images avec espacement régulier
- Traitement temps réel où la vitesse est critique
- Quand on veut un comportement constant et prévisible

### 5.5 Exemples Pratiques de Comportement

**Scénario : Image avec boîtes espacées de 20-30px**

**vertical_lines (adaptatif) :**
```
Écarts mesurés: [20px, 25px, 30px]
Seuil calculé: (20+25)/2 = 22.5px
Tests: 13.5px, 22.5px, 31.5px
Résultat: 13.5px → 4 groupes (séparation maximale)
```

**horizontal_shelves (simple) :**
```
Seuil fixe: 25px
Écarts: [20px, 25px, 30px]
Résultat: 20px < 25px → fusion, 25px = 25px → séparation, 30px > 25px → séparation
→ 3 groupes (regroupement intermédiaire)
```

**Impact sur les résultats :**
- **Adaptatif** : S'adapte aux données, peut créer plus de groupes
- **Simple** : Comportement fixe, plus prévisible mais moins optimal

---

## 6. Paramètres et Configuration

### 6.1 Paramètres de Détection

| Paramètre | Valeur | Impact |
|-----------|--------|--------|
| `DOWNSAMPLE_FACTOR` | 3 | Performance vs précision |
| `GAUSSIAN_BLUR_SIGMA` | 3 | Réduction bruit |
| `VERTICAL_ERODE_LENGTH` | 50 | Filtrage lignes courtes |
| `MIN_SPINE_LINES_THRESHOLD` | 5 | Déclenchement fallback |

### 6.2 Paramètres OCR

| Paramètre | Valeur | Impact |
|-----------|--------|--------|
| `OCR_WIDTH_THS` | 0.3 | Tolérance largeur caractères |
| `OCR_HEIGHT_THS` | 0.3 | Tolérance hauteur caractères |
| `OCR_CONTRAST_THS` | 0.05 | Seuil contraste minimum |
| `OCR_TEXT_THRESHOLD` | 0.5 | Confiance minimum détection |

### 6.3 Paramètres de Regroupement

| Paramètre | Valeur | Impact |
|-----------|--------|--------|
| `HORIZONTAL_GROUP_THRESHOLD_BASE` | 25 | Distance max regroupement (horizontal_shelves) |
| `ADAPTIVE_THRESHOLD_MIN/MAX` | 10/35 | Limites seuil adaptatif |
| `FONT_SIZE_RATIO_STRICT` | 1.5 | Seuil police différente |

---

## 7. Optimisations et Performance

### 7.1 Accélération GPU

**Impact sur les moteurs :**

| Moteur | CPU | GPU | Accélération |
|--------|-----|-----|--------------|
| EasyOCR | ~17s | ~3-5s | 3-5× |
| Tesseract | ~0.07s | N/A | - |
| TrOCR | ~15s | ~2-3s | 5-7× |

**Technologies :**
- CUDA pour calculs matriciels
- cuDNN pour optimisations réseau
- TensorRT pour inférence optimisée

### 7.2 Traitement Multi-échelle

**Principe :** Test multiple seuils pour robustesse

```python
thresholds = [adaptive * 0.6, adaptive * 1.0, adaptive * 1.4]
best_result = max(results, key=lambda r: len(r.groups))
```

**Avantages :** Meilleure détection dans conditions variables

### 7.3 Filtrage de Confiance

**Principe :** Élimination résultats peu fiables

```python
confident_results = [r for r in results if r.confidence > threshold]
```

**Impact :** Réduction faux positifs, amélioration précision

### 8. [Glossaire - Vocabulaire pour Débutants](#8-glossaire---vocabulaire-pour-débutants)

**Pourquoi un glossaire ?** Ce document utilise beaucoup de termes techniques issus des mathématiques, de l'informatique et de la vision par ordinateur. Cette section explique les concepts clés de manière simple, comme si vous découvriez ces notions pour la première fois. Chaque terme est défini avec des mots accessibles, parfois avec des analogies du quotidien.

**Comment l'utiliser :** Si vous rencontrez un mot inconnu dans le document, cherchez-le ici ! Les explications sont classées par ordre alphabétique pour faciliter la recherche.

### A
**Algorithme** : Recette mathématique qui dit à l'ordinateur comment résoudre un problème étape par étape.

**Analyse composantes connectées** : Technique pour trouver des "îlots" de pixels connectés dans une image (comme trouver des continents sur une carte).

### B
**Binarisation** : Transformer une image en noir et blanc (pixels = 0 ou 255) pour simplifier l'analyse.

**Boîte englobante (bounding box)** : Rectangle imaginaire qui entoure un élément détecté (comme une boîte autour d'un mot).

### C
**Canny** : Algorithme de détection de bords dans les images (trouve les contours des objets).

**CLAHE (Contrast Limited Adaptive Histogram Equalization)** : Technique pour améliorer le contraste local d'une image sans créer d'artefacts.

**CNN (Convolutional Neural Network)** : Type d'intelligence artificielle spécialisé dans l'analyse d'images, inspiré du cerveau humain.

**Composantes connectées** : Groupes de pixels qui se touchent dans une image.

**Confiance (confidence)** : Probabilité (entre 0 et 1) que la reconnaissance OCR soit correcte.

**Convolution** : Opération mathématique qui "glisse" un petit filtre sur l'image pour en extraire des caractéristiques.

### D
**Détection de bords** : Trouver les contours des objets dans une image.

**Dilatation morphologique** : Grossir les zones blanches d'une image (élargir les contours).

**Downsampling** : Réduire la taille d'une image pour accélérer les calculs.

**DPI (Dots Per Inch)** : Nombre de points par pouce, mesure de la résolution d'une image.

### E
**Écart-type (standard deviation)** : Mesure de la dispersion des valeurs autour de la moyenne.

**Érosion morphologique** : Réduire les zones blanches d'une image (affaiblir les contours).

### F
**Fallback** : Plan B - méthode alternative utilisée quand la méthode principale échoue.

**Filtrage bilatéral** : Technique pour réduire le bruit d'une image tout en préservant les bords.

**Filtrage gaussien** : Flou naturel appliqué à une image (comme un effet de brouillard).

### G
**GPU (Graphics Processing Unit)** : Processeur spécialisé dans les calculs graphiques et parallèles.

### H
**Histogramme** : Graphique montrant la distribution des valeurs (ex: combien de pixels de chaque couleur).

**horizontal_shelves** : Algorithme de détection des étagères horizontales (ex-ICCV2013).

### I
**ICCV2013** : Ancienne appellation de l'algorithme de détection des étagères horizontales (maintenant horizontal_shelves).

**Intelligence artificielle (IA)** : Programmes qui apprennent et prennent des décisions comme un humain.

**Interpolation** : Technique pour agrandir une image en inventant des pixels intermédiaires.

### K
**Kernel** : Petit matrice utilisée pour les opérations de convolution (comme un tampon).

### L
**LSTM (Long Short-Term Memory)** : Type de réseau neuronal qui se souvient du passé.

### M
**Machine Learning** : Apprentissage automatique - l'ordinateur apprend des patterns sans être explicitement programmé.

**Médiane** : Valeur centrale d'une liste triée (50% des valeurs sont en dessous, 50% au-dessus).

**Morphologie mathématique** : Ensemble d'opérations pour analyser la forme des objets dans les images.

**Multi-échelle** : Analyser une image à différentes résolutions/tailles.

### N
**Neurone artificiel** : Unité de base d'un réseau neuronal, inspirée des neurones biologiques.

**Normalisation** : Mettre les valeurs à la même échelle (ex: entre 0 et 1) pour les comparer.

### O
**OCR (Optical Character Recognition)** : Reconnaissance optique de caractères - transformer une image de texte en texte numérique.

**OpenCV** : Bibliothèque logicielle gratuite pour le traitement d'images et la vision par ordinateur.

### P
**Paramètre** : Valeur que l'on peut ajuster pour changer le comportement d'un algorithme.

**Pixel** : Plus petit élément d'une image numérique (contraction de "picture element").

**Prétraitement** : Étapes préparatoires avant l'analyse principale (nettoyer, améliorer l'image).

**Probabilité** : Chance qu'un événement se produise (entre 0 = impossible et 1 = certain).

### Q
**Quantile** : Division d'un ensemble trié (ex: Q25 = valeur où 25% des données sont en dessous).

### R
**Réseau neuronal** : Système d'IA inspiré du cerveau, composé de neurones artificiels connectés.

**Résolution** : Nombre de pixels dans une image (ex: 1920x1080 pixels).

**RGB** : Système de couleurs avec Rouge, Vert, Bleu (Red, Green, Blue).

### S
**Seuil (threshold)** : Valeur limite pour décider si quelque chose est accepté ou rejeté.

**SHELFIE** : Ancienne appellation de l'algorithme de détection des lignes verticales (maintenant vertical_lines).

**Sobel** : Opérateur mathématique pour détecter les bords verticaux et horizontaux.

**Standardisation** : Transformer les données pour qu'elles aient une moyenne de 0 et un écart-type de 1.

### T
**Tensor** : Structure de données multi-dimensionnelle (généralisation des matrices).

**Traitement d'images** : Ensemble de techniques pour analyser et modifier des images numériques.

### U
**Upsampling** : Agrandir une image (augmenter le nombre de pixels).

### V
**vertical_lines** : Algorithme de détection des lignes verticales entre tranches de livres (ex-SHELFIE).

**Vision par ordinateur** : Domaine de l'IA qui apprend aux ordinateurs à "voir" et comprendre les images.

### W
**Weight (poids)** : Paramètre d'un réseau neuronal qui contrôle l'importance d'une connexion.

---

*Glossaire - Comprendre les termes techniques de l'OCR*</content>
<parameter name="filePath">/home/delart/Documents/dev/python/Shelfreader/p1-OCR-Streamlit/src/engines/OCR_SCIENCES_ET_TECHNOLOGIES.md