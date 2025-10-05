# DÉPENDANCES:
#   - Utilise: __init__.py (import du moteur), engines.tesseract (module parent)
#   - Importe: argparse, sys, os, cv2, time, pathlib, PIL, json
#   - Utilisé par: Utilisateur final (script exécutable)

#!/usr/bin/env python3
"""
ShelfReader - Tesseract Engine Main Script
Script principal pour tester le moteur Tesseract en ligne de commande.
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

from engines.tesseract import TesseractOCRProcessor

def main():
    parser = argparse.ArgumentParser(
        description='Test du moteur Tesseract avec une image',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py image.jpg
  python main.py image.jpg --lang eng fra --confidence 0.6
  python main.py image.jpg --psm 8 --benchmark
  python main.py image.jpg --output results.json
        """
    )

    parser.add_argument('image_path', help='Chemin vers l\'image à traiter')
    parser.add_argument('--lang', nargs='+', default=['eng'],
                       help='Langues Tesseract à utiliser (ex: eng fra deu)')
    parser.add_argument('--confidence', type=float, default=0.5,
                       help='Seuil de confiance minimum (0.0-1.0)')
    parser.add_argument('--psm', type=str, default='6',
                       help='Page Segmentation Mode (ex: 6, 8, 11)')
    parser.add_argument('--cpu', action='store_true',
                       help='Forcer l\'utilisation du CPU (Tesseract est CPU-only)')
    parser.add_argument('--gpu', action='store_true',
                       help='Non supporté par Tesseract (CPU-only)')
    parser.add_argument('--debug', action='store_true',
                       help='Mode debug avec informations détaillées')
    parser.add_argument('--benchmark', action='store_true',
                       help='Afficher les métriques de performance')
    parser.add_argument('--output', type=str,
                       help='Fichier de sortie pour les résultats (JSON)')

    args = parser.parse_args()

    # Validation des arguments
    if args.gpu:
        print("⚠️ Avertissement: Tesseract est CPU-only, l'option --gpu est ignorée")
    if args.cpu and args.gpu:
        print("❌ Erreur: --cpu et --gpu sont mutuellement exclusifs")
        return 1

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

        # Mode debug
        if args.debug:
            print(f"🐛 DEBUG - Arguments: {vars(args)}")
            print(f"🐛 DEBUG - Tesseract est CPU-only")

        # Initialiser le processeur
        print("🚀 Initialisation du moteur Tesseract...")
        print(f"   Langues: {args.lang}")
        print(f"   Seuil de confiance: {args.confidence}")
        print(f"   PSM: {args.psm}")
        print(f"   Device: CPU (Tesseract est CPU-only)")

        start_init = time.time()
        processor = TesseractOCRProcessor(
            languages=args.lang,
            confidence_threshold=args.confidence
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

        # Sauvegarde automatique dans result-ocr
        from datetime import datetime
        result_ocr_dir = current_dir.parent.parent.parent / "result-ocr"
        result_ocr_dir.mkdir(exist_ok=True)
        result_file = result_ocr_dir / "tesseract_results.txt"

        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"=== RÉSULTATS OCR - {os.path.basename(args.image_path)} ===\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Nombre de textes détectés: {len(results)}\n")

            if results:
                confidences = [r.get('confidence', 0) for r in results]
                avg_confidence = sum(confidences) / len(confidences)
                f.write(f"Confiance moyenne: {avg_confidence:.3f}\n")
            else:
                f.write("Confiance moyenne: 0.000\n")

            f.write("\nTEXTE COMPLET:\n")
            if results:
                for result in results:
                    text = result.get('text', '').strip()
                    confidence = result.get('confidence', 0)
                    f.write(f"{text} (conf: {confidence:.2f})\n")
            else:
                f.write("(aucun texte détecté)\n")

            f.write("\n")

            if results:
                f.write("DÉTAIL PAR LIVRE:\n")
                for i, result in enumerate(results, 1):
                    f.write(f"\n--- Livre {i} ---\n")
                    confidence = result.get('confidence', 0)
                    text = result.get('text', '').strip()
                    f.write(f"Confiance: {confidence:.3f}\n")
                    f.write(f"Texte: {text}\n")

        print(f"💾 Résultats sauvegardés automatiquement dans: {result_file}")

        # Sauvegarder les résultats si demandé
        if args.output:
            import json
            output_data = {
                'engine': 'tesseract',
                'image_path': args.image_path,
                'parameters': {
                    'languages': args.lang,
                    'confidence_threshold': args.confidence,
                    'psm_config': args.psm
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
    exit(main())