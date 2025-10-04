#!/usr/bin/env python3
"""
ShelfReader - Script de détection OCR simple
Usage: python scripts/ocr_detect.py <image_path> [--gpu] [--easyocr|--tesseract]
"""

import sys
import os
import argparse
from pathlib import Path

def _group_books_by_boxes(boxes, vertical_threshold=50):
    """Regroupe les textes par livre et reconstitue les titres."""
    if not boxes:
        return []
    
    # Filtrer: garder seulement les textes verticaux avec grandes polices
    vertical_boxes = [b for b in boxes if b.get('is_vertical', False)]
    
    if not vertical_boxes:
        return []
    
    # Calculer la médiane de la taille de police
    font_sizes = [b['font_size'] for b in vertical_boxes]
    median_font_size = sorted(font_sizes)[len(font_sizes) // 2]
    
    # Garder seulement les grandes polices (> 80% de la médiane)
    large_text_boxes = [b for b in vertical_boxes if b['font_size'] >= median_font_size * 0.8]
    
    # Trier par position X (gauche à droite)
    sorted_boxes = sorted(large_text_boxes, key=lambda b: b['x'])
    
    # Regrouper par colonnes (même livre)
    books = []
    current_book = [sorted_boxes[0]]
    current_x = sorted_boxes[0]['x']
    
    for box in sorted_boxes[1:]:
        if abs(box['x'] - current_x) <= vertical_threshold:
            current_book.append(box)
        else:
            books.append(current_book)
            current_book = [box]
            current_x = box['x']
    
    if current_book:
        books.append(current_book)
    
    # Extraire les titres
    formatted_books = []
    for book_texts in books:
        title = _extract_book_title(book_texts)
        formatted_books.append({
            'title': title,
            'x': book_texts[0]['x'],
            'all_texts': [b['text'] for b in book_texts],
            'text_count': len(book_texts)
        })
    
    return formatted_books

def _extract_book_title(book_texts):
    """Combine tous les textes détectés pour former un titre approximatif."""
    if not book_texts:
        return "Unknown"
    
    # Trier par position Y (du haut vers le bas du livre)
    sorted_texts = sorted(book_texts, key=lambda b: b['y'])
    
    # Combiner tous les textes
    all_texts = [b['text'].strip() for b in sorted_texts]
    combined = ' / '.join(all_texts)
    
    # Limiter la longueur
    if len(combined) > 60:
        combined = combined[:60] + '...'
    
    return combined

def main():
    """Fonction principale du script de détection OCR."""
    
    # Parser les arguments
    parser = argparse.ArgumentParser(description='ShelfReader - Détection OCR de livres')
    parser.add_argument('image_path', help='Chemin vers l\'image à analyser')
    parser.add_argument('--gpu', action='store_true', help='Utiliser le GPU pour l\'OCR (plus rapide)')
    parser.add_argument('--easyocr', action='store_true', help='Utiliser EasyOCR (par défaut)')
    parser.add_argument('--tesseract', action='store_true', help='Utiliser Tesseract au lieu d\'EasyOCR')
    parser.add_argument('--trocr', action='store_true', help='Utiliser TrOCR (Transformers-based OCR)')
    
    args = parser.parse_args()
    image_path = args.image_path
    use_gpu = args.gpu
    use_easyocr = args.easyocr
    use_tesseract = args.tesseract
    use_trocr = args.trocr

    # Validation des options OCR
    ocr_options = [use_easyocr, use_tesseract, use_trocr]
    if sum(ocr_options) > 1:
        print("❌ Erreur: Vous ne pouvez utiliser qu'une seule option OCR à la fois")
        print("   Options: --easyocr, --tesseract, --trocr")
        sys.exit(1)
    
    # Déterminer le moteur OCR à utiliser
    # Par défaut: EasyOCR, sauf si une option spécifique est choisie
    final_use_trocr = use_trocr
    final_use_tesseract = use_tesseract and not use_trocr
    final_use_easyocr = not (use_tesseract or use_trocr)

    # Vérifier que le fichier image existe
    if not os.path.exists(image_path):
        print(f"❌ Image introuvable: {image_path}")
        print("💡 Images de test disponibles dans le dossier test_images/")
        print("   Ou créez une image avec du texte pour tester l'OCR")
        sys.exit(1)

    # Afficher le début de l'analyse
    ocr_type = "TrOCR" if final_use_trocr else ("Tesseract" if final_use_tesseract else "EasyOCR")
    device_info = "GPU 🚀" if use_gpu else "CPU"
    print(f"🔍 Analyse OCR de: {image_path} ({ocr_type} - {device_info})")

    try:
        # Configuration du chemin d'import
        import os as os_module
        script_dir = os_module.path.dirname(os_module.path.abspath(__file__))
        src_dir = os_module.path.join(script_dir, '..', 'src')
        sys.path.insert(0, src_dir)

        # Import des modules OCR
        from ocr_easyocr import EasyOCRProcessor
        from ocr_tesseract import TesseractOCRProcessor
        from ocr_trocr import TrOCRProcessor
        from PIL import Image

        # Initialisation du processeur OCR selon l'option choisie
        if final_use_trocr:
            processor = TrOCRProcessor(['en'], 0.2, use_gpu=use_gpu)
            ocr_type = "TrOCR"
        elif final_use_tesseract:
            processor = TesseractOCRProcessor('eng', 0.2, use_gpu=use_gpu)
            ocr_type = "Tesseract"
        else:
            processor = EasyOCRProcessor(['en'], 0.2, use_gpu=use_gpu)
            ocr_type = "EasyOCR"

        # Chargement et traitement de l'image
        pil_image = Image.open(image_path)
        
        text, confidence = processor.get_text_and_confidence(pil_image, preprocess=False)
        boxes = processor.get_boxes(pil_image, preprocess=False)
        books = _group_books_by_boxes(boxes)

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