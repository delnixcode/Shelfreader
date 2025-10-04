#!/usr/bin/env python3
"""
Démonstration des améliorations OCR ShelfReader
Compare les différentes méthodes de traitement OCR.
"""

import os
import sys
from PIL import Image

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ocr_easyocr import EasyOCRProcessor

def demo_ocr_improvements():
    """Démontre les améliorations OCR avec différentes configurations."""

    print("🚀 Démonstration des améliorations OCR ShelfReader")
    print("=" * 60)

    # Configuration des tests
    image_path = "test_images/books1.jpg"
    if not os.path.exists(image_path):
        print(f"❌ Image non trouvée: {image_path}")
        return

    # Titres de référence pour validation
    reference_titles = [
        "Ada 95",
        "Software Construction",
        "THE C PROGRAMMING LANGUAGE",
        "THE C++ PROGRAMMING LANGUAGE",
        "THE DYLAN REFERENCE MANUAL",
        "The Java Programming Language",
        "The Little MLer",
        "ELEMENTS OF ML PROGRAMMING",
        "Miranda: The Craft of Functional Programming",
        "Programming Perl",
        "Learning Python",
        "Systems Programming with Modula-3",
        "THE SCHEME PROGRAMMING LANGUAGE",
        "Squeak: Open Personal Computing and Multimedia",
        "The π-calculus: A Theory of Mobile Processes"
    ]

    # Tests avec différentes configurations
    configs = [
        {"name": "GPU + Spine Detection", "gpu": True, "spine": True, "validate": False},
        {"name": "GPU + Spine + Validation", "gpu": True, "spine": True, "validate": True},
        {"name": "GPU + Proximity Only", "gpu": True, "spine": False, "validate": False},
        {"name": "CPU + Spine Detection", "gpu": False, "spine": True, "validate": False},
    ]

    pil_image = Image.open(image_path)

    for config in configs:
        print(f"\n🔧 Configuration: {config['name']}")
        print("-" * 40)

        try:
            # Initialisation du processeur
            processor = EasyOCRProcessor(['en'], 0.1, config['gpu'])

            # Traitement
            ref_titles = reference_titles if config['validate'] else None
            boxes = processor.get_boxes(
                pil_image,
                preprocess=False,
                use_spine_detection=config['spine'],
                reference_titles=ref_titles
            )

            text, confidence = processor.get_text_and_confidence(
                pil_image,
                preprocess=False,
                use_spine_detection=config['spine'],
                reference_titles=ref_titles
            )

            # Résultats
            print(f"📊 Livres détectés: {len(boxes)}")
            print(f"🎯 Confiance moyenne: {confidence:.3f}")
            print(f"📝 Aperçu: {text[:100]}{'...' if len(text) > 100 else ''}")

        except Exception as e:
            print(f"❌ Erreur: {e}")

    print("\n" + "=" * 60)
    print("✅ Démonstration terminée!")
    print("\n📋 Résumé des améliorations:")
    print("• GPU support avec PyTorch CUDA")
    print("• Détection de tranches shelfie")
    print("• Validation de similarité")
    print("• Gestion d'erreurs robuste")
    print("• Code consolidé et optimisé")

if __name__ == "__main__":
    demo_ocr_improvements()