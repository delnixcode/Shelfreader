# 📚 ShelfReader

Application pour détecter et rechercher des livres sur une étagère.


## �️ Nouveau layout desktop (MVP)

Depuis octobre 2025, l'interface web du MVP Desktop propose un **layout vertical optimisé** :

**Workflow utilisateur :**
1. Upload d'une image d'étagère
2. Première ligne : image originale + paramètres de traitement
3. Deuxième ligne : résultats de l'analyse + tableau des livres détectés
4. Troisième ligne : détails par livre + visualisation des zones détectées

Ce flux vertical améliore la clarté et la navigation sur desktop.

## 🎯 Fonctionnalités

1. 📸 Uploader une photo d'étagère
2. 🔍 Détecter les titres de livres (OCR modulaire)
3. 🌐 Récupérer les métadonnées (Open Library API)
4. 🎨 Afficher les résultats dans une interface web

## 📂 Structure du projet

Consulte [STRUCTURE.md](Structure.md) pour la structure complète.

## 🚀 Installation

```bash
# Cloner le projet
git clone <url>
cd ShelfReader

# Installer les dépendances
pip install -r requirements.txt
```

## 📖 Documentation

Consulte [docs/LEARNING.md](LEARNING.md) pour la documentation complète.

## 🧪 Tester l'API Client (Phase 1)

```bash
python src/api_client.py
```


## 🎯 Phases du projet

- ✅ **Phase 1** : Client API Open Library → `src/api_client.py`
- ✅ **Phase 2** : OCR Modulaire (EasyOCR, Tesseract, TrOCR) → `src/ocr_*.py`
- ✅ **Phase 3** : Interface Streamlit verticale desktop → `src/app.py`
- ⏳ **Phase 4** : Tests → `tests/`

## 🧪 Tester les modules OCR (Phase 2)

```bash
# Tester EasyOCR
python src/ocr_easyocr.py --image ../data/test_images/sample.jpg

# Tester Tesseract
python src/ocr_tesseract.py --image ../data/test_images/sample.jpg

# Tester TrOCR
python src/ocr_trocr.py --image ../data/test_images/sample.jpg

# Script unifié utilisant tous les moteurs
python scripts/ocr_detect.py --image ../data/test_images/sample.jpg --engine easyocr
```

## 📝 Prochaines étapes

1. Teste le client API : `python src/api_client.py`
2. Teste les modules OCR individuels
3. Lis la doc : [docs/OCR_Code_Explanation.md](OCR_Code_Explanation.md)
4. Passe à la Phase 3 : Interface utilisateur