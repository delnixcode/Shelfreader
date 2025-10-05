# DÉPENDANCES:
#   - Utilise: __init__.py (import du moteur), engines.trocr (module parent)
#   - Importe: argparse, sys, os, cv2, time, pathlib, PIL, json
#   - Utilisé par: Utilisateur final (script exécutable)

#!/usr/bin/env python3
"""
ShelfReader - TrOCR Engine Main Script
Script principal pour tester le moteur TrOCR en ligne de commande.
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

from engines.trocr import ShelfReaderTrOCRProcessor

def main():
    parser = argparse.ArgumentParser(
        description='Test du moteur TrOCR avec une image',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py image.jpg
  python main.py image.jpg --device cuda --benchmark
  python main.py image.jpg --output results.json
        """
    )

    parser.add_argument('image_path', help='Chemin vers l\'image à traiter')
    parser.add_argument('--device', choices=['cpu', 'cuda', 'auto'], default='auto',
                       help='Device pour l\'inférence (cpu, cuda, auto)')
    parser.add_argument('--cpu', action='store_true',
                       help='Forcer l\'utilisation du CPU')
    parser.add_argument('--gpu', action='store_true',
                       help='Forcer l\'utilisation du GPU')
    parser.add_argument('--debug', action='store_true',
                       help='Mode debug avec informations détaillées')
    parser.add_argument('--benchmark', action='store_true',
                       help='Afficher les métriques de performance')
    parser.add_argument('--output', type=str,
                       help='Fichier de sortie pour les résultats (JSON)')

    args = parser.parse_args()

    # Validation des arguments
    if args.cpu and args.gpu:
        print("❌ Erreur: --cpu et --gpu sont mutuellement exclusifs")
        return 1

    # Avertissements pour conflits explicites entre flags et --device
    # On ne change pas la logique de priorité existante (flags > --device),
    # mais on informe l'utilisateur si sa combinaison d'arguments est contradictoire.
    if args.cpu and args.device == 'cuda':
        print("⚠️ Conflit d'arguments: vous avez demandé '--cpu' mais aussi '--device cuda'. '--cpu' aura la priorité et forcera l'exécution sur CPU.")
    if args.gpu and args.device == 'cpu':
        print("⚠️ Conflit d'arguments: vous avez demandé '--gpu' mais aussi '--device cpu'. '--gpu' aura la priorité et forcera l'exécution sur GPU.")

    # Configuration du device
    if args.cpu:
        device = 'cpu'
    elif args.gpu:
        device = 'cuda'
    else:
        device = args.device

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
            print(f"🐛 DEBUG - Device configuré: {device}")

        # Initialiser le processeur
        print("🚀 Initialisation du moteur TrOCR...")
        print(f"   Device: {device}")

        start_init = time.time()
        processor = ShelfReaderTrOCRProcessor(device=device)
        init_time = time.time() - start_init
        print(f"   Temps d'initialisation: {init_time:.2f}s")
        # Afficher les infos du modèle
        model_info = processor.get_model_info()
        print(f"   Modèle: {model_info['model_name']}")
        print(f"   Device utilisé: {model_info['device']}")
        print(f"   Paramètres: {model_info['model_parameters']:,}")

        # Traiter l'image
        print("🔍 Analyse de l'image en cours...")
        start_process = time.time()
        results = processor.process_image(image)
        process_time = time.time() - start_process

        # Afficher les résultats
        print(f"\n📋 RÉSULTATS ({len(results)} éléments trouvés)")
        print("=" * 50)

        if results:
            for i, result in enumerate(results, 1):
                text = result.get('text', '').strip()
                confidence = result.get('confidence', 0)
                bbox = result.get('bbox', [])

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
        result_file = result_ocr_dir / "trocr_results.txt"

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
                'engine': 'trocr',
                'image_path': args.image_path,
                'parameters': {
                    'device': args.device
                },
                'model_info': model_info,
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