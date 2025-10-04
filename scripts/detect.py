#!/usr/bin/env python3
"""
ShelfReader - Script de détection OCR simple
=============================================

Ce script permet de détecter automatiquement les titres de livres
sur une image de bibliothèque en utilisant la classe BookOCR.

Usage: python scripts/detect.py <chemin_vers_image>

Auteur: ShelfReader Team
"""

import sys
import os
from pathlib import Path

def main():
    """
    Fonction principale du script de détection OCR.

    Vérifie les arguments, charge l'image, exécute l'OCR
    et affiche les résultats formatés.
    """

    # Vérification des arguments de ligne de commande
    if len(sys.argv) != 2:
        # Afficher l'aide si pas assez d'arguments
        print("📚 ShelfReader - Détection OCR")
        print("Usage: python scripts/detect.py <image_path>")
        print("Example: python scripts/detect.py data/test_images/programming-books.jpg")
        sys.exit(1)

    # Récupérer le chemin de l'image depuis les arguments
    image_path = sys.argv[1]

    # Vérifier que le fichier image existe
    if not os.path.exists(image_path):
        print(f"❌ Image introuvable: {image_path}")
        sys.exit(1)

    # Afficher le début de l'analyse
    print(f"🔍 Analyse OCR de: {image_path}")

    try:
        # === CONFIGURATION DU CHEMIN D'IMPORT ===
        # Le script doit importer la classe BookOCR depuis p1-MVP-Desktop/src/
        # On ajoute dynamiquement ce chemin au PYTHONPATH

        # Obtenir le répertoire du script actuel
        script_dir = Path(__file__).parent  # /path/to/Shelfreader/scripts/

        # Construire le chemin vers le dossier src de P1
        src_dir = script_dir.parent / "p1-MVP-Desktop" / "src"  # /path/to/Shelfreader/p1-MVP-Desktop/src/

        # Ajouter ce chemin au début de sys.path pour les imports
        sys.path.insert(0, str(src_dir))

        # === IMPORT DES MODULES ===
        # Importer la classe BookOCR depuis ocr_processor.py
        from ocr_processor import BookOCR

        # Importer PIL pour le chargement d'images
        from PIL import Image

        # === INITIALISATION DE L'OCR ===
        # Créer une instance de BookOCR avec:
        # - Langues: ['en'] (anglais)
        # - Seuil de confiance: 0.2 (légèrement permissif)
        processor = BookOCR(['en'], 0.2)

        # === CHARGEMENT DE L'IMAGE ===
        # Ouvrir l'image avec PIL (Python Imaging Library)
        pil_image = Image.open(image_path)

        # === DÉTECTION DU TEXTE ===
        # Appeler les méthodes de détection sans préprocessing
        # (le préprocessing dégradait la qualité de détection)

        # Obtenir le texte complet et la confiance moyenne
        text, confidence = processor.get_text_and_confidence(pil_image, preprocess=False)

        # Obtenir la liste détaillée des boîtes de texte détectées
        boxes = processor.get_boxes(pil_image, preprocess=False)

        # === AFFICHAGE DES RÉSULTATS ===

        # Section principale des résultats
        print(f"\n📊 Résultats:")
        print(f"   Livres détectés: {len(boxes)}")  # Nombre total de textes détectés
        print(f"   Confiance: {confidence:.2f}")     # Confiance moyenne (0.0 à 1.0)
        print(f"   Texte: {text[:100]}{'...' if len(text) > 100 else ''}")  # Aperçu du texte

        # Lister tous les titres détectés individuellement
        if boxes:
            print(f"\n📚 Titres détectés ({len(boxes)}):")
            for i, box in enumerate(boxes, 1):
                # Extraire et nettoyer le titre
                title = box['text'].strip()
                # N'afficher que les titres non vides
                if title:
                    print(f"   {i:2d}. {title}")  # Format: "  1. Titre du livre"

        # Message de fin
        print("\n✅ Analyse terminée!")

    # === GESTION DES ERREURS ===

    except ImportError as e:
        # Erreur d'import des modules (dépendances manquantes)
        print(f"❌ Erreur d'import: {e}")
        print("Vérifiez que les dépendances sont installées:")
        print("   pip install -r requirements.txt")
        print("   pip install -r p1-MVP-Desktop/requirements.txt")

    except Exception as e:
        # Toute autre erreur inattendue
        print(f"❌ Erreur: {e}")

# === POINT D'ENTRÉE DU SCRIPT ===
# Cette section s'exécute seulement si le script est lancé directement
# (pas quand il est importé comme module)
if __name__ == "__main__":
    main()