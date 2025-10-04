#!/usr/bin/env python3
"""
ShelfReader - Détection OCR simple
Usage: python scripts/detect.py <image_path>
"""

import sys
import os
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("📚 ShelfReader - Détection OCR")
        print("Usage: python scripts/detect.py <image_path>")
        print("Example: python scripts/detect.py data/test_images/programming-books.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(f"❌ Image introuvable: {image_path}")
        sys.exit(1)

    print(f"🔍 Analyse OCR de: {image_path}")

    try:
        # Importer depuis p1-MVP-Desktop/src
        script_dir = Path(__file__).parent
        src_dir = script_dir.parent / "p1-MVP-Desktop" / "src"
        sys.path.insert(0, str(src_dir))

        from ocr_processor import BookOCR
        from PIL import Image

        # Initialiser l'OCR
        processor = BookOCR(['en'], 0.2)

        # Charger l'image
        pil_image = Image.open(image_path)

        # Détecter le texte (sans préprocessing pour meilleurs résultats)
        text, confidence = processor.get_text_and_confidence(pil_image, preprocess=False)
        boxes = processor.get_boxes(pil_image, preprocess=False)

        # Afficher les résultats
        print(f"\n📊 Résultats:")
        print(f"   Livres détectés: {len(boxes)}")
        print(f"   Confiance: {confidence:.2f}")
        print(f"   Texte: {text[:100]}{'...' if len(text) > 100 else ''}")

        if boxes:
            print(f"\n📚 Titres détectés ({len(boxes)}):")
            for i, box in enumerate(boxes, 1):
                title = box['text'].strip()
                if title:
                    print(f"   {i:2d}. {title}")

        print("\n✅ Analyse terminée!")

    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("Vérifiez que les dépendances sont installées:")
        print("   pip install -r requirements.txt")
        print("   pip install -r p1-MVP-Desktop/requirements.txt")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()