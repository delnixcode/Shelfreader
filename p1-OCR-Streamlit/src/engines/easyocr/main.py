# DÉPENDANCES:
#   - Utilise: __init__.py (import du moteur), engines.easyocr (module parent)
#   - Importe: argparse, sys, os, cv2, time, pathlib, PIL, json
#   - Utilisé par: Utilisateur final (script exécutable)

#!/usr/bin/env python3
"""
ShelfReader - EasyOCR Engine Main Script
Script principal pour tester le moteur EasyOCR en ligne de commande.
"""

import argparse
import sys
import os
import cv2
import time
from pathlib import Path
from PIL import Image

# Ajouter le répertoire src au path pour les imports
current_dir = Path(__file__).parent
src_dir = current_dir.parent.parent  # Remonter à src/
sys.path.insert(0, str(src_dir))

from engines.easyocr import EasyOCRProcessor

def main():
    parser = argparse.ArgumentParser(
        description='Test du moteur EasyOCR avec une image',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py image.jpg
  python main.py image.jpg --lang fr --confidence 0.7 --gpu
  python main.py image.jpg --benchmark
        """
    )

    parser.add_argument('image_path', help='Chemin vers l\'image à traiter')
    parser.add_argument('--lang', nargs='+', default=['en'],
                       help='Langues à utiliser (ex: en fr de)')
    parser.add_argument('--confidence', type=float, default=0.5,
                       help='Seuil de confiance minimum (0.0-1.0)')
    parser.add_argument('--gpu', action='store_true',
                       help='Utiliser le GPU si disponible')
    parser.add_argument('--benchmark', action='store_true',
                       help='Afficher les métriques de performance')
    parser.add_argument('--output', type=str,
                       help='Fichier de sortie pour les résultats (JSON)')

    args = parser.parse_args()

    # Vérifier que l'image existe
    if not os.path.exists(args.image_path):
        print(f"❌ Erreur: Image '{args.image_path}' non trouvée")
        return 1

    try:
        # Charger l'image
        print(f"📷 Chargement de l'image: {args.image_path}")
        image = cv2.imread(args.image_path)

        if image is None:
            print("❌ Erreur: Impossible de charger l'image")
            return 1

        print(f"📊 Dimensions: {image.shape[1]}x{image.shape[0]} pixels")

        # Initialiser le processeur
        print("🚀 Initialisation du moteur EasyOCR...")
        print(f"   Langues: {args.lang}")
        print(f"   Seuil de confiance: {args.confidence}")
        print(f"   GPU: {'Activé' if args.gpu else 'Désactivé'}")

        start_init = time.time()
        processor = EasyOCRProcessor(
            languages=args.lang,
            confidence_threshold=args.confidence,
            use_gpu=args.gpu
        )
        init_time = time.time() - start_init
        print(f"   Temps d'initialisation: {init_time:.2f}s")
        # Traiter l'image
        print("🔍 Analyse de l'image en cours...")
        start_process = time.time()
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        results = processor.get_boxes(pil_image)
        process_time = time.time() - start_process

        # Afficher les résultats
        print(f"\n📋 RÉSULTATS ({len(results)} éléments trouvés)")
        print("=" * 50)

        if results:
            for i, result in enumerate(results, 1):
                text = result.get('text', '').strip()
                confidence = result.get('confidence', 0)
                bbox = [result.get('x', 0), result.get('y', 0), result.get('width', 0), result.get('height', 0)]

                print(f"{i:2d}. \"{text}\"")
                print(f"    Confiance: {confidence:.2f}")
                print(f"    Position: {bbox}")
                print()

            # Statistiques
            confidences = [r.get('confidence', 0) for r in results]
            avg_confidence = sum(confidences) / len(confidences)
            min_confidence = min(confidences)
            max_confidence = max(confidences)

            print("📊 STATISTIQUES")
            print(f"   Confiance moyenne: {avg_confidence:.2f}")
            print(f"   Confiance min: {min_confidence:.2f}")
            print(f"   Confiance max: {max_confidence:.2f}")
        else:
            print("⚠️ Aucun texte détecté dans l'image")

        # Métriques de performance
        if args.benchmark:
            print("\n⏱️ PERFORMANCES")
            print(f"   Temps d'initialisation: {init_time:.2f}s")
            print(f"   Temps de traitement: {process_time:.2f}s")
            print(f"   Temps total: {init_time + process_time:.2f}s")
            print(f"   FPS: {1.0 / process_time:.1f}")
        # Sauvegarder les résultats si demandé
        if args.output:
            import json
            output_data = {
                'engine': 'easyocr',
                'image_path': args.image_path,
                'parameters': {
                    'languages': args.lang,
                    'confidence_threshold': args.confidence,
                    'use_gpu': args.gpu
                },
                'results': results,
                'performance': {
                    'init_time': init_time,
                    'process_time': process_time,
                    'total_time': init_time + process_time
                },
                'timestamp': time.time()
            }

            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Résultats sauvegardés dans: {args.output}")

        print("\n✅ Traitement terminé avec succès!")
        return 0

    except Exception as e:
        print(f"❌ Erreur lors du traitement: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())