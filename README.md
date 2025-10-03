# 📚 **ShelfReader - Structure de projets**

Projet de reconnaissance de livres via OCR et intelligence artificielle, organisé en 4 projets progressifs.

## 📁 **Structure du repository**

```
ShelfReader/
├── p1-MVP-Desktop/         # 🏗️ Projet 1 : OCR + API + Interface web
├── p2-Enhanced-Desktop/    # 🚀 Projet 2 : YOLOv8 + Cache intelligent
├── p3-Mobile-Static/       # 📱 Projet 3 : Portage mobile + Hors-ligne
├── p4-Mobile-Real-time/    # 🎯 Projet 4 : AR temps réel + Performance
├── shared/                 # 🔗 Code partagé entre projets
├── docs/                   # 📖 Documentation complète
├── assets/                 # 🎨 Ressources graphiques
├── data/                   # 📊 Données et datasets
└── requirements.txt        # ⚙️ Dépendances globales
```

## 🎯 **Les 4 projets ShelfReader**

### **P1 - MVP Desktop** 🏗️
**Objectif** : Valider le concept de base
- OCR sur tranches de livres (EasyOCR)
- Enrichissement via Open Library API
- Interface web Streamlit
- **Technologies** : Python, OpenCV, PyTorch

### **P2 - Enhanced Desktop** 🚀
**Objectif** : Optimiser les performances
- Détection automatique (YOLOv8)
- Correction d'orientation automatique
- Cache intelligent multi-niveaux
- Métriques de performance
- **Technologies** : YOLOv8, Redis, OpenCV Hough

### **P3 - Mobile Static** 📱
**Objectif** : Portage mobile
- Application mobile native
- Capture photo intégrée
- Mode hors-ligne avec cache local
- UX mobile optimisée
- **Technologies** : React Native/Flutter, SQLite

### **P4 - Mobile Real-time** 🎯
**Objectif** : Application finale AR
- Réalité augmentée temps réel
- Performance 5-10 FPS
- Cache prédictif intelligent
- Optimisation maximale
- **Technologies** : ARCore/ARKit, TensorFlow Lite

## 🚀 **Démarrage rapide**

Chaque projet est indépendant et peut être développé séparément :

```bash
# Projet 1 - MVP Desktop
cd p1-MVP-Desktop
pip install -r requirements.txt
streamlit run src/app.py

# Projet 2 - Enhanced Desktop
cd p2-Enhanced-Desktop
pip install -r requirements.txt
python src/app_enhanced.py

# Projet 3 - Mobile Static
cd p3-Mobile-Static
# Suivre instructions dans README.md

# Projet 4 - Mobile Real-time
cd p4-Mobile-Real-time
# Suivre instructions dans README.md
```

## 📖 **Documentation**

- **[Structure générale](docs/Structure.md)** : Vue d'ensemble et workflows
- **[Projet 1 détaillé](docs/project1.md)** : Spécifications complètes P1
- **[Projet 2 détaillé](docs/project2.md)** : Spécifications complètes P2
- **[Projet 3 détaillé](docs/project3.md)** : Spécifications complètes P3
- **[Projet 4 détaillé](docs/project4.md)** : Spécifications complètes P4

## 🎓 **Objectifs pédagogiques**

- **OCR avancé** : EasyOCR, Tesseract, optimisation
- **Computer Vision** : OpenCV, YOLOv8, traitement d'images
- **IA/ML** : PyTorch, TensorFlow Lite, modèles optimisés
- **Mobile** : React Native, Flutter, ARCore/ARKit
- **Performance** : Cache, optimisation, métriques
- **Architecture** : Clean code, modularité, tests

## 🏆 **Résultat final**

Une application mobile professionnelle capable de :
- 📸 Reconnaître des livres en temps réel via caméra
- 🎯 Afficher des informations enrichies en AR
- 🧠 Apprendre des préférences utilisateur
- ⚡ Maintenir 5-10 FPS en conditions réelles
- 🔋 Optimiser l'autonomie batterie

---

**ShelfReader** - *De l'idée au produit fini, étape par étape* 🎯