# Informations techniques ShelfReader P1

## Architecture
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

## Algorithmes
- Détection adaptative Shelfie
- ICCC2013 (Canny)
- TrOCR (transformers)

## Dépendances
- easyocr
- torch
- streamlit
- opencv-python
- Pillow
