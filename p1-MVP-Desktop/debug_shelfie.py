#!/usr/bin/env python3
"""
Script de débogage pour la méthode Shelfie
"""

import cv2
import numpy as np
import sys

# Charger l'image
image_path = "test_images/books1.jpg"
image = cv2.imread(image_path)

if image is None:
    print(f"❌ Impossible de charger l'image: {image_path}")
    sys.exit(1)

print(f"✅ Image chargée: {image.shape}")

# Importer le processeur
from src.ocr_easyocr import EasyOCRProcessor

# Créer une instance
processor = EasyOCRProcessor(['en'], 0.3, use_gpu=False)

# Tester la détection de lignes avec debug
print("\n🔍 Test de détection de lignes (méthode Shelfie)...")
lines = processor._detect_spine_lines_shelfie(image, debug=False)

print(f"\n📊 Résultat: {len(lines)} lignes détectées")

if lines:
    print("\nPositions des lignes (X center):")
    for i, line in enumerate(lines):
        print(f"  Ligne {i+1}: X={line.center[0]:.1f}, Y={line.center[1]:.1f}")
else:
    print("❌ Aucune ligne détectée - la méthode a échoué")
    
    # Essayer avec debug pour voir où ça bloque
    print("\n🔍 Nouvelle tentative avec debug activé...")
    lines = processor._detect_spine_lines_shelfie(image, debug=True)
