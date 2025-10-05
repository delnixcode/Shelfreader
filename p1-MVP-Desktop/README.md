# 🏗️ **ShelfReader P1 - MVP Desktop**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![EasyOCR](https://img.shields.io/badge/EasyOCR-1.7+-green.svg)](https://github.com/JaidedAI/EasyOCR)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Reconnaissance automatique de livres sur étagères avec OCR intelligent**

---


### �️ Nouveau layout vertical desktop

Depuis octobre 2025, l'interface web Streamlit propose un **layout vertical optimisé pour desktop** :

**Flux utilisateur après upload :**
1. **Première ligne** : Image originale (gauche) + paramètres de traitement (droite)
2. **Deuxième ligne** : Résultats de l'analyse (métriques) et tableau des livres détectés (pleine largeur)
3. **Troisième ligne** : Détails par livre (gauche) + visualisation des zones détectées (droite)

Ce layout améliore la lisibilité et l'expérience utilisateur sur grand écran.

#### **Démarrage rapide**
```bash
# Linux/macOS
cd p1-MVP-Desktop
source env-p1/bin/activate
streamlit run src/app.py

# Windows
cd p1-MVP-Desktop
env-p1\Scripts\activate
streamlit run src/app.py
```

Ouvrir http://localhost:8501 dans votre navigateur.

#### **Fonctionnalités principales**
- 📤 **Upload intuitif**
- ⚙️ **Paramètres avancés**
- 📊 **Résultats détaillés** (métriques, tableau)
- 👁️ **Visualisation des zones détectées**
- � **Détails par livre**
- 💾 **Export automatique**

#### **Avantages du layout vertical**
- ✅ **Lisibilité accrue** sur desktop
- ✅ **Navigation logique** : chaque étape est clairement séparée
- ✅ **Responsive** : fonctionne aussi sur mobile

#### **Quand utiliser la ligne de commande**
- � **Automatisation**
- ⚡ **Performance**
- 🔄 **Intégration**
- 📊 **Batch processing**
- **Connexion internet** : Pour télécharger les composants

### **Installation automatique**

#### **Étape 1 : Télécharger le projet**
```bash
# Copier cette commande dans votre terminal
git clone https://github.com/delnixcode/Shelfreader.git
cd Shelfreader/p1-MVP-Desktop
```

#### **Étape 2 : Activer l'environnement virtuel**
```bash
# Sur Linux/macOS
source env-p1/bin/activate

# Sur Windows
env-p1\Scripts\activate
```

#### **Étape 3 : Installer les dépendances**
```bash
# Cette commande installe tous les composants nécessaires
pip install -r requirements.txt
```

#### **Étape 4 : Vérifier l'installation**
```bash
# Tester que tout fonctionne
python --version  # Doit afficher Python 3.8+

# Tester les composants principaux
python -c "import easyocr, torch; print('✅ Installation réussie !')"
```

**🎉 Félicitations !** ShelfReader est maintenant installé sur votre ordinateur.

---

## ⚡ **Démarrage rapide (3 étapes)**

### **Étape 1 : Activer l'environnement**
```bash
# Toujours faire ça au début
source env-p1/bin/activate  # Linux/macOS
# ou
env-p1\Scripts\activate     # Windows
```

### **Démarrage rapide (3 étapes)**

### **Étape 1 : Activer l'environnement**
```bash
# Toujours faire ça au début
source env-p1/bin/activate  # Linux/macOS
# ou
env-p1\Scripts\activate     # Windows
```

### **Étape 2 : Choisir votre interface**

#### **🖥️ Interface Web (Recommandé pour débuter)**
```bash
# Linux/macOS
source env-p1/bin/activate
streamlit run src/app.py

# Windows
env-p1\Scripts\activate
streamlit run src/app.py

# Puis ouvrir: http://localhost:8501
```

#### **💻 Ligne de commande (Pour experts)**
```bash
# Test rapide avec image d'exemple
python src/ocr_easyocr.py test_images/books1.jpg --gpu --confidence 0.3
```

**Résultat attendu :**
```
🔍 EasyOCR avec détection adaptative - Image: test_images/books1.jpg
📊 Résultats: 14 livres détectés (93% de précision)
🎯 Confiance moyenne: 93.3%
🧮 Seuil adaptatif calculé: 13.4px
```

### **Étape 3 : Analyser vos propres images**
- **Interface web** : Uploadez votre image via le navigateur
- **Ligne de commande** : `python src/ocr_easyocr.py votre_image.jpg --gpu`

**🎉 Félicitations !** Vous venez d'analyser votre première étagère de livres !

### **Étape 3 : Voir les résultats**
Les résultats sont automatiquement sauvegardés dans le dossier `result-ocr/`.

**🎯 Succès !** Vous venez d'analyser votre première étagère de livres !

---

## 💻 **Comment utiliser**

### **Analyser vos propres photos**

#### **Format des images**
- ✅ **JPG/JPEG** : Recommandé
- ✅ **PNG** : Fonctionne aussi
- 📏 **Taille** : Minimum 1000 pixels de largeur
- 💡 **Conseil** : Photos bien éclairées, perpendiculaires à l'étagère

#### **Commandes de base**

```bash
# Analyser une photo simple (CPU, algorithme adaptatif par défaut)
python src/ocr_easyocr.py ma_photo.jpg

# Avec GPU pour aller plus vite (recommandé)
python src/ocr_easyocr.py ma_photo.jpg --gpu --confidence 0.3

# Sauvegarder les résultats dans un fichier spécifique
python src/ocr_easyocr.py ma_photo.jpg --output mes_resultats.txt
```

#### **Exemple complet (recommandé)**
```bash
# Analyser une étagère avec algorithme adaptatif optimisé (93% précision)
python src/ocr_easyocr.py etagere_bibliotheque.jpg --gpu --confidence 0.3 --spine-method shelfie
```

### **Comprendre les résultats**

Le fichier de résultats contient :
```
=== RÉSULTATS OCR ===
Titre détecté: "LE PETIT PRINCE"
Confiance: 0.892
Position: x=45, y=120

Titre détecté: "HARRY POTTER"
Confiance: 0.756
Position: x=45, y=160
```

- **Titre détecté** : Le nom du livre reconnu
- **Confiance** : Probabilité que ce soit correct (0.0 à 1.0)
- **Position** : Coordonnées sur l'image

### **Traiter plusieurs images**
```bash
# Analyser toutes les photos JPG d'un dossier
for photo in mes_photos/*.jpg; do
  echo "Analyse de $photo..."
  python src/ocr_easyocr.py "$photo" --gpu
done
```

---

## 🎨 **Interface web**

ShelfReader propose une interface web moderne et intuitive pour analyser vos images d'étagères.

### **Démarrage rapide**
```bash
# Linux/macOS
cd p1-MVP-Desktop
source env-p1/bin/activate
streamlit run src/app.py

# Windows
cd p1-MVP-Desktop
env-p1\Scripts\activate
streamlit run src/app.py
```

Puis ouvrir http://localhost:8501 dans votre navigateur.

### **Fonctionnalités**
- 📤 **Upload intuitif** : Glissez-déposez vos photos directement
- ⚙️ **Paramètres avancés** : Réglages du seuil de confiance et GPU
- 👁️ **Visualisation temps réel** : Aperçu des zones détectées sur l'image
- 📊 **Résultats détaillés** : Tableaux et métriques de performance
- 💾 **Export automatique** : Résultats sauvegardés dans `result-ocr/`
- 🎯 **Algorithme optimisé** : Utilise automatiquement l'OCR adaptatif (93% précision)

### **Interface utilisateur**
- **Colonne gauche** : Informations sur l'algorithme et paramètres
- **Zone centrale** : Upload d'image et paramètres de traitement
- **Résultats** : Métriques, visualisation et détails par livre

### **Avantages de l'interface web**
- ✅ **Plus simple** : Pas besoin de commandes complexes
- ✅ **Visuel** : Aperçu immédiat des résultats
- ✅ **Interactif** : Ajustement des paramètres en temps réel
- ✅ **Complet** : Toutes les fonctionnalités disponibles

### **Quand utiliser la ligne de commande**
- 🔧 **Automatisation** : Scripts et traitement par lots
- ⚡ **Performance** : Traitement direct sans interface
- 🔄 **Intégration** : Utilisation dans d'autres programmes
- 📊 **Batch processing** : Traitement de plusieurs images

---

## 🔧 **Options avancées**

### **Améliorer la précision**

#### **Seuil de confiance**
```bash
# Très tolérant (beaucoup de résultats, peut-être des erreurs)
python src/ocr_easyocr.py image.jpg --confidence 0.1

# Recommandé pour images nettes (93% précision)
python src/ocr_easyocr.py image.jpg --confidence 0.3

# Strict (haute précision, moins de résultats)
python src/ocr_easyocr.py image.jpg --confidence 0.5
```

#### **Méthodes de détection**
```bash
# Algorithme adaptatif Shelfie (recommandé - 14/15 livres détectés)
python src/ocr_easyocr.py image.jpg --gpu --spine-method shelfie

# Alternative ICCC2013 (détection basée sur Canny)
python src/ocr_easyocr.py image.jpg --gpu --spine-method iccc2013

# Mode debug (affiche les analyses multi-échelle sans fenêtres)
python src/ocr_easyocr.py image.jpg --gpu --debug
```

### **Désactiver des fonctionnalités**
```bash
# Désactiver la détection intelligente de livres
python src/ocr_easyocr.py image.jpg --no-spine

# Mode debug (pour les développeurs)
python src/ocr_easyocr.py image.jpg --debug
```

### **Configuration recommandée**
```bash
# Pour débuter (simple et efficace)
python src/ocr_easyocr.py image.jpg --gpu

# Configuration optimale (93% précision sur books1.jpg)
python src/ocr_easyocr.py image.jpg --gpu --confidence 0.3 --spine-method shelfie

# Pour production complète
python src/ocr_easyocr.py image.jpg --gpu --confidence 0.3 --spine-method shelfie --output resultats.txt
```

---

## 🛠️ **Dépannage**

### **❌ "ModuleNotFoundError"**
**Problème :** Un composant n'est pas installé.

**Solution :**
```bash
# Réactiver l'environnement virtuel
source env-p1/bin/activate

# Réinstaller les dépendances
pip install -r requirements.txt
```

### **❌ "CUDA out of memory"**
**Problème :** Problème avec le GPU.

**Solution :**
```bash
# Utiliser le CPU à la place
python src/ocr_easyocr.py image.jpg  # Sans --gpu
```

### **❌ Aucun texte détecté**
**Problème :** L'image est trop sombre ou floue.

**Solutions :**
```bash
# Baisser le seuil de confiance
python src/ocr_easyocr.py image.jpg --confidence 0.1

# Essayer un autre moteur OCR
python src/ocr_tesseract.py image.jpg

# Vérifier la qualité de l'image
```

### **❌ Commande inconnue**
**Problème :** Erreur de frappe dans la commande.

**Solution :**
```bash
# Voir toutes les options disponibles
python src/ocr_easyocr.py --help
```

### **Vérifications système**
```bash
# Vérifier Python
python --version

# Vérifier l'environnement virtuel
which python  # Doit pointer vers env-p1/bin/python

# Vérifier espace disque
df -h
```

---

## ❓ **Questions fréquentes**

### **🤔 Quel moteur OCR choisir ?**
- **EasyOCR** (recommandé) : Bon équilibre vitesse/précision
- **Tesseract** : Ultra rapide, pour les tests
- **TrOCR** : Maximum précision, plus lent

### **💻 GPU obligatoire ?**
- **Non**, mais recommandé pour aller 3x plus vite
- Tous les moteurs fonctionnent en CPU
- Testez d'abord sans GPU, ajoutez `--gpu` après

### **📏 Quelle taille d'image ?**
- **Minimum** : 1000 pixels de largeur
- **Recommandé** : 2000+ pixels
- **Format** : JPG ou PNG de bonne qualité

### **⚡ C'est rapide ?**
- **Tesseract** : ~2 secondes
- **EasyOCR CPU** : ~5-10 secondes
- **EasyOCR GPU** : ~2-5 secondes
- **TrOCR GPU** : ~5-15 secondes

### **💾 Où sont sauvegardés les résultats ?**
- **Dossier** : `result-ocr/`
- **Format** : Fichiers texte (.txt)
- **Contenu** : Titres détectés + détails techniques

### **🌐 Internet nécessaire ?**
- **OCR** : Fonctionne hors ligne
- **Enrichissement** : Nécessite internet (optionnel)
- **Interface web** : Fonctionne en local

---

## 📚 **Informations techniques**

### **Architecture du projet**
```
p1-MVP-Desktop/
├── src/                    # Code source principal
│   ├── ocr_easyocr.py      # Moteur OCR principal
│   ├── ocr_tesseract.py    # Moteur rapide
│   ├── ocr_trocr.py        # Moteur haute précision
│   ├── app.py              # Interface web
│   └── api_client.py       # API externes
├── tests/                  # Tests et démonstrations
├── test_images/            # Photos d'exemple
├── result-ocr/             # Résultats (auto-créé)
└── requirements.txt        # Dépendances
```

### **Algorithmes utilisés**

#### **Détection Adaptative Shelfie (Nouveau)**
- **Analyse statistique des gaps** : Calcule le seuil optimal automatiquement
- **Détection multi-échelle** : Teste 3 seuils différents (0.6x, 1.0x, 1.4x)
- **Adaptation à la taille de police** : Ajuste ±25% selon le ratio de hauteur
- **Pipeline 13 étapes** : Downsample → Sobel² → Binarisation → Morphologie → Clustering
- **Fallback intelligent** : Bascule automatiquement si <5 lignes détectées
- **Précision mesurée** : 93% (14/15 livres) sur books1.jpg

#### **Formule du seuil adaptatif**
```
threshold = (Q25 + median) / 2
threshold = clamp(threshold, 10, 35)  # Limites px
```

#### **Support GPU**
- Accélération PyTorch CUDA
- Fallback automatique CPU
- Détection automatique du matériel

### **Dépendances principales**
- **easyocr** : Reconnaissance optique de caractères
- **torch** : Calcul GPU/CPU
- **streamlit** : Interface web
- **opencv-python** : Traitement d'images
- **Pillow** : Manipulation d'images

### **Performances mesurées**
| Moteur | Précision | Vitesse | GPU | Méthode |
|--------|-----------|---------|-----|---------|
| **EasyOCR Adaptatif** | **93.3%** | 3-5s | ✅ | Shelfie multi-échelle |
| EasyOCR ICCC2013 | 87.2% | 3-5s | ✅ | Détection Canny |
| Tesseract | 73.3% | 1-2s | ❌ | OCR basique |
| TrOCR | 80.7% | 8-15s | ✅ | Transformers |

**Résultats détaillés algorithme adaptatif (6 images testées) :**
- books1.jpg : 14/15 livres (93%) - confidence 93.3%
- books2.jpg : 13 livres - confidence 82.4%
- books3.jpg : 12 livres - confidence 87.2%
- books4.jpg : 9 livres - confidence 83.4%
- books5.jpg : 7 livres - confidence 79.7%
- books6.png : 11 livres - confidence 76.6%
- **Moyenne totale : 66 livres, 83.8% de confiance**

### **API externes**
- **Open Library** : Métadonnées des livres
- **Limite** : 100 requêtes/minute
- **Usage** : Enrichissement optionnel

---

## 🤝 **Contribuer**

### **Signaler un problème**
1. Vérifier que le problème n'existe pas déjà
2. Créer une "issue" sur GitHub avec :
   - Description claire du problème
   - Étapes pour reproduire
   - Version de Python et OS

### **Améliorer le code**
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Tester vos changements
4. Créer une Pull Request

### **Standards de développement**
- **Python** : Version 3.8 minimum
- **Style** : PEP 8
- **Tests** : Couverture minimum 80%
- **Documentation** : Commentaires en anglais

---

## 📈 **Évolution du projet**

### **✅ Version actuelle (P1 - MVP)**
- [x] Reconnaissance OCR basique
- [x] Interface web simple
- [x] Support GPU
- [x] **Détection adaptative multi-échelle (93% précision)**
- [x] **Analyse statistique automatique des gaps**
- [x] **Adaptation dynamique à la taille de police**
- [x] Pipeline Shelfie 13 étapes optimisé
- [x] Méthode alternative ICCC2013
- [x] CLI raccourci pour utilisation rapide
- [x] Documentation complète

### **🔄 Prochaines étapes**
- [ ] Interface mobile
- [ ] Base de données locale
- [ ] Mode traitement par lot
- [ ] Export PDF/Excel
- [ ] API REST
- [ ] Synchronisation cloud

---

**🎉 Merci d'utiliser ShelfReader !**

Pour plus d'informations : [GitHub Issues](https://github.com/delnixcode/Shelfreader/issues)

*Développé avec ❤️ pour les amoureux des livres*
