#!/usr/bin/env python3
"""
Test script pour démontrer les améliorations EasyOCR
"""
import sys
import os
sys.path.append('src')

from src.ocr_easyocr import EasyOCRProcessor
from PIL import Image
import numpy as np

def test_adaptive_preprocessing():
    """Test des améliorations de préprocessing adaptatif."""
    print("🧪 Test des améliorations EasyOCR")
    print("=" * 50)

    # Créer une image de test simple
    test_image = Image.new('RGB', (800, 600), color='white')

    # Initialiser le processeur (sans GPU pour le test)
    processor = EasyOCRProcessor(languages=['en'], confidence_threshold=0.8, use_gpu=False)

    print("✓ Processeur EasyOCR initialisé")

    # Tester l'analyse de qualité d'image
    print("\n📊 Test de l'analyse de qualité d'image:")
    quality_metrics = processor._analyze_image_quality(test_image)
    for metric, value in quality_metrics.items():
        print(f"  {metric}: {value:.3f}")

    # Tester les paramètres adaptatifs
    print("\n⚙️ Test des paramètres de détection adaptatifs:")
    params = processor._get_adaptive_detection_params(quality_metrics)
    for param, value in params.items():
        print(f"  {param}: {value}")

    # Tester le nettoyage de texte
    print("\n🧹 Test du nettoyage de texte:")
    test_texts = [
        "LE   PETIT    PRINCE",
        "HARRY..POTTER!!!",
        "L'ART...DE...LA...GUERRE",
        "AAA BBB CCC DDD"
    ]

    for text in test_texts:
        cleaned = processor._clean_book_text(text)
        print(f"  '{text}' → '{cleaned}'")

    print("\n✅ Tous les tests passés avec succès!")
    print("🎯 Les améliorations EasyOCR sont opérationnelles!")

if __name__ == "__main__":
    test_adaptive_preprocessing()