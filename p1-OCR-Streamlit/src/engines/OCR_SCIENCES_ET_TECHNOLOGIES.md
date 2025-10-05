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

**Multi-scale detection :**
1. Calcul seuil adaptatif basé sur statistiques des écarts
2. Test 3 seuils : 0.6×, 1.0×, 1.4× du seuil adaptatif
3. Sélection meilleur résultat (max groupes sans dépasser 20)

**Seuil adaptatif :**
```python
gaps = [distance between consecutive boxes]
adaptive_threshold = (Q25 + median) / 2
clamped_threshold = clamp(adaptive_threshold, 10, 35)
```

### 5.3 Fallback Simple (horizontal_shelves)

**Regroupement par proximité :**
- Tri boîtes par position X
- Regroupement si écart < seuil fixe (50px)
- Combinaison textes dans chaque groupe

**Avantages :** Rapide, déterministe, prévisible

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
| `HORIZONTAL_GROUP_THRESHOLD_BASE` | 50 | Distance max regroupement |
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

---

*Document technique - ShelfReader OCR Engine - Version 1.0*</content>
<parameter name="filePath">/home/delart/Documents/dev/python/Shelfreader/p1-OCR-Streamlit/src/engines/OCR_SCIENCES_ET_TECHNOLOGIES.md