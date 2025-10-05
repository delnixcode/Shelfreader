# Utilisation ShelfReader P1 - Desktop

## Interface Web
- Upload d'image
- Choix du moteur OCR
- Réglage du seuil de confiance
- Visualisation des résultats et des bounding boxes
- Comparaison multi-moteurs (nouvelle page)

## Ligne de commande
```bash
python src/ocr_easyocr.py test_images/books1.jpg --gpu --confidence 0.3
```

## Conseils
- Images bien éclairées, perpendiculaires à l'étagère
- Taille recommandée : 1000px minimum
- Formats supportés : JPG, PNG
