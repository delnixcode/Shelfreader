# 🧠 ShelfReader - Memories & Guidelines

## 🚀 Démarrage Rapide - État Actuel

## 📅 **Session** : 3 Octobre 2025
## 📊 **Statut** : Framework de développement établi, prêt pour implémentation

### 🎯 **Résumé Express**
**ShelfReader** : App mobile computer vision pour détecter des livres en temps réel sur étagère.

**4 projets indépendants** :
- **P1** : MVP Desktop (OCR + API + Streamlit) ✅ Framework prêt
- **P2** : Enhanced Desktop (YOLOv8 + Cache) ✅ Framework prêt
- **P3** : Mobile Static (Kivy + Offline) ✅ Framework prêt
- **P4** : Mobile Real-time (AR + Tracking) ✅ Framework prêt

### 🔥 **Prochaines Actions Prioritaires**
1. **Choisir un projet** (P1 recommandé pour débuter)
2. **Lire le `TODO.md`** correspondant
3. **Créer environnement virtuel** pour le projet choisi
4. **Installer dépendances** depuis requirements.txt

### 🛠️ **Commandes Essentielles**
```bash
# Environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Installation
pip install -r requirements.txt

# Tests
pytest tests/
black --check .
flake8 .
```

### 📂 **Fichiers Clés**
- `docs/Dependencies.md` - Catalogue des 118 bibliothèques
- `docs/Structure.md` - Roadmap globale
- `pX-*/TODO.md` - Plan détaillé par projet

---

## 📋 Mission du Projet
**ShelfReader** est une application mobile de computer vision en temps réel qui permet de détecter et rechercher des livres sur une étagère. L'utilisateur pointe son téléphone vers une étagère et l'app détecte automatiquement les livres, lit les titres via OCR, et fournit des recommandations personnalisées.

## 🏗️ Structure du Projet
```
ShelfReader/
├── README.md                    # Aperçu général du projet
├── requirements.txt             # TOUTES les dépendances (118 libs)
├── docs/                        # Documentation complète
│   ├── Dependencies.md          # Guide détaillé des bibliothèques
│   ├── Structure.md             # Roadmap & organisation
│   ├── p1-MVP-Desktop.md        # Documentation Projet 1
│   ├── p2-Enhanced-Desktop.md   # Documentation Projet 2
│   ├── p3-Mobile-Static.md      # Documentation Projet 3
│   └── p4-Mobile-Real-time.md   # Documentation Projet 4
├── p1-MVP-Desktop/             # Phase 1 : OCR + API + Streamlit
├── p2-Enhanced-Desktop/        # Phase 2 : YOLOv8 + Cache
├── p3-Mobile-Static/           # Phase 3 : Mobile natif + Offline
└── p4-Mobile-Real-time/        # Phase 4 : AR temps réel
```

## 🎯 Règles de Développement

### 📝 Principes DRY (Don't Repeat Yourself)
- **Pas de duplication de code** : Chaque fonctionnalité doit être implémentée une seule fois
- **Modules réutilisables** : Créer des fonctions/classes génériques
- **Configuration centralisée** : Paramètres dans des fichiers dédiés
- **Héritage et composition** : Réutiliser le code existant intelligemment

### 🧹 Code Propre
- **PEP 8** : Respecter les conventions Python
- **Nommage explicite** : Variables, fonctions, classes avec noms significatifs
- **Documentation** : Docstrings pour toutes les fonctions/classes publiques
- **Séparation des responsabilités** : Une fonction/classe = une responsabilité
- **Tests unitaires** : Couvrir les fonctionnalités critiques
- **Gestion d'erreurs** : Exceptions appropriées avec messages clairs

### 🔧 Bonnes Pratiques
- **Type hints** : Annotations de type pour la lisibilité
- **Logging** : Utiliser `logging` au lieu de `print`
- **Configuration** : Variables d'environnement pour les paramètres
- **Validation** : Vérifier les inputs et gérer les cas d'erreur
- **Performance** : Optimiser les boucles et les accès mémoire
- **Sécurité** : Validation des inputs utilisateur

## 📊 Workflow de Développement

1. **Lire la documentation** du projet dans `docs/pX-*.md`
2. **Développer itérativement** : petit pas par petit pas
3. **Tester régulièrement** : validation continue
4. **Commiter fréquemment** : sauvegarde progressive

### 📝 TODO par Projet
Chaque projet doit avoir un fichier `TODO.md` qui détaille :
- **Fichiers à créer/modifier**
- **Fonctionnalités à implémenter**
- **Raison/justification** de chaque choix
- **Dépendances** entre tâches
- **Critères d'acceptation**

## 📋 TODOs par Projet

### Structure des TODOs
Chaque projet possède un fichier `TODO.md` détaillé qui guide le développement :
- **Vue d'ensemble du projet** : Objectifs, technologies, durée estimée
- **Structure du projet** : Hiérarchie complète des dossiers et fichiers
- **Analyse par fichier** : Chaque fichier source expliqué avec TODOs spécifiques
- **Justification technique** : Pourquoi chaque choix et approche
- **Workflow de développement** : Phases séquentielles avec dépendances
- **Critères d'acceptation** : Conditions de validation objectives

### TODOs Disponibles
- ✅ **P1 - MVP Desktop** : `p1-MVP-Desktop/TODO.md` - Interface Streamlit + OCR + API
- ✅ **P2 - Enhanced Desktop** : `p2-Enhanced-Desktop/TODO.md` - YOLOv8 + Cache Redis + Métriques
- ✅ **P3 - Mobile Static** : `p3-Mobile-Static/TODO.md` - Kivy + TFLite + SQLite hors-ligne
- ✅ **P4 - Mobile Real-time** : `p4-Mobile-Real-time/TODO.md` - AR temps réel + Tracking + Gestes

### Utilisation des TODOs
1. **Lire le TODO.md** du projet avant de commencer
2. **Suivre l'ordre des phases** : Développement séquentiel
3. **Valider chaque TODO** : Tests et vérifications
4. **Mettre à jour** : Ajouter/modifier selon les découvertes
5. **Commiter** : Après chaque phase complète

### 🔄 Gestion Git
- **Commits fréquents** : Après chaque fonctionnalité complète
- **Messages descriptifs** : Expliquer ce qui a été fait et pourquoi
- **Push régulier** : Synchronisation avec GitHub
- **Branches** : Une branche par fonctionnalité majeure

### 🎮 Mode Interactif
- **Questions avant actions** : Demander confirmation pour les changements importants
- **Explications détaillées** : Justifier chaque décision technique
- **Alternatives proposées** : Présenter les options quand il y en a plusieurs
- **Feedback demandé** : Vérifier la compréhension et l'accord

## 🎯 Objectifs par Phase

### P1 - MVP Desktop
**Focus** : Prouver la faisabilité technique
- OCR basique avec EasyOCR
- API Open Library simple
- Interface Streamlit minimaliste
- Tests de base

### P2 - Enhanced Desktop
**Focus** : Optimisation et intelligence
- YOLOv8 pour détection précise
- Cache Redis intelligent
- Correction d'orientation automatique
- Métriques de performance

### P3 - Mobile Static
**Focus** : Accessibilité mobile
- Interface native (Kivy)
- Mode offline avec SQLite
- Capture photo statique
- Synchronisation cloud

### P4 - Mobile Real-time
**Focus** : Performance maximale
- Flux vidéo temps réel
- TensorFlow Lite optimisé
- Cache multi-niveaux
- Overlay AR fluide

## ⚠️ Règles Importantes

### ❌ À Éviter
- **Code dupliqué** : Toujours factoriser
- **Hardcoding** : Utiliser des constantes/variables
- **Fonctions trop longues** : Maximum 50 lignes
- **Imports inutiles** : Nettoyer régulièrement
- **Commits massifs** : Préférer commits atomiques

### ✅ À Faire
- **Documentation** : Mettre à jour après chaque changement
- **Tests** : Écrire avant/après le code
- **Revue de code** : Vérifier la qualité
- **Performance** : Mesurer et optimiser
- **Sécurité** : Valider les inputs

## 🛠️ Outils et Technologies

### Core Python
- **PyTorch** : Deep learning et inference
- **OpenCV** : Computer vision
- **EasyOCR** : Reconnaissance de texte
- **Streamlit** : Interface web rapide

### Avancé
- **Ultralytics/YOLOv8** : Détection d'objets
- **Redis** : Cache haute performance
- **TensorFlow Lite** : Mobile AI
- **Kivy** : Applications mobiles Python

### Développement
- **pytest** : Tests unitaires
- **black** : Formatage automatique
- **flake8** : Linting
- **Git** : Contrôle de version

## 📈 Métriques de Succès

### Qualité Code
- **Coverage tests** : > 80%
- **Complexité cyclomatique** : < 10
- **Violations flake8** : 0
- **Documentation** : 100% des fonctions publiques

### Performance
- **OCR** : < 2 secondes par image
- **API** : < 500ms par requête
- **Interface** : Temps de réponse < 100ms
- **Mobile** : 30 FPS en temps réel

### Utilisateur
- **Précision OCR** : > 90%
- **Taux de reconnaissance** : > 95%
- **Satisfaction** : Score > 4/5

---

*Ce fichier doit être consulté avant chaque session de développement pour maintenir la cohérence et la qualité du projet.*