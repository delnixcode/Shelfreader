# 🏗️ Moteurs OCR - Architecture Modulaire

## 📋 Vue d'ensemble

ShelfReader utilise une architecture modulaire avec **3 moteurs OCR spécialisés** :

- **EasyOCR** : Précision maximale sur tranches de livres (93% de réussite)
- **Tesseract** : Traitement ultra-rapide (CPU uniquement)
- **TrOCR** : Spécialisé texte manuscrit (GPU recommandé)

## 📁 Structure des Moteurs

```
src/engines/
├── easyocr/           # Moteur EasyOCR spécialisé tranches
│   ├── README.md      # Documentation complète
│   ├── __init__.py    # Point d'entrée du module
│   ├── main.py        # Script principal de test
│   ├── logic/         # Logique métier (orchestrator, config)
│   ├── models/        # Structures de données
│   ├── preprocessing/ # Amélioration d'images
│   ├── detection/     # Algos détection texte
│   └── grouping/      # Regroupement résultats
├── tesseract/         # Moteur Tesseract rapide
│   ├── README.md      # Documentation complète
│   ├── __init__.py    # Point d'entrée du module
│   ├── main.py        # Script principal de test
│   ├── logic/         # Logique métier (orchestrator, config)
│   ├── preprocessing/ # CLAHE et filtres
│   └── grouping/      # Regroupement proximité
├── trocr/            # Moteur TrOCR manuscrit
│   ├── README.md      # Documentation complète
│   ├── __init__.py    # Point d'entrée du module
│   ├── main.py        # Script principal de test
│   ├── logic/         # Logique métier (orchestrator, config)
│   ├── preprocessing/ # Conversion RGB
│   ├── detection/     # Segmentation bandes
│   └── grouping/      # Regroupement temporel
└── README.md          # Cette documentation
```

## 🎯 Architecture de Chaque Moteur

### Composants Standards
1. **`orchestrator.py`** - Orchestrateur principal du pipeline OCR
2. **`config.py`** - Paramètres et constantes spécifiques
3. **`preprocessing/`** - Amélioration qualité des images
4. **`detection/`** - Détection régions de texte (optionnel)
5. **`grouping/`** - Regroupement en lignes cohérentes
6. **`models/`** - Classes de données (optionnel)

### Interface Unifiée
Tous les moteurs implémentent la même interface :
```python
process_image(image: np.ndarray) -> List[Dict[str, Any]]
get_model_info() -> Dict[str, Any]
```

## 🔍 Détails par Moteur

### 1. EasyOCR Engine
**Spécialisation** : Tranches de livres, texte vertical, multi-langues
- **Prétraitement** : Amélioration contraste, réduction bruit
- **Détection** : Algorithmes SHELFIE + ICCV2013
- **Regroupement** : Adaptatif basé sur proximité et orientation
- **Avantages** : Haute précision (93%), robustesse images bruitées

### 2. Tesseract Engine
**Spécialisation** : Texte imprimé standard, traitement rapide
- **Prétraitement** : CLAHE, binarisation optimale
- **Configuration** : Modes PSM (Page Segmentation Mode)
- **Regroupement** : Par proximité des boîtes
- **Avantages** : Ultra-rapide (CPU), faible consommation

### 3. TrOCR Engine
**Spécialisation** : Texte manuscrit, documents historiques
- **Prétraitement** : Conversion RGB, segmentation bandes
- **Modèle** : Transformers (microsoft/trocr-base-handwritten)
- **Génération** : Beam search avec paramètres optimisés
- **Avantages** : Excellente reconnaissance manuscrit

## 🚀 Utilisation Rapide

```bash
# EasyOCR (recommandé)
cd src/engines/easyocr
python main.py ../test_images/books1.jpg --device cuda

# Tesseract (rapide)
cd src/engines/tesseract
python main.py ../test_images/books1.jpg --lang eng

# TrOCR (manuscrit)
cd src/engines/trocr
python main.py ../test_images/books1.jpg --device cuda
```

## 🔒 Indépendance des Moteurs

- ✅ **Aucun code partagé** entre moteurs
- ✅ **Dépendances isolées** par moteur
- ✅ **Évolution indépendante** possible
- ✅ **Tests unitaires** facilités

## 🎯 Avantages de l'Architecture

### Indépendance Totale
- Chaque moteur peut évoluer indépendamment
- Pas de conflits de dépendances entre moteurs
- Maintenance facilitée par moteur

### Modularité Interne
- Code organisé par responsabilité
- Facilite les tests unitaires
- Améliore la lisibilité et la maintenabilité

### Évolutivité
- Ajout de nouveaux moteurs facile
- Modification d'un moteur sans impact sur les autres
- Possibilité de versions différentes par moteur

## 📊 Comparaison des Moteurs

| Critère | EasyOCR | Tesseract | TrOCR |
|---------|---------|-----------|-------|
| **Précision** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Vitesse** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **GPU Support** | ✅ | ❌ | ✅ |
| **Texte imprimé** | ✅ | ✅ | ⚠️ |
| **Texte manuscrit** | ⚠️ | ❌ | ✅ |
| **Multi-langues** | ✅ | ✅ | ⚠️ |
| **Installation** | Simple | Système | Modèle lourd |

## 📚 Documentation

Chaque moteur possède sa propre documentation complète :
- [📖 EasyOCR](easyocr/README.md) - Architecture, commandes, exemples détaillés
- [📖 Tesseract](tesseract/README.md) - Configuration PSM, benchmarks, prérequis
- [📖 TrOCR](trocr/README.md) - Paramètres génération, cas d'usage, optimisations

---

*Architecture modulaire OCR - ShelfReader P1*
