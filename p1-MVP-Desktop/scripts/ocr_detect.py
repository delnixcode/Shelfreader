#!/usr/bin/env python3
"""
ShelfReader - Script de détection OCR simple
Usage: python scripts/ocr_detect.py <image_path> [--gpu] [--easyocr|--tesseract]
"""

import sys
import os
import argparse
from pathlib import Path

def main():
    """Fonction principale du script de détection OCR."""
    
    # Parser les arguments
    parser = argparse.ArgumentParser(description='ShelfReader - Détection OCR de livres')
    parser.add_argument('image_path', help='Chemin vers l\'image à analyser')
    parser.add_argument('--gpu', action='store_true', help='Utiliser le GPU pour l\'OCR (plus rapide)')
    parser.add_argument('--easyocr', action='store_true', help='Utiliser EasyOCR (par défaut)')
    parser.add_argument('--tesseract', action='store_true', help='Utiliser Tesseract au lieu d\'EasyOCR')
    
    args = parser.parse_args()
    image_path = args.image_path
    use_gpu = args.gpu
    use_easyocr = args.easyocr
    use_tesseract = args.tesseract

    # Validation des options OCR
    if use_easyocr and use_tesseract:
        print("❌ Erreur: Vous ne pouvez pas utiliser --easyocr et --tesseract en même temps")
        sys.exit(1)
    
    # Déterminer le moteur OCR à utiliser
    # Par défaut: EasyOCR, sauf si --tesseract est spécifié
    final_use_tesseract = use_tesseract and not use_easyocr

    # Vérifier que le fichier image existe
    if not os.path.exists(image_path):
        print(f"❌ Image introuvable: {image_path}")
        print("💡 Images de test disponibles dans le dossier test_images/")
        print("   Ou créez une image avec du texte pour tester l'OCR")
        sys.exit(1)

    # Afficher le début de l'analyse
    ocr_type = "Tesseract" if final_use_tesseract else "EasyOCR"
    device_info = "GPU 🚀" if use_gpu else "CPU"
    print(f"🔍 Analyse OCR de: {image_path} ({ocr_type} - {device_info})")

    try:
        # Configuration du chemin d'import
        script_dir = Path(__file__).parent
        src_dir = script_dir.parent / "src"
        sys.path.insert(0, str(src_dir))

        # Import des modules
        from ocr_processor import BookOCR
        from PIL import Image

        # Initialisation de l'OCR avec options
        processor = BookOCR(['en'], 0.2, use_gpu=use_gpu, use_tesseract=final_use_tesseract)

        # Chargement et traitement de l'image
        pil_image = Image.open(image_path)
        
        text, confidence = processor.get_text_and_confidence(pil_image, preprocess=False)
        boxes = processor.get_boxes(pil_image, preprocess=False)
        books = processor.get_books(pil_image, preprocess=False)

        # Affichage des résultats
        print(f"\n📊 Résultats:")
        print(f"   Textes détectés: {len(boxes)}")
        print(f"   Livres détectés: {len(books)}")
        print(f"   Confiance: {confidence:.2f}")
        print(f"   Texte: {text[:80]}{'...' if len(text) > 80 else ''}")

        if books:
            print(f"\n📚 Livres détectés ({len(books)}):")
            for i, book in enumerate(books, 1):
                print(f"   {i:2d}. {book['title']}")
                if book['text_count'] > 1:
                    other_texts = ', '.join(book['all_texts'][:3])
                    print(f"       └─ (+{book['text_count']-1} textes: {other_texts})")

        print("\n✅ Analyse terminée!")

    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("Installez les dépendances: pip install -r requirements.txt")

    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()