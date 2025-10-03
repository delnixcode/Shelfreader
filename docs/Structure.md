# 📂 Structure du projet ShelfReader

Ce document centralise la vision, la roadmap, la structure et les bonnes pratiques pour garantir la portabilité PC/mobile et la clarté du projet.

---

## � Sommaire

- [🗺️ Roadmap & Projets](#-roadmap--projets)
- [🔄 Réutilisabilité du code](#-réutilisabilité-du-code)
- [📚 Vue d'ensemble technique](#-vue-densemble-technique)
- [ Projets détaillés](#-projets-détaillés)
- [🏗️ Projet 1 : MVP Desktop (OCR + API + Interface)](#️-projet-1--mvp-desktop-ocr--api--interface)
- [� Projet 3 : Mobile Static - Portage Mobile & Interface Native](#-projet-3--mobile-static---portage-mobile--interface-native)
- [� Projet 4 : Mobile Real-time - AR + Performance + Intelligence](#-projet-4--mobile-real-time---ar--performance--intelligence)

---

## �🗺️ Roadmap & Phases

### Projet 1 : MVP Desktop (OCR + API + Interface)
- Implémentation du module OCR
- Client API pour Open Library
- Interface Streamlit pour upload et résultats
- Tests unitaires et end-to-end

### Projet 2 : Enhanced Desktop (Optimisation)
- Orientation automatique des images
- Cache intelligent pour OCR et API
- Optimisation des performances
- Métriques et profiling

### Projet 3 : Mobile Static
- Interface mobile native (React Native/Flutter)
- Capture photo statique sur mobile
- Portage des fonctionnalités desktop
- Mode hors-ligne avec cache

### Projet 4 : Mobile Real-time (Final)
- Flux vidéo en continu
- Détection temps réel avec YOLOv8n
- OCR sélectif et cache multi-niveaux
- Overlay AR et recommandations IA

---

## 🔄 Réutilisabilité du code

Tout le code développé pour les phases PC (API, OCR, logique de recherche, visualisation) doit être conçu pour être réutilisable sur mobile :
- Les modules Python (API, OCR) doivent être indépendants de l'interface (web ou mobile).
- La logique métier (détection, filtrage, surlignage) doit être séparée de la présentation.
- Les fonctions et classes doivent pouvoir être importées et utilisées dans une app mobile (ex : Kivy, BeeWare, Flutter/Python, React Native/Python).
- Les tests unitaires doivent valider le fonctionnement sur toutes les plateformes.

---

## 📚 Vue d'ensemble technique

**ShelfReader** combine plusieurs technologies :
1. **Computer Vision** : Détection des tranches de livres
2. **OCR** : Reconnaissance optique de caractères
3. **API REST** : Récupération des métadonnées
4. **IA/ML** : Recommandations personnalisées
5. **Mobile** : Application native temps réel

---

## 📐 Projets détaillés

Le projet **ShelfReader** est organisé en **4 projets autonomes et progressifs**, chacun représentant une étape complète du développement. Contrairement à une approche linéaire, chaque projet peut être lu et compris indépendamment, avec tous les contextes, objectifs et détails techniques intégrés.

### 📋 Organisation des projets

Chaque projet contient :
- **🎯 Vue d'ensemble** : Contexte et objectifs pédagogiques
- **📋 Roadmap & Phases** : Plan de développement détaillé
- **🏗️ Architecture** : Structure technique et flux de données
- **🛠️ Technologies** : Stack technique et environnement
- **🎯 Défis techniques** : Problèmes à résoudre et solutions
- **�� Architecture d'intégration** : Pipeline complet et implémentation

### 📚 Projets disponibles

| Projet | Focus | Technologies clés | Durée estimée |
|--------|-------|-------------------|---------------|
| **🏗️ [Projet 1 : MVP Desktop](docs/project1/)** | OCR + API + Interface | EasyOCR, OpenCV, Streamlit | 2-3 semaines |
| **⚡ [Projet 2 : Enhanced Desktop](docs/project2/)** | YOLOv8 + Optimisations | YOLOv8, Redis, Métriques | 3-4 semaines |
| **📱 [Projet 3 : Mobile Static](docs/project3/)** | Portage mobile + Native UI | React Native/Flutter, SQLite | 4-5 semaines |
| **🚀 [Projet 4 : Mobile Real-time](docs/project4/)** | AR temps réel + Performance | ARCore/ARKit, TensorFlow Lite | 5-6 semaines |

### 🎯 Approche pédagogique

- **Autonomie** : Chaque projet est auto-suffisant et peut être abordé indépendamment
- **Progression** : Complexité croissante des technologies et concepts
- **Réutilisation** : Code et apprentissages transférables entre projets
- **Validation** : Chaque projet valide une hypothèse technique ou fonctionnelle

### 📖 Comment utiliser cette documentation

1. **Pour débuter** : Commencer par le [Projet 1](project1.md) pour les bases
2. **Pour approfondir** : Suivre la séquence 1→2→3→4 pour une progression complète
3. **Pour référence** : Consulter n'importe quel projet selon les besoins spécifiques
4. **Pour contribution** : Chaque projet peut être développé indépendamment

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

## 🔄 Workflows par projet

Chaque projet ShelfReader a son propre workflow adapté à ses besoins spécifiques :

### 📸 **Workflow Projet 1 : MVP Desktop - Photo unique**

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
│    📸 Upload photo étagère                      │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 4. PRÉPROCESSING                                │
│    � Conversion et optimisation image          │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 5. OCR (EasyOCR)                                │
│    📝 Extraction texte de chaque tranche        │
│    Livre1: "Python Crash Course"                │
│    Livre2: "Java Programming"                   │
│    Livre3: "Learning Python"                    │
│    Livre4: "Django for Beginners"               │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 6. ENRICHISSEMENT (Open Library API)            │
│    🌐 Récupération métadonnées                  │
│    Livre1: ["Python", "Programming"]            │
│    Livre2: ["Java", "Programming"]              │
│    Livre3: ["Python", "Beginner"]               │
│    Livre4: ["Python", "Django", "Web"]          │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 7. MATCHING                                     │
│    🎯 Recherche thématique : "Python"           │
│    ✅ Livre1: "Python" dans titre + catégories  │
│    ❌ Livre2: "Java" (pas de match)             │
│    ✅ Livre3: "Python" dans titre + catégories  │
│    ✅ Livre4: "Python" + "Django" dans catégories│
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 8. AFFICHAGE RÉSULTATS                          │
│    📊 Liste des livres trouvés                  │
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

### 🎥 **Workflow Projet 4 : Mobile Real-time - AR temps réel**

```
┌─────────────────────────────────────────────────┐
│ 1. LANCEMENT APP                                │
│    📱 Ouverture application mobile               │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 2. ACTIVATION CAMÉRA                            │
│    🎥 Flux vidéo continu (30 FPS)               │
│    📸 Stream : frame 1, frame 2, frame 3...     │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ 3. BOUCLE TEMPS RÉEL                            │
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
         │ 9. OVERLAY AR                │
         │    🎨 Rectangles sur livres  │
         │    📝 Titres lisibles        │
         │    ⭐ Scores (si recherche)  │
         │    ⏱️ ~10ms                  │
         └──────────────────────────────┘
                        ↓
         ┌──────────────────────────────┐
         │ 10. AFFICHAGE ÉCRAN          │
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

## 📐 Projets détaillés

Le projet est divisé en **4 projets progressifs** pour apprendre pas à pas :

| Projet | Nom | Description | Statut | Durée | Fichier |
|--------|-----|-------------|--------|-------|---------|
| **1** | ✅ MVP Desktop | OCR + API + Interface web | EN COURS | 2 semaines | [project1.md](project1.md) |
| **2** | Enhanced Desktop | YOLOv8 + Orientation + Cache | À FAIRE | 3 semaines | [project2.md](project2.md) |
| **3** | Mobile Static | Portage mobile + Hors-ligne | À FAIRE | 4 semaines | [project3.md](project3.md) |
| **4** | 🚀 Mobile Real-time | AR temps réel + Performance | OBJECTIF | 5 semaines | [project4.md](project4.md) |

Chaque projet est documenté dans son propre fichier pour une lecture autonome.

---

## 🏗️ Vision finale du projet