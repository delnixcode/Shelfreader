# Guide d'utilisation - OCR avec validation configurable

## 🚀 Utilisation de base (sans validation)
```bash
python src/ocr_easyocr.py test_images/votre_image.jpg --confidence 0.3
```

## 🔍 Utilisation avec validation personnalisée
```bash
# Créer un fichier de titres de référence (un titre par ligne)
echo "Titre du livre 1" > titres.txt
echo "Titre du livre 2" >> titres.txt

# Lancer l'OCR avec validation
python src/ocr_easyocr.py test_images/votre_image.jpg --validate --reference-file titres.txt --confidence 0.3
```

## 📋 Options disponibles
- `--gpu` : Utiliser le GPU pour accélérer le traitement
- `--confidence 0.3` : Seuil de confiance minimum (0.1 par défaut)
- `--validate` : Activer la validation de similarité
- `--reference-file fichier.txt` : Fichier contenant les vrais titres (un par ligne)
- `--no-spine` : Désactiver la détection de tranches
- `--debug` : Mode debug (ouvre des fenêtres - nécessite interface graphique)

## 🎯 Titres de référence
- **Sans --reference-file** : Utilise les titres par défaut seulement pour books1.jpg
- **Avec --reference-file** : Charge les titres depuis votre fichier personnalisé
- **Format** : Un titre par ligne dans un fichier texte UTF-8

## 📁 Exemples de fichiers de référence
- `test_images/books2_reference.txt` : Titres pour books2.jpg
- `test_images/books3_reference.txt` : Titres pour books3.jpg

Le script fonctionne maintenant sur **n'importe quelle image** ! 🎉