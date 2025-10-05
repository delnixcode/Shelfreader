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
│   ├── processor.py   # Classe principale
│   ├── config.py      # Paramètres et configuration
│   ├── preprocessing/ # Amélioration d'images
│   ├── detection/     # Algos détection texte
│   ├── grouping/      # Regroupement résultats
│   └── models/        # Classes de données
├── tesseract/         # Moteur Tesseract rapide
│   ├── README.md      # Documentation complète
│   ├── processor.py   # Classe principale
│   ├── config.py      # Configurations PSM
│   ├── preprocessing/ # CLAHE et filtres
│   └── grouping/      # Regroupement proximité
├── trocr/            # Moteur TrOCR manuscrit
│   ├── README.md      # Documentation complète
│   ├── processor.py   # Classe principale
│   ├── config.py      # Paramètres génération
│   ├── preprocessing/ # Conversion RGB
│   ├── detection/     # Segmentation bandes
│   └── grouping/      # Regroupement temporel
└── README.md          # Cette documentation
```

## 🎯 Architecture de Chaque Moteur

### Composants Standards
1. **`processor.py`** - Orchestrateur principal du pipeline OCR
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

## 🚀 Utilisation Rapide

```bash
# EasyOCR (recommandé)
cd src/engines/easyocr
python main.py ../../../../test_images/books1.jpg --device cuda

# Tesseract (rapide)
cd src/engines/tesseract
python main.py ../../../../test_images/books1.jpg --lang eng

# TrOCR (manuscrit)
cd src/engines/trocr
python main.py ../../../../test_images/books1.jpg --device cuda
```

## 🔒 Indépendance des Moteurs

- ✅ **Aucun code partagé** entre moteurs
- ✅ **Dépendances isolées** par moteur
- ✅ **Évolution indépendante** possible
- ✅ **Tests unitaires** facilités

## 📚 Documentation

Chaque moteur possède sa propre documentation complète :
- [📖 EasyOCR](easyocr/README.md) - Architecture, commandes, exemples
- [📖 Tesseract](tesseract/README.md) - Configuration PSM, benchmarks
- [� TrOCR](trocr/README.md) - Paramètres génération, cas d'usage

---

*Architecture modulaire OCR - ShelfReader P1*</content>
<parameter name="filePath">/home/delart/Documents/dev/python/Shelfreader/p1-OCR-Streamlit/src/engines/globale-explanation.md