# 📋 P1 - MVP Desktop - Plan de Développement

## 🎯 Vue d'ensemble
**Projet 1** : Application desktop basique avec OCR + API + interface Streamlit. Objectif : prouver la faisabilité technique du concept ShelfReader.

**Technologies** : EasyOCR, OpenCV, Streamlit, Requests
**Durée estimée** : 2-3 semaines
**Critères de succès** : OCR fonctionnel, API intégrée, interface utilisable

## 🏗️ Structure du projet

```
p1-MVP-Desktop/
├── src/
│   ├── __init__.py
│   ├── api_client.py          # Client API Open Library
│   ├── ocr_processor.py       # Traitement OCR avec EasyOCR
│   └── app.py                 # Interface Streamlit principale
├── tests/
│   ├── __init__.py
│   ├── test_api_client.py     # Tests API client
│   ├── test_ocr_processor.py  # Tests OCR
│   └── test_app.py            # Tests interface
├── assets/
│   └── test_images/           # Images de test pour validation
├── docs/
│   └── README.md              # Documentation spécifique P1
├── requirements.txt           # Dépendances P1 uniquement
├── .env.example               # Variables d'environnement
└── README.md                  # Guide d'utilisation P1
```

## 📁 Structure des fichiers

### 🔧 `src/api_client.py` - Client API Open Library
**Objectif** : Interface propre vers l'API Open Library pour récupérer les métadonnées des livres.

**TODO :**
- [ ] **Fonction `search_book(title)`**
  - Input : titre du livre (string)
  - Output : dict avec titre, auteur, description, genres
  - Gestion d'erreur : livre non trouvé
  - Rate limiting : respecter les limites API
  - *Pourquoi* : Abstraction de l'API pour réutilisabilité

- [ ] **Fonction `get_book_details(isbn)`**
  - Input : ISBN du livre
  - Output : métadonnées complètes
  - Cache local basique (dict en mémoire)
  - *Pourquoi* : Support ISBN pour recherche précise

- [ ] **Gestion d'erreurs robuste**
  - Timeout des requêtes
  - Erreurs réseau
  - Réponses API invalides
  - *Pourquoi* : Application stable en conditions réelles

- [ ] **Tests unitaires**
  - Mock des appels API
  - Tests d'erreur
  - Validation des données
  - *Pourquoi* : Fiabilité du composant critique

### 🔍 `src/ocr_processor.py` - Traitement OCR
**Objectif** : Extraction de texte à partir d'images de tranches de livres.

**TODO :**
- [ ] **Fonction `extract_text_from_image(image_path)`**
  - Input : chemin vers image
  - Output : liste de textes détectés avec positions
  - Prétraitement : redimensionnement, contraste
  - *Pourquoi* : Interface simple pour l'OCR

- [ ] **Optimisation des performances**
  - Cache des résultats OCR
  - Traitement par lots si plusieurs images
  - *Pourquoi* : Performance acceptable pour l'utilisateur

- [ ] **Gestion des formats d'image**
  - Support JPEG, PNG, WebP
  - Validation des dimensions
  - Conversion automatique si nécessaire
  - *Pourquoi* : Robustesse face aux différents formats

- [ ] **Filtrage des résultats**
  - Suppression du bruit OCR
  - Validation basique des titres
  - *Pourquoi* : Qualité des données pour l'API

- [ ] **Tests avec images de test**
  - Images d'étagères réelles
  - Différents angles/orientations
  - *Pourquoi* : Validation en conditions réelles

### 🎨 `src/app.py` - Interface Streamlit
**Objectif** : Interface web simple pour upload d'images et affichage des résultats.

**TODO :**
- [ ] **Page d'accueil avec upload**
  - Sélecteur de fichier image
  - Aperçu de l'image uploadée
  - Bouton "Analyser"
  - *Pourquoi* : UX intuitive pour les utilisateurs

- [ ] **Zone de résultats**
  - Liste des livres détectés
  - Titres, auteurs, descriptions
  - Indicateur de chargement
  - *Pourquoi* : Feedback visuel des résultats

- [ ] **Gestion des erreurs UI**
  - Messages d'erreur user-friendly
  - États de chargement
  - Retry automatique
  - *Pourquoi* : Expérience utilisateur fluide

- [ ] **Mode recherche avancée**
  - Filtrage par genre/thématique
  - Recherche par titre exact
  - *Pourquoi* : Fonctionnalités différenciantes

### 🧪 `tests/` - Tests unitaires
**Objectif** : Validation de tous les composants critiques.

**TODO :**
- [ ] **`test_api_client.py`**
  - Tests des fonctions API
  - Mocks pour éviter appels réels
  - Tests d'erreur
  - *Pourquoi* : Fiabilité de l'intégration API

- [ ] **`test_ocr_processor.py`**
  - Tests avec images mock
  - Validation des extractions
  - Tests de performance
  - *Pourquoi* : Qualité de l'OCR

- [ ] **`test_app.py`**
  - Tests d'intégration UI
  - Simulation d'uploads
  - *Pourquoi* : Interface fonctionnelle

## 🔄 Workflow de développement

### Phase 1 : Infrastructure (Semaine 1)
1. Configuration de l'environnement virtuel
2. Installation des dépendances de base
3. Structure des dossiers et fichiers
4. Tests d'imports et dépendances

### Phase 2 : API Client (Semaine 1-2)
1. Implémentation `api_client.py`
2. Tests unitaires API
3. Gestion d'erreurs
4. Documentation des fonctions

### Phase 3 : OCR Processor (Semaine 2)
1. Implémentation `ocr_processor.py`
2. Tests avec images d'exemple
3. Optimisation des performances
4. Intégration avec API

### Phase 4 : Interface Web (Semaine 2-3)
1. Implémentation `app.py`
2. Intégration OCR + API
3. Tests end-to-end
4. Polissage UI/UX

### Phase 5 : Tests & Validation (Semaine 3)
1. Tests complets de tous les composants
2. Validation avec données réelles
3. Optimisation des performances
4. Documentation finale

## ✅ Critères d'acceptation

### Fonctionnels
- [ ] Upload d'image d'étagère
- [ ] Détection automatique des titres
- [ ] Récupération des métadonnées via API
- [ ] Affichage des résultats dans l'interface
- [ ] Recherche par titre ou thématique

### Techniques
- [ ] Temps de traitement < 10 secondes
- [ ] Précision OCR > 80%
- [ ] Gestion d'erreurs robuste
- [ ] Code couvert par les tests > 70%
- [ ] Respect des bonnes pratiques PEP 8

### Qualité
- [ ] Documentation complète
- [ ] Code review passé
- [ ] Tests automatisés fonctionnels
- [ ] Interface intuitive

## 🚨 Points d'attention

### Performance
- OCR peut être lent : implémenter cache
- API peut échouer : gérer les timeouts
- Images lourdes : compression/redimensionnement

### Robustesse
- Formats d'image variés : validation stricte
- Connexion réseau : mode offline/degraded
- Erreurs imprévues : logging détaillé

### Maintenabilité
- Code modulaire : séparation des responsabilités
- Configuration externalisée : variables d'environnement
- Tests automatisés : CI/CD friendly