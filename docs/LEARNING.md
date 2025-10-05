# 📚 ShelfReader - Documentation d'apprentissage

> 📖 **Guide principal** : Cette page contient la vision globale et les liens vers les documentations détaillées de chaque module.

## 📂 Structure de la documentation

```
📁 ShelfReader/
├── README.md              # Vue d'ensemble du projet
├── LEARNING.md            # ← Vous êtes ici (hub principal)
└── docs/
    └── phase1/            # Phase 1 : P1 OCR Streamlit
        ├── api_client.md  # 🌐 Détails complets du client API
        ├── ocr_module.md  # 🔤 Détails complets de l'OCR (à venir)
        ├── app.md         # 🖥️ Détails de l'interface (à venir)
        └── torch_utils.md # 🔮 Stub Phase 2 (à venir)
```

## 🗺️ Navigation rapide

### 📖 Phase 1 (en cours)
- **[🌐 api_client.md](docs/phase1/api_client.md)** ← Explication complète des TODOs 1-4
- 🔤 ocr_module.md (à venir)
- 🖥️ app.md (à venir)

### 🚀 Phases futures
- Phase 2 : Orientation automatique
- Phase 3 : Optimisation et cache
- Phase 4 : Interface mobile statique
- Phase 5 : Temps réel et AR

---

## 🎯 Vision finale du projet

**ShelfReader** est une application mobile de computer vision en **temps réel** qui permet de :

### 📱 Expérience utilisateur
```
👤 Tu es dans une bibliothèque
     ↓
📱 Tu ouvres l'app sur ton téléphone
     ↓
🎥 Ta caméra reste ouverte en continu
     ↓
🚶 Tu te déplaces devant les étagères
     ↓
✨ L'app détecte et analyse EN TEMPS RÉEL :
   - 🔍 Détecte les tranches de livres
   - 📝 Lit les titres avec OCR
   - 📚 Récupère les résumés
   - ⭐ Affiche des recommandations personnalisées
     ↓
🔄 Analyse continue pendant que tu avances
```

### 🎮 Cas d'usage
- Tu marches dans une bibliothèque
- Tu pointes ton téléphone vers une étagère
- L'app affiche en **overlay** (superposition) :
  - Rectangles autour des livres détectés
  - Titre + auteur de chaque livre
  - Score de recommandation selon tes goûts
- Tu avances → nouveaux livres détectés automatiquement

### 🚀 Défis techniques
- ⚡ **Performance temps réel** : Détection + OCR + API en < 100ms
- 📱 **Optimisation mobile** : Modèle léger, faible consommation batterie
- 🔄 **Analyse continue** : Traitement de flux vidéo 30 FPS
- 🧠 **Cache intelligent** : Ne pas retraiter les mêmes livres
- 🎯 **Recommandations IA** : Système de préférences avec PyTorch

---

## 🎯 Cas d'usage de l'application

### 📚 Problème à résoudre
Tu es dans une bibliothèque avec des centaines de livres sur les étagères :
- 😫 **Problème 1** : Les titres sont **verticaux** → mal au cou pour lire
- 😫 **Problème 2** : Tu cherches un livre spécifique → difficile à trouver visuellement
- 😫 **Problème 3** : Tu veux des livres sur un sujet (ex: "Python") → pas de filtre

### ✨ Solution : ShelfReader

**Mode 1 : Recherche par titre exact**
```
"Je cherche : Harry Potter"
→ L'app détecte tous les livres
→ Surligne "Harry Potter" avec sa position
```

**Mode 2 : Recherche par thématique**
```
"Thématique : Python"
→ L'app détecte tous les livres
→ Surligne TOUS les livres sur Python
→ Affiche les titres en horizontal (lisibles)
```

**Mode 3 : Exploration (temps réel)**
```
Caméra ouverte en continu
→ L'app détecte et affiche les titres en direct
→ Tu te déplaces devant l'étagère
→ Les infos se mettent à jour automatiquement
```

---

## 🔄 Workflows complets

### 📸 Workflow Version 1 : Photo unique (Phase 1)

```
┌─────────────────────────────────────────────────┐
│ 1. CHOIX DU MODE                                │
│    ○ Titre exact  ● Thématique                  │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 2. ENTRÉE UTILISATEUR                           │
│    Recherche : "Python"                         │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 3. CAPTURE IMAGE                                │
│    📸 Prendre une photo de l'étagère            │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 4. DÉTECTION (YOLOv8)                           │
│    � Détecter chaque tranche de livre          │
│    [Livre1] [Livre2] [Livre3] [Livre4]         │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 5. ORIENTATION                                  │
│    🔄 Détecter l'angle du texte                 │
│    ↩️ Rotation automatique (vertical → horizontal)│
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 6. OCR (EasyOCR)                                │
│    📝 Lire le texte de chaque livre             │
│    Livre1: "Python Crash Course"                │
│    Livre2: "Java Programming"                   │
│    Livre3: "Learning Python"                    │
│    Livre4: "Django for Beginners"               │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 7. ENRICHISSEMENT (Open Library API)            │
│    🌐 Pour chaque livre détecté :               │
│    - Chercher dans Open Library                 │
│    - Récupérer catégories/sujets                │
│    - Récupérer couverture                       │
│                                                 │
│    Livre1: ["Python", "Programming"]            │
│    Livre2: ["Java", "Programming"]              │
│    Livre3: ["Python", "Beginner"]               │
│    Livre4: ["Python", "Django", "Web"]          │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 8. MATCHING                                     │
│    🎯 Recherche thématique : "Python"           │
│                                                 │
│    Chercher dans :                              │
│    - Texte OCR (titre)                          │
│    - Catégories Open Library                    │
│                                                 │
│    ✅ Livre1: "Python" dans titre + catégories  │
│    ❌ Livre2: "Java" (pas de match)             │
│    ✅ Livre3: "Python" dans titre + catégories  │
│    ✅ Livre4: "Python" + "Django" dans catégories│
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 9. AFFICHAGE AVEC OVERLAY                       │
│    📸 Image annotée :                           │
│    ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐         │
│    │ ✅   │ │      │ │ ✅   │ │ ✅   │         │
│    │PYTHON│ │ JAVA │ │PYTHON│ │DJANGO│         │
│    │CRASH │ │      │ │  FOR │ │      │         │
│    │COURSE│ │      │ │DUMMIES│      │         │
│    └──────┘ └──────┘ └──────┘ └──────┘         │
│       1        2        3        4              │
│                                                 │
│    📋 Résultats (3 livres trouvés) :            │
│    1. Python Crash Course (Position 1)          │
│       📚 Catégories : Python, Programming       │
│    2. Learning Python (Position 3)              │
│       📚 Catégories : Python, Beginner          │
│    3. Django for Beginners (Position 4)         │
│       📚 Catégories : Python, Django, Web       │
└─────────────────────────────────────────────────┘
```

---

### 🎥 Workflow Version 2 : Temps réel (Phase 5)

```
┌─────────────────────────────────────────────────┐
│ 1. OUVERTURE DE L'APP MOBILE                    │
│    📱 Lancement de l'application                │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 2. ACTIVATION CAMÉRA                            │
│    🎥 Flux vidéo en continu (30 FPS)            │
│    📸 Stream : frame 1, frame 2, frame 3...     │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 3. BOUCLE INFINIE (jusqu'à fermeture app)       │
│    🔄 while camera.is_open():                   │
└─────────────────────────────────────────────────┘
      ↓                                     ↑
      │                                     │
      │  ┌──────────────────────────────┐  │
      └─→│ 4. CAPTURE FRAME             │──┘
         │    📸 Lire 1 frame du stream │
         └──────────────────────────────┘
                        ↓
         ┌──────────────────────────────┐
         │ 5. CACHE INTELLIGENT         │
         │    🧠 Frame similaire ?      │
         │    Si OUI → Réutiliser cache│
         │    Si NON → Nouvelle analyse│
         └──────────────────────────────┘
                        ↓
         ┌──────────────────────────────┐
         │ 6. DÉTECTION (YOLOv8n)       │
         │    ⚡ Modèle optimisé mobile │
         │    🔍 Détecter livres        │
         │    ⏱️ ~50ms                  │
         └──────────────────────────────┘
                        ↓
         ┌──────────────────────────────┐
         │ 7. OCR SÉLECTIF              │
         │    📝 Seulement nouveaux     │
         │    💾 Cache des connus       │
         │    ⏱️ ~100ms par livre       │
         └──────────────────────────────┘
                        ↓
         ┌──────────────────────────────┐
         │ 8. API AVEC CACHE LOCAL      │
         │    🌐 SQLite local           │
         │    📦 Requêtes batch         │
         │    ⏱️ ~50ms (si en cache)    │
         └──────────────────────────────┘
                        ↓
         ┌──────────────────────────────┐
         │ 9. AFFICHAGE OVERLAY AR      │
         │    🎨 Rectangles sur livres  │
         │    📝 Titres lisibles        │
         │    ⭐ Scores (si recherche)  │
         │    ⏱️ ~10ms                  │
         └──────────────────────────────┘
                        ↓
         ┌──────────────────────────────┐
         │ 10. AFFICHAGE À L'ÉCRAN      │
         │     📱 Mise à jour UI        │
         │     🔄 Retour à étape 4      │
         └──────────────────────────────┘
```

**Performance temps réel** :
- Détection : 50ms
- OCR : 100ms (avec cache)
- API : 50ms (avec cache)
- Affichage : 10ms
- **Total : ~210ms → ~5 FPS** (acceptable pour UX)

---

## �📐 Plan de développement en phases

Le projet est divisé en **5 phases progressives** pour apprendre pas à pas :

### ✅ Phase 1 : P1 OCR Streamlit - Photo unique (EN COURS)
**Objectif** : Apprendre les bases fondamentales
- 📸 Upload photo → Détection → OCR → Matching → Affichage
- 🎓 **Apprentissage** : OCR (EasyOCR), API REST, YOLOv8, Streamlit
- ⏱️ **Durée** : 1-2 semaines
- 💡 **Pourquoi ?** Sans ces bases, impossible de faire le temps réel

**Fonctionnalités** :
- ✅ OCR sur tranches de livres
- ✅ Détection multiple (YOLOv8)
- ✅ Recherche par titre exact
- ✅ Recherche par thématique
- ✅ Enrichissement Open Library
- ✅ Affichage avec overlay

### 📅 Phase 2 : Orientation automatique
**Objectif** : Gérer les livres verticaux/horizontaux/inclinés
- 🔄 Détection de l'angle du texte
- ↩️ Rotation automatique des images
- 🎯 OCR robuste multi-angles
- 🎓 **Apprentissage** : Transformations d'images, rotation OpenCV
- ⏱️ **Durée** : 3-5 jours

**Fonctionnalités** :
- ✅ Détection d'angle avec Hough Transform
- ✅ Rotation automatique pré-OCR
- ✅ Amélioration précision OCR

### 📅 Phase 3 : Optimisation et cache
**Objectif** : Améliorer les performances
- ⚡ Cache intelligent pour OCR
- � Base de données locale (SQLite)
- 🔄 Requêtes batch pour l'API
- 📊 Métriques de performance
- 🎓 **Apprentissage** : Optimisation, caching, profiling
- ⏱️ **Durée** : 1 semaine

**Fonctionnalités** :
- ✅ Cache des résultats OCR
- ✅ Cache des résultats API
- ✅ Détection de frames similaires
- ✅ Réduction temps de traitement

### 📅 Phase 4 : Interface mobile statique
**Objectif** : Porter l'app sur mobile (photo unique)
- 📱 App React Native ou Flutter
- � Capture photo native
- 🎨 Interface mobile optimisée
- � Gestion permissions caméra
- 🎓 **Apprentissage** : Mobile dev, UI/UX mobile
- ⏱️ **Durée** : 2 semaines

**Fonctionnalités** :
- ✅ Interface mobile native
- ✅ Capture et upload photo
- ✅ Affichage résultats optimisé mobile
- ✅ Mode hors-ligne (cache)

### 📅 Phase 5 : Temps réel et AR 🎯 (OBJECTIF FINAL)
**Objectif** : Application mobile en temps réel avec réalité augmentée
- 🎥 Flux vidéo caméra en continu (viser 5-10 FPS)
- ⚡ Détection + OCR + API optimisés pour mobile
- 🧠 Threading et async pour performance
- 🎨 Overlay AR (réalité augmentée) en temps réel
- 🔋 Optimisation batterie
- 💾 Cache intelligent multi-niveaux
- 🎓 **Apprentissage** : Temps réel, threading, optimisation mobile, AR
- ⏱️ **Durée** : 3-4 semaines

**Fonctionnalités** :
- ✅ Caméra en direct (stream vidéo)
- ✅ Détection temps réel (YOLOv8n mobile)
- ✅ OCR sélectif (nouveaux livres uniquement)
- ✅ Cache multi-niveaux (mémoire + SQLite)
- ✅ Overlay AR avec rectangles et textes
- ✅ Mode exploration (scan continu)
- ✅ Mode recherche (highlight en temps réel)
- ✅ Optimisation batterie (frame skipping intelligent)

**Défis techniques Phase 5** :
- ⚡ Performance : Traitement en ~200ms par frame
- 🧠 Threading : Détection + OCR + API en parallèle
- 💾 Cache : Éviter de retraiter les mêmes livres
- 🔋 Batterie : Ne pas analyser toutes les frames (1 frame sur 10)
- 📱 Mobile : Modèles légers (quantization, pruning)

---

## 💡 Pourquoi commencer par Phase 1 ?

### 🎓 Apprentissage progressif
```
Simple (Phase 1)  →  Complexe (Phase 5)
     ↓
Les bases de Phase 1 sont INDISPENSABLES pour Phase 5
```

### ✅ Validation rapide du concept
Avant de passer des semaines sur le mobile, on vérifie que :
- ✅ L'OCR fonctionne bien sur des tranches de livres
- ✅ L'API Open Library retourne de bons résultats
- ✅ Le concept est techniquement viable

### ♻️ Réutilisabilité du code
Le code de Phase 1 sera **réutilisé** en Phase 5 :
```python
# Phase 1 (desktop) - Code que tu écris maintenant
class BookOCR:
    def extract_text(image): ...

# Phase 5 (mobile) - Réutilisation avec optimisation
class MobileBookOCR(BookOCR):
    def extract_text_optimized(image): ...
```

### 🐛 Debugging plus facile
- Phase 1 : Tester sur ordinateur, debugger facilement
- Phase 5 : Mobile = plus complexe à debugger

**Stratégie** : Valide chaque brique séparément avant d'assembler !

---

## 📌 Vue d'ensemble technique

**ShelfReader** combine plusieurs technologies :
1. **Computer Vision** : Détection des tranches de livres
2. **OCR** : Reconnaissance optique de caractères
3. **API REST** : Récupération des métadonnées
4. **IA/ML** : Recommandations personnalisées
5. **Mobile** : Application native temps réel

---

## 🗂️ Phase 1 : P1 OCR Streamlit (OCR + API + Interface)

### Objectifs pédagogiques
- ✅ Comprendre l'OCR avec EasyOCR
- ✅ Structurer un projet Python propre
- ✅ Interroger une API REST
- ✅ Créer une interface avec Streamlit

### Architecture
```
ShelfReader/
├── ocr_module.py      # ← En cours de développement
├── api_client.py      # TODO
├── app.py             # TODO
├── torch_utils.py     # TODO (Phase 2)
├── requirements.txt   # ✅ Dépendances déjà installées
└── data/
    └── test_images/   # Images de test
```

---

## 📄 Fichier 1 : `ocr_module.py`

### 🎯 Rôle
Extraire le texte d'une image de tranche de livre

### 🔧 Technologies
- **EasyOCR** : Modèle PyTorch pré-entraîné pour la reconnaissance de texte
- **OpenCV (cv2)** : Traitement d'image (preprocessing)
- **NumPy** : Manipulation de matrices d'images
- **PIL/Pillow** : Gestion d'images (format Streamlit)

### 📚 Concepts clés

#### Pourquoi une classe ?
On encapsule la logique OCR dans une classe pour :
- ✅ Charger le modèle EasyOCR **une seule fois** (évite de recharger ~100 MB à chaque appel)
- ✅ Réutiliser facilement avec différentes configurations
- ✅ Garder un code propre et organisé
- ✅ Éviter les variables globales

**Analogie** : C'est comme avoir un scanner personnel. Tu l'allumes une fois (initialisation), puis tu scannes autant de documents que tu veux sans le rallumer.

---

### 🔍 Méthode 1 : `__init__(self, languages, confidence_threshold)`

#### 📖 Rôle
Initialiser le lecteur OCR et stocker la configuration

#### 💻 Code
```python
def __init__(self, languages, confidence_threshold):
    self.reader = easyocr.Reader(languages, gpu=True)
    self.confidence_threshold = confidence_threshold
```

#### 📝 Explications ligne par ligne

##### `self.reader = easyocr.Reader(languages, gpu=True)`

**Que fait cette ligne ?**
- Charge le modèle de deep learning EasyOCR
- Le modèle est un **réseau de neurones PyTorch** pré-entraîné sur des millions d'images

**Paramètres** :
- `languages` : Liste des langues à reconnaître (ex: `['fr', 'en']`)
  - `'fr'` = français
  - `'en'` = anglais
  - Supporte 80+ langues !

- `gpu=True` : Utilise le GPU si disponible (NVIDIA avec CUDA)
  - **Avec GPU** : ~10x plus rapide ⚡
  - **Sans GPU** : Fonctionne quand même, mais plus lent 🐌

**Pourquoi c'est lent la première fois ?**
1. Télécharge les poids du modèle depuis internet (~100 MB)
2. Charge le modèle en mémoire (GPU ou CPU)
3. Les appels suivants sont instantanés car le modèle est déjà chargé

**Stockage avec `self.`** :
- `self.reader` devient un **attribut de la classe**
- Accessible dans toutes les méthodes avec `self.reader`
- Reste en mémoire tant que l'objet existe

---

##### `self.confidence_threshold = confidence_threshold`

**Qu'est-ce que la confidence (confiance) ?**

Quand EasyOCR détecte du texte, il donne un **score de probabilité** :

| Score | Signification | Action |
|-------|---------------|--------|
| 0.0 - 0.3 | Très incertain (probablement du bruit) | ❌ Jeter |
| 0.3 - 0.5 | Incertain (peut-être du texte) | ⚠️ Suspect |
| 0.5 - 0.8 | Assez confiant | ✅ Garder |
| 0.8 - 1.0 | Très confiant | ✅✅ Excellent |

**Le threshold (seuil)** :
- Définit la **limite minimale** pour garder une détection
- Exemple : `threshold = 0.5` → on garde seulement les détections ≥ 50%

**Pourquoi filtrer ?**

EasyOCR peut détecter du "faux texte" :
- Ombres sur le mur
- Reflets de lumière
- Motifs qui ressemblent à du texte
- Bruit dans l'image

**Exemple concret** :
```python
# Configuration
ocr = BookOCR(languages=['fr', 'en'], confidence_threshold=0.5)

# EasyOCR détecte :
"Harry Potter"  → confidence: 0.95  → ✅ GARDÉ (≥ 0.5)
"J.K. Rowling"  → confidence: 0.87  → ✅ GARDÉ (≥ 0.5)
"x8$#"          → confidence: 0.23  → ❌ JETÉ (< 0.5)
"|||"           → confidence: 0.15  → ❌ JETÉ (< 0.5)
```

**Résultat** : Texte propre sans bruit ! ✨

---

### 🔍 Méthode 2 : `preprocess_image(self, image)`

#### 📖 Rôle
Améliorer la qualité de l'image avant l'OCR pour augmenter la précision de détection

#### 💻 Code
```python
def preprocess_image(self, image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)
    return equalized
```

#### 📝 Explications ligne par ligne

##### `gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)`

**Qu'est-ce que la conversion en niveaux de gris ?**

Une image couleur a **3 canaux** (BGR : Bleu, Vert, Rouge) :
```python
# Image couleur
pixel = [Bleu=255, Vert=0, Rouge=0]  # Pixel bleu
# Stockage : 3 valeurs par pixel

# Image grise
pixel = [128]  # Niveau de gris moyen
# Stockage : 1 valeur par pixel
```

**Pourquoi convertir en gris ?**

1. **Moins de données** : 3x moins d'informations à traiter
   - Couleur : hauteur × largeur × 3 canaux
   - Gris : hauteur × largeur × 1 canal

2. **Le texte n'a pas besoin de couleur**
   - Ce qui compte : la **forme** des lettres
   - La couleur est du **bruit** pour l'OCR

3. **Meilleure détection**
   - Le modèle se concentre sur les formes
   - Moins de distractions

**Analogie** : Quand tu lis un livre, tu ne regardes pas les couleurs de l'encre, tu regardes la forme des lettres.

**Exemple visuel** :
```
Image couleur :           Image grise :
🟦🟩🟥🟨 (beaucoup          ⬜⬛⬜⬛ (focus sur
d'informations)            les formes)
```

---

##### `equalized = cv2.equalizeHist(gray)`

**Qu'est-ce que l'égalisation d'histogramme ?**

Un **histogramme d'image** montre la distribution des niveaux de luminosité :
```
Histogramme :
Nombre de  │     
pixels     │  ▄▄▄
           │ ▆███▆
           │▇█████▇
           └──────────── Luminosité (0-255)
           Sombre → Clair
```

**Problème** : Photo prise dans une bibliothèque sombre
```
Mauvaise distribution :
Nombre de  │     
pixels     │ ████▆▄
           │ █████▆▄
           │ ███████
           └──────────── Luminosité
           Sombre → Clair
           ↑ Tout est dans les valeurs sombres !
```

**Solution** : `equalizeHist()` **redistribue** les niveaux de luminosité
```
Bonne distribution :
Nombre de  │     
pixels     │ ▄ ▄ ▄ ▄
           │ █ █ █ █
           │ █ █ █ █
           └──────────── Luminosité
           Sombre → Clair
           ↑ Réparti uniformément !
```

**Effet visuel** :
```
Avant égalisation :        Après égalisation :
😐 Texte peu visible       😃 Texte bien visible
🌑 Faible contraste        ☀️ Contraste élevé
```

**Pourquoi c'est utile pour l'OCR ?**
- Augmente le **contraste** entre le texte et le fond
- Le texte devient **plus net**
- Le modèle détecte mieux les lettres

**Analogie** : C'est comme mettre des lunettes ou augmenter la luminosité de ton écran. Le contenu est le même, mais tu le vois beaucoup mieux.

---

##### `return equalized`

**Pourquoi retourner l'image ?**

Une fonction doit **retourner** son résultat pour qu'on puisse l'utiliser :

```python
# Sans return (❌ ERREUR) :
def preprocess_image(self, image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)
    # Pas de return → résultat perdu !

# Utilisation :
result = self.preprocess_image(image)
print(result)  # None (rien !) ❌

# Avec return (✅ CORRECT) :
def preprocess_image(self, image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)
    return equalized  # On retourne le résultat

# Utilisation :
result = self.preprocess_image(image)
print(result)  # numpy array (l'image traitée) ✅
```

**Pourquoi retourner `equalized` et pas `gray` ?**
- `gray` = image en niveaux de gris (première étape)
- `equalized` = image en gris + contraste amélioré (étape finale)
- On veut l'image la **plus optimisée** pour l'OCR

---

### 🔍 Méthode 3 : `extract_text_from_pil(self, pil_image, preprocess=True)`

#### 📖 Rôle
Pipeline complet : image → conversions → preprocessing → OCR → texte nettoyé

#### ⚠️ Problème à résoudre : Les formats d'image

En Python, il existe **3 formats différents** pour représenter une image :

| Format | Type | Couleurs | Utilisé par |
|--------|------|----------|-------------|
| PIL/Pillow | `PIL.Image` | RGB | Streamlit, web, Matplotlib |
| NumPy array | `numpy.ndarray` | RGB/BGR | PyTorch, calculs |
| OpenCV | `numpy.ndarray` | **BGR** | OpenCV, EasyOCR |

**Le problème** : Streamlit donne une image PIL (RGB), mais EasyOCR veut un array NumPy (BGR) !

**La solution** : On doit faire 2 conversions :
1. PIL → NumPy array
2. RGB → BGR

---

#### 💻 Partie 1 : Conversions de format

```python
image_array = np.array(pil_image)
bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
```

##### `image_array = np.array(pil_image)`

**Conversion PIL → NumPy**

```python
# Avant (format PIL) :
pil_image = <PIL.Image.Image object at 0x7f8b...>
type(pil_image)  # <class 'PIL.Image.Image'>

# Après (format NumPy) :
image_array = np.array(pil_image)
type(image_array)  # <class 'numpy.ndarray'>
image_array.shape  # (1080, 1920, 3) pour une image Full HD
```

**Structure d'un array NumPy** :
```python
# Dimensions : (hauteur, largeur, canaux)
image_array.shape = (1080, 1920, 3)
                     ↑     ↑     ↑
                   hauteur  largeur  3 canaux RGB

# Exemple de pixels :
image_array[0, 0]  # [255, 0, 0] = pixel rouge en haut à gauche
image_array[0, 1]  # [0, 255, 0] = pixel vert à côté
```

**Pourquoi faire ça ?**
- PIL est un format **haut niveau** (orienté objet)
- NumPy est un format **bas niveau** (matrices de nombres)
- OpenCV et EasyOCR travaillent avec NumPy

**Analogie** : C'est comme convertir un document Word en PDF pour qu'une autre application puisse le lire.

---

##### `bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)`

**Conversion RGB → BGR**

**Pourquoi OpenCV utilise BGR ?**
- Raison **historique** : OpenCV créé en 1999 pour des caméras qui utilisaient BGR
- Aujourd'hui c'est bizarre mais on doit vivre avec 😅

**Différence RGB vs BGR** :

```python
# Pixel ROUGE en RGB (PIL/Streamlit) :
pixel_rgb = [Rouge=255, Vert=0, Bleu=0]
             [0]=R     [1]=G  [2]=B

# Même pixel ROUGE en BGR (OpenCV) :
pixel_bgr = [Bleu=0, Vert=0, Rouge=255]
             [0]=B   [1]=G   [2]=R
```

**Exemple visuel** :
```
Image RGB (PIL) :          Image BGR (OpenCV) :
[🔴, 🟢, 🔵]               [🔵, 🟢, 🔴]
 R   G   B                  B   G   R
```

**Que fait `cv2.cvtColor()` ?**
- Inverse l'ordre des canaux : RGB → BGR
- Le pixel `[255, 0, 0]` devient `[0, 0, 255]`
- Les couleurs restent les mêmes visuellement

**Si on ne fait pas cette conversion** :
```python
# Sans conversion :
# OpenCV pense que [255, 0, 0] = BLEU (au lieu de ROUGE)
# L'image aurait les mauvaises couleurs
# L'OCR pourrait être perturbé
```

---

#### 💻 Partie 2 : Preprocessing conditionnel

```python
if preprocess:
    image = self.preprocess_image(bgr_image)
else:
    image = bgr_image
```

**Pourquoi un paramètre `preprocess` ?**

1. **Flexibilité** : Tester avec/sans preprocessing
2. **Debug** : Si l'OCR échoue, essayer sans preprocessing
3. **Performance** : Sur de bonnes photos, le preprocessing n'est pas toujours nécessaire

**Exemples d'utilisation** :
```python
# Photo nette, bien éclairée :
text = ocr.extract_text_from_pil(image, preprocess=False)
# → Pas besoin de preprocessing, économise du temps

# Photo sombre, floue :
text = ocr.extract_text_from_pil(image, preprocess=True)
# → Preprocessing recommandé pour améliorer la qualité
```

**Le `if/else` en détail** :
```python
if preprocess:  # Si preprocess == True
    image = self.preprocess_image(bgr_image)  # Applique gris + égalisation
else:  # Si preprocess == False
    image = bgr_image  # Garde l'image originale (BGR)
```

---

#### 💻 Partie 3 : Appel EasyOCR

```python
results = self.reader.readtext(image)
```

**Que fait `readtext()` ?**

C'est le **cœur du système** : le modèle PyTorch analyse l'image et détecte le texte.

**Structure du résultat** :

`results` est une **liste de tuples** :
```python
results = [
    (bbox1, text1, confidence1),
    (bbox2, text2, confidence2),
    ...
]
```

**Détail de chaque tuple** :
```python
result = (
    [[x1,y1], [x2,y2], [x3,y3], [x4,y4]],  # bbox : 4 coins du rectangle
    "Harry Potter",                         # text : texte détecté
    0.95                                    # confidence : score 0-1
)
```

**Accès aux éléments** :
```python
result[0]  # bbox (coordonnées)
result[1]  # text (le texte)
result[2]  # confidence (score)
```

**Exemple concret** :
```python
results = [
    ([[10,20], [200,20], [200,60], [10,60]], "Harry Potter", 0.95),
    ([[10,70], [180,70], [180,100], [10,100]], "J.K. Rowling", 0.87),
    ([[10,110], [50,110], [50,130], [10,130]], "x8$#", 0.23),  # Bruit
    ([[10,140], [40,140], [40,160], [10,160]], "|||", 0.15)    # Ombre
]
```

**Visualisation** :
```
┌─────────────────────────────┐
│  Harry Potter       95%  ✅ │
│  J.K. Rowling       87%  ✅ │
│  x8$#               23%  ❌ │
│  |||                15%  ❌ │
└─────────────────────────────┘
```

---

#### 💻 Partie 4 : Filtrage par confidence (TODO 3)

```python
filtered_results = [r for r in results if r[2] >= self.confidence_threshold]
```

**Objectif** : Éliminer les fausses détections (bruit, ombres, reflets)

**Comment ça marche ?**

1. On parcourt chaque résultat `r` dans `results`
2. On regarde la confiance : `r[2]`
3. On teste si `r[2] >= self.confidence_threshold`
4. On garde seulement les résultats qui passent le test

**Accès à la confidence** :
```python
result = (bbox, text, confidence)
          [0]   [1]   [2]

confidence = result[2]  # Accès au 3ème élément
```

**List comprehension expliquée** :
```python
# Version courte (Pythonic) ✅ :
filtered_results = [r for r in results if r[2] >= self.confidence_threshold]

# Version longue (équivalente) :
filtered_results = []
for r in results:
    if r[2] >= self.confidence_threshold:
        filtered_results.append(r)
```

**Décomposition** :
```python
[r                              # Valeur à garder
 for r in results               # Pour chaque r dans results
 if r[2] >= self.confidence_threshold]  # Condition de filtrage
```

**Exemple pas à pas** :

```python
# Configuration
self.confidence_threshold = 0.5  # Seuil à 50%

# Résultats EasyOCR
results = [
    (bbox, "Harry Potter", 0.95),  # Test : 0.95 ≥ 0.5 ? → OUI ✅
    (bbox, "J.K. Rowling", 0.87),  # Test : 0.87 ≥ 0.5 ? → OUI ✅
    (bbox, "x8$#", 0.23),          # Test : 0.23 ≥ 0.5 ? → NON ❌
    (bbox, "|||", 0.15)            # Test : 0.15 ≥ 0.5 ? → NON ❌
]

# Après filtrage
filtered_results = [
    (bbox, "Harry Potter", 0.95),
    (bbox, "J.K. Rowling", 0.87)
]
```

**Visualisation** :
```
Avant filtrage :               Après filtrage :
┌─────────────────────┐       ┌─────────────────────┐
│ "Harry Potter" 95%  │ ✅ →  │ "Harry Potter" 95%  │
│ "J.K. Rowling" 87%  │ ✅ →  │ "J.K. Rowling" 87%  │
│ "x8$#"         23%  │ ❌    │                     │
│ "|||"          15%  │ ❌    │                     │
└─────────────────────┘       └─────────────────────┘
```

**Pourquoi c'est crucial ?**
- Sans filtrage : `"Harry Potter J.K. Rowling x8$# |||"` → **Pollué** 💩
- Avec filtrage : `"Harry Potter J.K. Rowling"` → **Propre** ✨

---

#### 💻 Partie 5 : Extraction des textes (TODO 4)

```python
texts = [r[1] for r in filtered_results]
```

**Objectif** : Extraire seulement les textes (ignorer bbox et confidence)

**Que contient `filtered_results` ?**

Après le TODO 3, on a les détections fiables :
```python
filtered_results = [
    (bbox1, "Harry Potter", 0.95),
    (bbox2, "J.K. Rowling", 0.87)
]
```

Chaque élément est un tuple avec 3 parties :
- `r[0]` = bbox → On n'en a **pas besoin**
- `r[1]` = text → **C'est ce qu'on veut !** ✅
- `r[2]` = confidence → Déjà utilisée pour filtrer

**Accès au texte** :
```python
result = (bbox, text, confidence)
          [0]   [1]   [2]

texte = result[1]  # "Harry Potter"
```

**List comprehension** :
```python
texts = [r[1] for r in filtered_results]

# Équivalent :
texts = []
for r in filtered_results:
    texts.append(r[1])
```

**Exemple pas à pas** :
```python
filtered_results = [
    (bbox1, "Harry Potter", 0.95),
    (bbox2, "J.K. Rowling", 0.87)
]

# Extraction :
texts = [r[1] for r in filtered_results]

# Itération 1 : r = (bbox1, "Harry Potter", 0.95)
#               r[1] = "Harry Potter" → ajouté

# Itération 2 : r = (bbox2, "J.K. Rowling", 0.87)
#               r[1] = "J.K. Rowling" → ajouté

# Résultat :
texts = ["Harry Potter", "J.K. Rowling"]
```

**Visualisation** :
```
Avant (tuples complexes) :     Après (liste simple) :
┌─────────────────────────┐   ┌─────────────────────┐
│ (bbox, "Harry", 0.95)   │ → │ "Harry Potter"      │
│ (bbox, "Rowling", 0.87) │ → │ "J.K. Rowling"      │
└─────────────────────────┘   └─────────────────────┘
```

**Pourquoi ?**
- Plus simple à manipuler
- Prépare pour TODO 5 (combinaison)

---

#### 💻 Partie 6 : Combinaison des textes (TODO 5)

```python
full_text = ' '.join(texts)
```

**Objectif** : Fusionner tous les textes en une seule chaîne

**Comment fonctionne `join()` ?**

`join()` est une méthode des strings qui **colle** les éléments d'une liste :

```python
separateur.join(liste)
```

**Exemples** :
```python
# Avec espace :
' '.join(["Harry", "Potter"])  # "Harry Potter"

# Avec tiret :
'-'.join(["2024", "10", "02"])  # "2024-10-02"

# Avec virgule :
', '.join(["pomme", "banane", "orange"])  # "pomme, banane, orange"

# Sans séparateur :
''.join(["A", "B", "C"])  # "ABC"
```

**Notre cas** :
```python
texts = ["Harry Potter", "J.K. Rowling", "Tome 1"]

full_text = ' '.join(texts)
# full_text = "Harry Potter J.K. Rowling Tome 1"
```

**Pourquoi un espace comme séparateur ?**
- Les mots doivent être séparés pour la recherche API
- `"HarryPotterJ.K.Rowling"` → ❌ Illisible
- `"Harry Potter J.K. Rowling"` → ✅ Lisible

**Visualisation** :
```
Avant :                    Après :
┌─────────────────────┐   ┌─────────────────────────────────┐
│ ["Harry Potter",    │   │ "Harry Potter J.K. Rowling"     │
│  "J.K. Rowling"]    │ → │                                 │
└─────────────────────┘   └─────────────────────────────────┘
```

**Pourquoi c'est utile ?**
- EasyOCR détecte chaque ligne séparément
- L'API a besoin d'un texte complet
- Plus facile à afficher à l'utilisateur

---

#### 💻 Partie 7 : Calcul de la confiance moyenne (TODO 6)

```python
if len(filtered_results) > 0:
    avg_confidence = sum([r[2] for r in filtered_results]) / len(filtered_results)
else:
    avg_confidence = 0.0
```

**Objectif** : Calculer la confiance globale de l'OCR

**Formule de la moyenne** :
```
Moyenne = (somme des valeurs) / (nombre de valeurs)
```

**Pourquoi c'est important ?**
- Savoir si l'OCR a bien fonctionné
- Prévenir l'utilisateur si le résultat est incertain
- Décider si on doit demander une nouvelle photo

**Échelle d'interprétation** :
| Confiance moyenne | Interprétation | Action |
|-------------------|----------------|--------|
| 0.9 - 1.0 | Excellent | ✅ Très fiable |
| 0.7 - 0.9 | Bon | ✅ Fiable |
| 0.5 - 0.7 | Moyen | ⚠️ Vérifier |
| 0.0 - 0.5 | Mauvais | ❌ Redemander photo |

**Exemple de calcul** :
```python
filtered_results = [
    (bbox, "Harry Potter", 0.95),
    (bbox, "J.K. Rowling", 0.87)
]

# Étape 1 : Extraire les confidences
confidences = [r[2] for r in filtered_results]  # [0.95, 0.87]

# Étape 2 : Calculer la somme
total = sum(confidences)  # 0.95 + 0.87 = 1.82

# Étape 3 : Compter le nombre d'éléments
count = len(filtered_results)  # 2

# Étape 4 : Calculer la moyenne
avg = total / count  # 1.82 / 2 = 0.91 (91%)
```

**Pourquoi `if len(filtered_results) > 0` ?**

**Problème** : Division par zéro !
```python
# Si aucun texte n'est détecté :
filtered_results = []

# Sans protection :
avg = sum([...]) / len(filtered_results)  # X / 0 → ERREUR ! 💥

# Avec protection :
if len(filtered_results) > 0:
    avg = sum([...]) / len(filtered_results)
else:
    avg = 0.0  # Aucun texte → confiance nulle
```

**Décomposition du calcul** :
```python
# Liste des confidences :
confidences = [r[2] for r in filtered_results]
# [0.95, 0.87]

# Somme :
total = sum(confidences)
# sum([0.95, 0.87]) = 1.82

# Nombre :
count = len(filtered_results)
# 2

# Moyenne :
avg_confidence = total / count
# 1.82 / 2 = 0.91
```

**Version condensée (notre code)** :
```python
avg_confidence = sum([r[2] for r in filtered_results]) / len(filtered_results)
#                ↑ Calcule la somme                     ↑ Divise par le nombre
```

---

#### 💻 Partie 8 : Retour du résultat (TODO 7)

```python
return (full_text, avg_confidence)
```

**Objectif** : Retourner les 2 informations importantes

**Pourquoi un tuple ?**

On veut retourner **2 valeurs** :
1. Le texte détecté
2. La confiance moyenne

**Options en Python** :
```python
# Option 1 : Tuple (recommandé) ✅
return (texte, confiance)

# Option 2 : Liste
return [texte, confiance]

# Option 3 : Dictionnaire
return {'text': texte, 'confidence': confiance}
```

**Pourquoi choisir un tuple ?**
- ✅ Léger et rapide
- ✅ Immutable (ne peut pas être modifié accidentellement)
- ✅ Convention Python pour retourner plusieurs valeurs
- ✅ Unpacking facile

**Utilisation du tuple** :
```python
# Appel de la méthode :
result = ocr.extract_text_from_pil(image)
# result = ("Harry Potter J.K. Rowling", 0.91)

# Accès par index :
texte = result[0]      # "Harry Potter J.K. Rowling"
confiance = result[1]  # 0.91

# Unpacking (plus élégant) :
texte, confiance = ocr.extract_text_from_pil(image)
# texte = "Harry Potter J.K. Rowling"
# confiance = 0.91

# Utilisation :
print(f"Texte : {texte}")
print(f"Confiance : {confiance:.2%}")

# Affichage :
# Texte : Harry Potter J.K. Rowling
# Confiance : 91.00%
```

**Exemple complet** :
```python
# Code complet :
def extract_text_from_pil(self, pil_image, preprocess=True):
    # ... tout le traitement ...
    full_text = "Harry Potter J.K. Rowling"
    avg_confidence = 0.91
    
    return (full_text, avg_confidence)

# Utilisation dans app.py :
texte, confiance = ocr.extract_text_from_pil(image)

if confiance > 0.8:
    print(f"✅ OCR fiable : {texte}")
else:
    print(f"⚠️ OCR incertain : {texte}")
```

---

## 🎯 Récapitulatif complet du pipeline

```python
def extract_text_from_pil(self, pil_image, preprocess=True):
    # 1. Conversions de format
    image_array = np.array(pil_image)              # PIL → NumPy
    bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)  # RGB → BGR
    
    # 2. Preprocessing (optionnel)
    if preprocess:
        image = self.preprocess_image(bgr_image)   # Gris + contraste
    else:
        image = bgr_image
    
    # 3. OCR
    results = self.reader.readtext(image)          # Détection texte
    
    # 4. Filtrage
    filtered_results = [r for r in results if r[2] >= self.confidence_threshold]
    
    # 5. Extraction
    texts = [r[1] for r in filtered_results]       # Seulement les textes
    
    # 6. Combinaison
    full_text = ' '.join(texts)                    # Un seul string
    
    # 7. Confiance moyenne
    if len(filtered_results) > 0:
        avg_confidence = sum([r[2] for r in filtered_results]) / len(filtered_results)
    else:
        avg_confidence = 0.0
    
    # 8. Retour
    return (full_text, avg_confidence)
```

**Flux de données** :
```
PIL Image (RGB)
    ↓ np.array()
NumPy array (RGB)
    ↓ cv2.cvtColor()
NumPy array (BGR)
    ↓ preprocess_image() [optionnel]
Image grise équalisée
    ↓ reader.readtext()
[(bbox, "Harry Potter", 0.95), (bbox, "J.K. Rowling", 0.87), ...]
    ↓ filtrage par confidence
[(bbox, "Harry Potter", 0.95), (bbox, "J.K. Rowling", 0.87)]
    ↓ extraction des textes
["Harry Potter", "J.K. Rowling"]
    ↓ join()
"Harry Potter J.K. Rowling"
    ↓ + calcul moyenne
("Harry Potter J.K. Rowling", 0.91)
```

---

## ✅ Checklist de compréhension

Avant de passer au fichier suivant, assure-toi de comprendre :

### Concepts généraux
- [ ] Pourquoi on utilise une classe pour l'OCR
- [ ] Pourquoi on charge le modèle dans `__init__`
- [ ] Ce qu'est la confidence et pourquoi on filtre

### Preprocessing
- [ ] Pourquoi convertir en niveaux de gris
- [ ] Comment fonctionne l'égalisation d'histogramme
- [ ] Quand utiliser ou non le preprocessing

### Conversions de format
- [ ] Différence entre PIL, NumPy et OpenCV
- [ ] Pourquoi convertir PIL → NumPy → BGR
- [ ] Différence entre RGB et BGR

### Pipeline OCR
- [ ] Structure du résultat EasyOCR (bbox, text, confidence)
- [ ] Comment filtrer par confidence avec list comprehension
- [ ] Comment extraire les textes avec `r[1]`
- [ ] Comment combiner avec `join()`
- [ ] Comment calculer une moyenne
- [ ] Pourquoi gérer la division par zéro
- [ ] Pourquoi retourner un tuple

---

## 🎯 TODO à compléter dans ton code

Maintenant que tu comprends tout, **complète les TODO 4-7** dans `ocr_module.py` :

```python
# TODO 4 : Extraire tous les textes
texts = [r[1] for r in filtered_results]

# TODO 5 : Combiner les textes
full_text = ' '.join(texts)

# TODO 6 : Calculer confiance moyenne
if len(filtered_results) > 0:
    avg_confidence = sum([r[2] for r in filtered_results]) / len(filtered_results)
else:
    avg_confidence = 0.0

# TODO 7 : Retourner (texte, confiance)
return (full_text, avg_confidence)
```

**⚠️ Attention** : Change `filtered_result` (singulier) en `filtered_results` (pluriel) dans TODO 3 pour cohérence !

---

## 📝 Notes personnelles

(Espace pour tes propres notes, questions et observations)

### Questions à explorer
- Quelle est la différence de performance avec/sans preprocessing ?
- Quel est le meilleur threshold pour mes images ?
- Comment gérer le texte vertical (tranches de livres) ?

### Bugs rencontrés


### Améliorations possibles


---

## 🚀 Prochaines étapes

1. ✅ Compléter `ocr_module.py` (TODO 4-7)
2. ⏭️ Créer `api_client.py` (recherche Open Library)
3. ⏭️ Créer `app.py` (interface Streamlit)
4. ⏭️ Tester le MVP complet

---

**Dernière mise à jour** : 2 octobre 2025  
**Statut** : TODO 1-3 expliqués, TODO 4-7 à coder  
**Fichier suivant** : `api_client.py`
