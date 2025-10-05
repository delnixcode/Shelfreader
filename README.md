# 📚 **ShelfReader** - Détection intelligente de livres
## De l'OCR simple à l'IA mobile temps réel

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**ShelfReader** est une application multi-phases ambitieuse qui transforme la reconnaissance de livres sur étagères en une expérience fluide et intelligente, évoluant du prototype desktop simple vers une application mobile AR temps réel.

---

## 🎯 **Objectifs du Projet**

### **Vision Globale**
Développer une suite d'applications capables de reconnaître automatiquement les titres de livres sur des photos d'étagères, avec enrichissement intelligent via APIs externes pour créer un catalogue personnel automatisé.

### **Objectifs Techniques**
- ✅ **Précision maximale** : Taux de reconnaissance > 90%
- ✅ **Performance temps réel** : AR fluide sur mobile (5-10 FPS)
- ✅ **Automatisation complète** : Détection sans intervention utilisateur
- ✅ **Scalabilité** : De desktop simple à mobile AR avancé
- ✅ **Production ready** : Applications déployables sur stores

### **Impact Utilisateur**
- 📚 **Bibliophiles** : Inventorier automatiquement leur collection
- 🏪 **Libraires** : Gestion de stock optimisée
- 📖 **Étudiants** : Recherche rapide dans bibliothèques
- 🏛️ **Institutions** : Catalogage automatisé de collections

---

## 🔗 **Accès Direct aux Phases**

| Phase | Dossier | Description | Documentation | État |
|-------|---------|-------------|---------------|------|
| **P1** | [p1-OCR-Streamlit](./p1-OCR-Streamlit) | MVP Desktop avec Streamlit, 3 moteurs OCR | [README P1](./p1-OCR-Streamlit/README.md) | 🔄 EN COURS |
| **P2** | [p2-Enhanced-Desktop](./p2-Enhanced-Desktop) | Desktop avancé, détection YOLOv8 | [README P2](./p2-Enhanced-Desktop/README.md) | 🔄 EN COURS |
| **P3** | [p3-Mobile-Static](./p3-Mobile-Static) | Application mobile statique | [README P3](./p3-Mobile-Static/README.md) | ⏳ PLANIFIÉ |
| **P4** | [p4-Mobile-Real-time](./p4-Mobile-Real-time) | Application mobile temps réel | [README P4](./p4-Mobile-Real-time/README.md) | ⏳ PLANIFIÉ |

---

## 🏗️ **Architecture - 4 Phases Évolutives**

```
ShelfReader/
├── shared/                 # 📁 Ressources communes
│   ├── data/test_images/   # Images de test
│   ├── docs/              # Documentation partagée
│   └── scripts/           # Outils communs
├── p1-MVP-Desktop/        # 🏗️ Phase 1: OCR de base (EN COURS)
├── p2-Enhanced-Desktop/   # 🚀 Phase 2: YOLOv8 + Cache
├── p3-Mobile-Static/      # 📱 Phase 3: Mobile statique
└── p4-Mobile-Real-time/   # ⚡ Phase 4: Mobile AR temps réel
```

---

## 📋 **Les 4 Phases de Développement**

### 🏗️ **P1 - MVP Desktop** 🔄 EN COURS
**OCR basique + Interface web temporaire**
- **Technologies** : EasyOCR, Tesseract, TrOCR, Streamlit
- **Fonctionnalités** : Détection texte brute, API Open Library
- **État** : ✅ OCR fonctionnel, ✅ API intégrée, 🔄 Interface temporaire
- **Défis** : Précision OCR, interface desktop native

### 🚀 **P2 - Enhanced Desktop** 🔄 EN COURS
**Automatisation + Performance desktop**
- **Technologies** : YOLOv8, Redis, OpenCV, PyQt/Tkinter
- **Fonctionnalités** : Détection automatique tranches, cache intelligent, métriques
- **État** : 🔄 En développement actif
- **Défis** : Entraînement YOLOv8, orientation automatique, cache multi-niveau

### 📱 **P3 - Mobile Static** ⏳ PLANIFIÉ
**Portage mobile + UX native**
- **Technologies** : React Native/Flutter, TensorFlow Lite, SQLite
- **Fonctionnalités** : Interface mobile native, mode hors-ligne, capture photo
- **État** : ⏳ Architecture définie
- **Défis** : Framework cross-platform, portage Python, UX mobile

### ⚡ **P4 - Mobile Real-time** ⏳ PLANIFIÉ
**AR temps réel + Intelligence ultime**
- **Technologies** : ARCore/ARKit, modèles quantisés, cache prédictif
- **Fonctionnalités** : AR fluide, détection temps réel, ML adaptatif
- **État** : ⏳ Spécifications complètes
- **Défis** : Performance 5-10 FPS, stabilité AR, optimisation batterie

---

## 🛠️ **Technologies par Phase**

| Phase | OCR | IA/Détection | Interface | Cache/Stockage | Performance |
|-------|-----|--------------|-----------|----------------|-------------|
| **P1** | EasyOCR, Tesseract, TrOCR | - | Streamlit (temp) | Fichiers locaux | CPU/GPU |
| **P2** | EasyOCR optimisé | YOLOv8 | PyQt/Tkinter | Redis + SQLite | GPU + Cache |
| **P3** | TinyML | TensorFlow Lite | React Native/Flutter | SQLite mobile | Mobile optimisé |
| **P4** | Edge AI quantisé | Modèles nano + ML | ARCore/ARKit | Cache prédictif | GPU mobile + AR |

---

## 🎯 **Défis Techniques Majeurs**

### **Défis Résolus (P1)**
- **Défi 1** : ✅ Intégration OCR multi-moteurs
- **Défi 2** : ✅ API Open Library stable
- **Défi 3** : ✅ Interface web fonctionnelle

### **Défis en Cours (P2)**
- **Défi 4** : 🔄 Entraînement/adaptation YOLOv8 pour tranches de livres
- **Défi 5** : 🔄 Correction automatique d'orientation d'images
- **Défi 6** : 🔄 Cache intelligent multi-niveau (mémoire + disque)

### **Défis Planifiés (P3-P4)**
- **Défi 7** : ⏳ Framework mobile cross-platform optimal
- **Défi 8** : ⏳ Portage et optimisation code Python → mobile
- **Défi 9** : ⏳ Interface AR temps réel fluide (5-10 FPS)
- **Défi 10** : ⏳ Cache prédictif avec apprentissage automatique
- **Défi 11** : ⏳ Gestion thermique et autonomie batterie
- **Défi 12** : ⏳ Tracking AR précis et stable

---

## 📊 **Métriques et KPIs**

### **Qualité de Détection**
- **Précision OCR** : > 85% (P1), > 95% (P4)
- **Taux de reconnaissance** : > 90% des livres identifiés
- **Faux positifs** : < 5% (réduction progressive)

### **Performance**
- **P1 Desktop** : 3-15 secondes par image
- **P2 Desktop** : < 2 secondes avec cache
- **P3 Mobile** : < 5 secondes par photo
- **P4 Mobile AR** : 5-10 FPS temps réel

### **Utilisabilité**
- **Temps setup** : < 5 minutes
- **Courbe d'apprentissage** : Interface intuitive
- **Fiabilité** : > 95% uptime

---

## 🚀 **Démarrage Rapide**

### **Phase 1 (Actuelle)**
```bash
cd p1-MVP-Desktop
source env-p1/bin/activate
pip install -r requirements.txt
python ocr_easyocr.py test_images/books1.jpg --gpu
streamlit run app.py
```

### **Phase 2 (Prochaine)**
```bash
cd p2-Enhanced-Desktop
source env-p2/bin/activate
pip install -r requirements.txt
python src/app_enhanced.py
```

---

## 📈 **Évolution et Apprentissage**

### **Stratégie d'Évolution**
1. **P1** : Prouver la viabilité technique (OCR + API)
2. **P2** : Optimiser l'expérience desktop (IA + performance)
3. **P3** : Valider le concept mobile (portage + UX)
4. **P4** : Atteindre l'excellence (AR + intelligence ultime)

### **Apprentissages Clés**
- **Architecture modulaire** : Chaque phase = module indépendant
- **Technologies progressives** : Complexité croissante maîtrisée
- **Tests continus** : Validation à chaque étape
- **Documentation** : Savoirs capitalisés

### **Risques et Mitigation**
- **Risque technique** : Phases incrémentales pour validation
- **Risque performance** : Benchmarks et optimisations continues
- **Risque scope** : MVP first, features additionnelles ensuite

---

## 🤝 **Contribution et Développement**

### **Structure de Contribution**
- **Issues** : Bug reports et feature requests
- **Branches** : `feature/nom-fonction`, `fix/issue-numero`
- **PRs** : Review obligatoire, tests requis
- **Documentation** : Mise à jour automatique

### **Standards de Code**
- **Python** : PEP 8, type hints, docstrings
- **Tests** : pytest, couverture > 80%
- **CI/CD** : GitHub Actions pour automatisation
- **Documentation** : README détaillés, wiki technique

---

## 📖 **Ressources et Documentation**

### **Documentation par Phase**
- **P1** : `p1-MVP-Desktop/README.md` - Guide complet utilisation
- **P2** : `p2-Enhanced-Desktop/README.md` - Architecture avancée
- **P3** : `p3-Mobile-Static/README.md` - Spécifications mobile
- **P4** : `p4-Mobile-Real-time/README.md` - AR et performance

### **Ressources Partagées**
- **Images de test** : `shared/data/test_images/`
- **Documentation** : `docs/` - Guides techniques et architecture
- **Scripts utilitaires** : `shared/scripts/`

### **Documentation Technique Détaillée**
- **🔬 Sciences OCR P1** : [`docs/P1_OCR_Sciences_et_Technologies.md`](./docs/P1_OCR_Sciences_et_Technologies.md) - Pipeline OCR complet, algorithmes de détection, optimisations
- **📚 Architecture Globale** : [`docs/README.md`](./docs/README.md) - Vue d'ensemble de l'architecture projet

### **Liens Externes**
- **Repository** : [GitHub](https://github.com/delnixcode/Shelfreader)
- **Issues** : [Bug Reports](https://github.com/delnixcode/Shelfreader/issues)
- **Wiki** : [Documentation Technique](https://github.com/delnixcode/Shelfreader/wiki)

---

## 🎯 **Vision Finale**

**ShelfReader** évoluera vers une application mobile AR professionnelle capable de :
- 📱 **Scanner automatiquement** les étagères en AR temps réel
- 🎯 **Reconnaître précisément** chaque livre instantanément
- 🧠 **Apprendre continuellement** des habitudes utilisateur
- ⚡ **Fonctionner offline** avec cache intelligent
- 🚀 **Être déployée** sur App Store et Play Store

**De l'OCR simple à l'IA mobile temps réel** - Une aventure technique passionnante ! 📚🤖✨

---
*Dernière mise à jour : 4 octobre 2025*
