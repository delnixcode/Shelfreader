# 🏗️ **ShelfReader P1 - MVP Desktop**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![EasyOCR](https://img.shields.io/badge/EasyOCR-1.7+-green.svg)](https://github.com/JaidedAI/EasyOCR)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Reconnaissance automatique de livres sur étagères avec OCR intelligent**

---

## 📋 **Sommaire**

- [🎯 Qu'est-ce que ShelfReader ?](#-quest-ce-que-shelfreader-)
- [🚀 Installation (5 minutes)](#-installation-5-minutes)
- [⚡ Démarrage rapide (3 étapes)](#-démarrage-rapide-3-étapes)
- [💻 Comment utiliser](#-comment-utiliser)
- [🎨 Interface web](#-interface-web)
- [🔧 Options avancées](#-options-avancées)
- [🛠️ Dépannage](#️-dépannage)
- [❓ Questions fréquentes](#-questions-fréquentes)
- [📚 Informations techniques](#-informations-techniques)

---

## 🎯 **Qu'est-ce que ShelfReader ?**

**ShelfReader** est une application qui reconnaît automatiquement les titres de livres sur des photos d'étagères.

### **Comment ça marche ?**
1. 📸 **Prenez une photo** d'une étagère de livres
2. 🤖 **L'IA analyse** l'image et détecte les textes
3. 📚 **Résultat** : Liste des livres identifiés avec leurs titres

### **Pour qui ?**
- 📖 **Particuliers** : Inventorier sa bibliothèque personnelle
- 🏪 **Libraires** : Gérer rapidement les stocks
- 📚 **Étudiants** : Trouver des livres dans les bibliothèques
- 🏛️ **Écoles** : Cataloguer automatiquement les collections

### **Points forts**
- ✅ **Facile à utiliser** : Interface simple et intuitive
- ✅ **Rapide** : Analyse une étagère en quelques secondes
- ✅ **Intelligent** : Détecte automatiquement les séparations entre livres
- ✅ **Précis** : Corrige automatiquement les erreurs de reconnaissance

---

## 🚀 **Installation (5 minutes)**

### **Prérequis**
- **Ordinateur** : Windows, macOS ou Linux
- **Python** : Version 3.8 ou supérieure
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

### **Étape 2 : Tester avec une image d'exemple**
```bash
# Cette commande analyse une photo d'exemple
python src/ocr_easyocr.py test_images/books1.jpg --gpu
```

**Résultat attendu :**
```
🔍 EasyOCR avec détection de tranches - Image: test_images/books1.jpg
📊 Résultats: 11 livres détectés
🎯 Confiance moyenne: 0.908
📝 Texte complet: Ada 95 | KERNICHAN THE SECOND EDITION PTR | ...
```

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
# Analyser une photo simple
python src/ocr_easyocr.py ma_photo.jpg

# Avec GPU pour aller plus vite (recommandé)
python src/ocr_easyocr.py ma_photo.jpg --gpu

# Sauvegarder les résultats dans un fichier spécifique
python src/ocr_easyocr.py ma_photo.jpg --output mes_resultats.txt
```

#### **Exemple complet**
```bash
# Analyser une étagère avec toutes les améliorations
python src/ocr_easyocr.py etagere_bibliotheque.jpg --gpu --validate --output resultats_etagere.txt
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

Pour une utilisation plus simple, ShelfReader propose une interface web moderne.

### **Démarrage**
```bash
# Lancer l'interface web
streamlit run src/app.py
```

Puis ouvrir http://localhost:8501 dans votre navigateur.

### **Fonctionnalités**
- 📤 **Glisser-déposer** : Déposez vos photos directement
- ⚙️ **Configuration** : Réglages simples pour l'analyse
- 👁️ **Aperçu** : Visualisez les zones détectées
- 📊 **Résultats** : Tableaux clairs des livres trouvés
- 💾 **Téléchargement** : Exportez les résultats

---

## 🔧 **Options avancées**

### **Améliorer la précision**

#### **Seuil de confiance**
```bash
# Très tolérant (beaucoup de résultats, peut-être des erreurs)
python src/ocr_easyocr.py image.jpg --confidence 0.1

# Équilibre recommandé (bon compromis)
python src/ocr_easyocr.py image.jpg --confidence 0.2

# Strict (haute précision, moins de résultats)
python src/ocr_easyocr.py image.jpg --confidence 0.5
```

#### **Validation intelligente**
```bash
# Activer la correction automatique des titres
python src/ocr_easyocr.py image.jpg --validate

# Combinaison optimale recommandée
python src/ocr_easyocr.py image.jpg --gpu --validate --confidence 0.3
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

# Pour production (maximum de précision)
python src/ocr_easyocr.py image.jpg --gpu --validate --confidence 0.3 --output resultats.txt
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

#### **Détection Shelfie**
- Analyse des lignes de séparation entre livres
- Réduction de 81% des fragments de texte
- Groupement intelligent des textes par livre

#### **Validation Jaccard**
- Comparaison avec base de référence connue
- Correction automatique des erreurs OCR
- Précision de 93% sur les titres

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
| Moteur | Précision | Vitesse | GPU |
|--------|-----------|---------|-----|
| EasyOCR Pro | 90.8% | 3-5s | ✅ |
| Tesseract | 73.3% | 1-2s | ❌ |
| TrOCR | 80.7% | 8-15s | ✅ |

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
- [x] Détection intelligente de livres
- [x] Validation des titres
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
