# ShelfReader P1 - Architecture Modulaire

## Vue d'ensemble

ShelfReader P1 est une application Streamlit pour l'analyse OCR adaptative multi-échelle avec détection intelligente de livres sur étagères.

## Architecture

```
src/frontend/
├── main.py                 # Point d'entrée principal
├── pages/                  # Pages Streamlit
│   ├── __init__.py
│   ├── analysis_page.py    # Page d'analyse OCR
│   └── comparison_page.py  # Page de comparaison OCR
├── components/             # Composants réutilisables
│   ├── __init__.py
│   ├── sidebar.py          # Navigation et informations
│   ├── results_display.py  # Affichage des résultats
│   └── visualization.py    # Visualisations et graphs
└── utils/                  # Logique métier
    ├── __init__.py
    ├── ocr_processing.py   # Traitement OCR unifié
    └── openlibrary_enrichment.py  # Enrichissement Open Library
```

## Lancement

```bash
cd p1-OCR-Streamlit
source ../env-p1/bin/activate
streamlit run src/frontend/main.py --server.headless true --server.port 8501
```

## Fonctionnalités

- **Analyse OCR** : Traitement d'images avec moteurs EasyOCR, Tesseract, TrOCR
- **Enrichissement** : Métadonnées Open Library (titres, auteurs, couvertures)
- **Comparaison** : Évaluation comparative des moteurs OCR
- **Visualisation** : Bounding boxes et graphiques interactifs
- **GPU Support** : Accélération automatique si disponible

## Moteurs OCR

- **EasyOCR** : Spécialisé détection livres, algorithme adaptatif "shelfie"
- **Tesseract** : Moteur classique rapide et fiable
- **TrOCR** : Basé transformers, précision maximale

## Métriques

- Précision : 93% (14/15 livres sur books1.jpg)
- GPU : Support automatique avec fallback CPU
- Temps traitement : ~2-5 secondes selon moteur et GPU