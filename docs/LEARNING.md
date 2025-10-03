# 📚 ShelfReader - Guide d'Apprentissage Complet

## 🎯 Vue d'ensemble du projet

**ShelfReader** est une application pour :
1. 📸 Uploader une photo d'étagère
2. 🔍 Détecter les titres de livres (OCR)
3. 🌐 Récupérer les métadonnées (Open Library API)
4. 🎨 Afficher les résultats dans une interface web

---

## 📖 Documentation par Module

### 🌐 Phase 1 : Client API Open Library

**Fichier** : `src/api_client.py`

**Documentation** : [📖 api_client.md](learning/api_client.md)

**Concepts abordés** :
- REST API et requêtes HTTP
- Gestion d'erreurs avec `try/except`
- Rate limiting
- F-strings et formatage d'URL
- Work key et navigation dans l'API

**TODOs** :
- ✅ `__init__()` - Initialisation
- ✅ `search_books()` - Recherche par titre
- ✅ `get_book_details()` - Récupérer subjects
- ✅ `get_book_cover_url()` - URL des couvertures

---

### 🔍 Phase 2 : OCR - Détection de texte

**Fichier** : `src/ocr_processor.py`

**Documentation** : [📖 ocr_processor.md](learning/ocr_processor.md)

**Concepts abordés** :
- Tesseract OCR et pytesseract
- Traitement d'images avec PIL/Pillow
- Extraction de texte structuré
- Filtrage et nettoyage de données
- Détection de langues

**TODOs** :
- ⏳ `__init__()` - Configuration Tesseract
- ⏳ `extract_text()` - Extraire texte brut
- ⏳ `extract_book_titles()` - Détecter les titres
- ⏳ `get_bounding_boxes()` - Coordonnées des textes

---

### 🎨 Phase 3 : Interface Streamlit

**Fichier** : `src/app.py`

**Documentation** : [📖 app.md](learning/app.md)

**Concepts abordés** :
- Streamlit : widgets et layout
- Upload de fichiers
- Session state (cache)
- Affichage d'images
- Composants interactifs

**TODOs** :
- ⏳ Interface d'upload
- ⏳ Affichage des résultats OCR
- ⏳ Recherche dans l'API
- ⏳ Filtrage thématique
- ⏳ Visualisation avec bounding boxes

---

### 🧪 Phase 4 : Tests

**Fichier** : `tests/test_api_client.py`

**Documentation** : [📖 testing.md](learning/testing.md)

**Concepts abordés** :
- pytest et tests unitaires
- Mocking avec `unittest.mock`
- Tests d'intégration
- Coverage et qualité du code
- TDD (Test-Driven Development)

**TODOs** :
- ⏳ Tests pour `search_books()`
- ⏳ Tests pour `get_book_details()`
- ⏳ Tests d'erreurs réseau
- ⏳ Tests de timeout

---

## 🗺️ Roadmap
### ⏳ Phase 5 : Mobile temps réel
- [ ] Capture flux vidéo continu (caméra mobile)
- [ ] OCR en temps réel sur chaque frame
- [ ] Saisie du titre ou thématique par l'utilisateur
- [ ] Recherche et filtrage dynamique via API
- [ ] Surlignage en temps réel des livres trouvés
- [ ] Interface utilisateur mobile

### ✅ Phase 1 : API Client (ACTUELLE)
- [x] Documentation complète
- [ ] Implémentation des 4 méthodes
- [ ] Tests unitaires

### ⏳ Phase 2 : OCR
- [ ] Installation Tesseract
- [ ] Configuration OCR
- [ ] Extraction de texte
- [ ] Tests avec images réelles

### ⏳ Phase 3 : Interface Streamlit
- [ ] Layout de base
- [ ] Upload d'image
- [ ] Affichage des résultats
- [ ] Recherche thématique

### ⏳ Phase 4 : Intégration
- [ ] Tests end-to-end
- [ ] Déploiement
- [ ] Documentation utilisateur

---

## 📂 Structure du projet
```
ShelfReader/
├── docs/
│   ├── LEARNING.md           # ← Tu es ici !
│   └── learning/
│       ├── api_client.md     # Documentation API
│       ├── ocr_processor.md  # Documentation OCR
│       ├── app.md            # Documentation Streamlit
│       └── testing.md        # Documentation Tests
├── src/
│   ├── api_client.py         # Client Open Library
│   ├── ocr_processor.py      # OCR Tesseract
│   └── app.py                # Interface Streamlit
├── mobile/
│   ├── ocr_realtime.py       # OCR temps réel (mobile)
│   ├── api_client_mobile.py  # API mobile
│   └── ui_mobile.py          # Interface mobile
├── tests/
│   ├── test_api_client.py
│   └── test_ocr_processor.py
└── requirements.txt
```

---

## 🚀 Comment utiliser cette documentation ?

### Pour apprendre :
1. Commence par [api_client.md](learning/api_client.md)
2. Lis les concepts théoriques
3. Implémente les TODOs un par un
4. Teste avec les exemples fournis

### Pour coder :
1. Ouvre le fichier `.py` correspondant
2. Ouvre la doc `.md` en parallèle
3. Suis les TODOs dans l'ordre
4. Vérifie avec les exemples d'utilisation

### Pour débugger :
1. Consulte la section "Erreurs courantes" de chaque module
2. Vérifie les logs et messages d'erreur
3. Compare avec les exemples de code

---

## 🎓 Concepts Python abordés

### Niveau débutant
- ✅ Variables et types de données
- ✅ Fonctions et méthodes
- ✅ F-strings
- ✅ Dictionnaires et listes
- ✅ Gestion d'erreurs (`try/except`)

### Niveau intermédiaire
- ⏳ Classes et POO
- ⏳ Modules et imports
- ⏳ Manipulation d'images
- ⏳ APIs et requêtes HTTP
- ⏳ Tests unitaires

### Niveau avancé
- ⏳ Async/await (futur)
- ⏳ Décorateurs
- ⏳ Context managers
- ⏳ Threading/multiprocessing

---

## 📝 Prochaines étapes

1. **Maintenant** : Termine `api_client.py` avec [📖 api_client.md](learning/api_client.md)
2. **Ensuite** : Passe à `ocr_processor.py` avec [📖 ocr_processor.md](learning/ocr_processor.md)
3. **Puis** : Crée l'interface avec [📖 app.md](learning/app.md)
4. **Enfin** : Teste tout avec [📖 testing.md](learning/testing.md)

---

## 💡 Conseils

- 📖 Lis TOUTE la documentation d'un module avant de coder
- 🧪 Teste chaque fonction après l'avoir écrite
- 🔄 N'hésite pas à revenir en arrière pour comprendre
- 💬 Pose des questions si quelque chose n'est pas clair
- 🎯 Concentre-toi sur UNE phase à la fois

Bon courage ! 🚀
Bon courage ! 🚀
