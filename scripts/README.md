# Scripts ShelfReader

## detect.py - Détection OCR simple

**Usage :**
```bash
python scripts/detect.py <chemin_image>
```

**Exemples :**
```bash
# Depuis la racine du projet
python scripts/detect.py data/test_images/programming-books.jpg

# Avec un chemin absolu
python scripts/detect.py /home/user/images/bookshelf.jpg
```

**Ce que fait le script :**
- Utilise la classe `BookOCR` du fichier `ocr_processor.py`
- Détecte automatiquement les titres de livres sur une image
- Affiche le nombre de livres détectés et le niveau de confiance
- Liste tous les titres trouvés

**Résultat typique :**
```
📊 Résultats:
   Livres détectés: 26
   Confiance: 0.85
   Texte: Programming Ruby Ubuntu Linux C# Java...

📚 Titres détectés (26):
    1. Programming
    2. Ruby
    3. Ubuntu Linux
    4. C#
    ...
```

**Dépendances requises :**
- EasyOCR
- OpenCV
- Pillow (PIL)
- NumPy
- PyTorch

Installez-les avec :
```bash
pip install -r requirements.txt
pip install -r p1-MVP-Desktop/requirements.txt
```