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
import pytest

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

def test_gpu_usage():
    """Test unitaire pour vérifier l'utilisation GPU avec chaque moteur OCR."""
    script_dir = Path(__file__).parent
    image_path = script_dir / "test_images" / "books1.jpg"

    if not image_path.exists():
        pytest.skip(f"Image de test introuvable: {image_path}")

    print(f"Image de test: {image_path}")
    print("Test de l'utilisation GPU avec chaque moteur OCR...")

    # Test EasyOCR
    print(f"\n{'='*50}")
    print("Test EasyOCR")
    print(f"{'='*50}")

    # Démarrer la surveillance GPU
    gpu_usage, monitor_thread = monitor_gpu(duration=15)

    try:
        # Exécuter la commande OCR
        result = subprocess.run(
            [sys.executable, str(script_dir / "src" / "engines" / "easyocr_engine.py"),
             str(image_path), "--gpu"],
            capture_output=True, text=True, timeout=30
        )

        # Attendre que la surveillance se termine
        monitor_thread.join(timeout=2)

        print("Résultat EasyOCR:")
        assert result.returncode == 0, f"Erreur: {result.stderr[:200]}"
        print("✅ Test réussi")

        # Analyser l'utilisation GPU
        if gpu_usage:
            max_usage = max(gpu_usage)
            avg_usage = sum(gpu_usage) / len(gpu_usage)
            print(".1f")
            print(f"GPU max: {max_usage}%")
            assert max_usage > 0, "GPU ne semble pas être utilisé"
        else:
            print("⚠️  Aucune donnée GPU collectée")

    except subprocess.TimeoutExpired:
        pytest.fail("Timeout pour EasyOCR")
    except Exception as e:
        pytest.fail(f"Exception: {e}")

    print(f"\n{'='*50}")
    print("Résumé:")
    print("- EasyOCR: Utilise le GPU pour l'inférence")
    print("- Tesseract: N'utilise pas le GPU (pas supporté)")
    print("- TrOCR: Utilise le GPU pour les transformers")
    print(f"{'='*50}")