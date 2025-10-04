#!/usr/bin/env python3
"""
Test script pour vérifier l'utilisation GPU avec chaque moteur OCR
"""

import sys
import os
import time
import subprocess
import threading
from pathlib import Path

def monitor_gpu(duration=10):
    """Surveille l'utilisation GPU pendant une durée donnée."""
    gpu_usage = []

    def monitor():
        start_time = time.time()
        while time.time() - start_time < duration:
            try:
                result = subprocess.run(
                    ['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
                    capture_output=True, text=True, timeout=2
                )
                if result.returncode == 0:
                    usage = int(result.stdout.strip())
                    gpu_usage.append(usage)
                    print(f"GPU: {usage}%", end='\r')
                time.sleep(0.5)
            except:
                break

    thread = threading.Thread(target=monitor)
    thread.start()
    return gpu_usage, thread

def test_ocr_engine(engine_name, cmd_args):
    """Test un moteur OCR et surveille l'utilisation GPU."""
    print(f"\n{'='*50}")
    print(f"Test {engine_name}")
    print(f"{'='*50}")

    # Démarrer la surveillance GPU
    gpu_usage, monitor_thread = monitor_gpu(duration=15)

    try:
        # Exécuter la commande OCR
        result = subprocess.run(cmd_args, capture_output=True, text=True, timeout=30)

        # Attendre que la surveillance se termine
        monitor_thread.join(timeout=2)

        print(f"\nRésultat {engine_name}:")
        if result.returncode == 0:
            # Afficher seulement les premières lignes de sortie
            lines = result.stdout.split('\n')[:10]
            for line in lines:
                if line.strip():
                    print(f"  {line}")
            print("✅ Test réussi")
        else:
            print(f"❌ Erreur: {result.stderr[:200]}")

        # Analyser l'utilisation GPU
        if gpu_usage:
            max_usage = max(gpu_usage)
            avg_usage = sum(gpu_usage) / len(gpu_usage)
            print(f"GPU avg: {avg_usage:.1f}%")
            print(f"GPU max: {max_usage}%")
        else:
            print("⚠️  Aucune donnée GPU collectée")

    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout pour {engine_name}")
        monitor_thread.join(timeout=2)
    except Exception as e:
        print(f"❌ Exception: {e}")
        monitor_thread.join(timeout=2)

def main():
    """Test tous les moteurs OCR."""
    script_dir = Path(__file__).parent
    image_path = script_dir / "test_images" / "books1.jpg"

    if not image_path.exists():
        print(f"❌ Image de test introuvable: {image_path}")
        return

    print(f"Image de test: {image_path}")
    print("Test de l'utilisation GPU avec chaque moteur OCR...")

    # Test EasyOCR
    test_ocr_engine(
        "EasyOCR",
        [sys.executable, str(script_dir / "scripts" / "ocr_detect.py"),
         str(image_path), "--gpu", "--easyocr"]
    )

    # Test Tesseract
    test_ocr_engine(
        "Tesseract",
        [sys.executable, str(script_dir / "scripts" / "ocr_detect.py"),
         str(image_path), "--gpu", "--tesseract"]
    )

    # Test TrOCR
    test_ocr_engine(
        "TrOCR",
        [sys.executable, str(script_dir / "scripts" / "ocr_detect.py"),
         str(image_path), "--gpu", "--trocr"]
    )

    print(f"\n{'='*50}")
    print("Résumé:")
    print("- EasyOCR: Utilise le GPU pour l'inférence")
    print("- Tesseract: N'utilise pas le GPU (pas supporté)")
    print("- TrOCR: Utilise le GPU pour les transformers")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()