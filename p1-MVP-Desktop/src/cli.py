#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI pour ShelfReader P1 - Interface en ligne de commande
Compatible avec tous les OS, comme npm scripts
"""

import os
import sys
import subprocess
import platform
import argparse

def get_python_executable():
    """Trouve l'exécutable Python de l'environnement virtuel"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(script_dir))

    if platform.system() == "Windows":
        python_exe = os.path.join(project_dir, "env-p1", "Scripts", "python.exe")
    else:
        python_exe = os.path.join(project_dir, "env-p1", "bin", "python")

    if os.path.exists(python_exe):
        return python_exe
    else:
        # Fallback vers python système
        return sys.executable

def run_ocr_script(script_path, args):
    """Exécute un script OCR avec les arguments donnés"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(script_dir))

    # Changer vers le répertoire du projet
    os.chdir(project_dir)

    python_exe = get_python_executable()
    cmd = [python_exe, script_path] + args

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Erreur: Python ou script OCR introuvable")
        sys.exit(1)

def main_easyocr():
    """Commande: easyocr [options] [image]"""
    parser = argparse.ArgumentParser(description="EasyOCR - OCR avec GPU/CPU support")
    parser.add_argument("image_pos", nargs="?", default="test_images/books1.jpg",
                       help="Chemin vers l'image (défaut: test_images/books1.jpg)")
    parser.add_argument("--image", "-i", help="Chemin vers l'image (remplace l'argument positionnel)")
    parser.add_argument("--gpu", action="store_true", help="Utiliser le GPU")
    parser.add_argument("--confidence", type=float, default=0.2,
                       help="Seuil de confiance (0.0-1.0, défaut: 0.2)")
    parser.add_argument("--output", help="Nom du fichier de sortie")

    args = parser.parse_args()

    # Utiliser --image si spécifié, sinon l'argument positionnel
    image = args.image if args.image is not None else args.image_pos

    script_args = [image]
    if args.gpu:
        script_args.append("--gpu")
    if args.confidence != 0.2:
        script_args.extend(["--confidence", str(args.confidence)])
    if args.output:
        script_args.extend(["--output", args.output])

    run_ocr_script("src/ocr_easyocr.py", script_args)

def main_tesseract():
    """Commande: tesseract [options] [image]"""
    parser = argparse.ArgumentParser(description="Tesseract - OCR rapide CPU")
    parser.add_argument("image_pos", nargs="?", default="test_images/books1.jpg",
                       help="Chemin vers l'image (défaut: test_images/books1.jpg)")
    parser.add_argument("--image", "-i", help="Chemin vers l'image (remplace l'argument positionnel)")
    parser.add_argument("--lang", default="eng", help="Langue (défaut: eng)")
    parser.add_argument("--confidence", type=float, default=0.2,
                       help="Seuil de confiance (0.0-1.0, défaut: 0.2)")
    parser.add_argument("--output", help="Nom du fichier de sortie")

    args = parser.parse_args()

    # Utiliser --image si spécifié, sinon l'argument positionnel
    image = args.image if args.image is not None else args.image_pos

    script_args = [image]
    if args.lang != "eng":
        script_args.extend(["--lang", args.lang])
    if args.confidence != 0.2:
        script_args.extend(["--confidence", str(args.confidence)])
    if args.output:
        script_args.extend(["--output", args.output])

    run_ocr_script("src/ocr_tesseract.py", script_args)

def main_trocr():
    """Commande: trocr [options] [image]"""
    parser = argparse.ArgumentParser(description="TrOCR - OCR haute précision")
    parser.add_argument("image_pos", nargs="?", default="test_images/books1.jpg",
                       help="Chemin vers l'image (défaut: test_images/books1.jpg)")
    parser.add_argument("--image", "-i", help="Chemin vers l'image (remplace l'argument positionnel)")
    parser.add_argument("--gpu", action="store_true", help="Utiliser le GPU")
    parser.add_argument("--confidence", type=float, default=0.2,
                       help="Seuil de confiance (0.0-1.0, défaut: 0.2)")
    parser.add_argument("--output", help="Nom du fichier de sortie")

    args = parser.parse_args()

    # Utiliser --image si spécifié, sinon l'argument positionnel
    image = args.image if args.image is not None else args.image_pos

    script_args = [image]
    if args.gpu:
        script_args.append("--gpu")
    if args.confidence != 0.2:
        script_args.extend(["--confidence", str(args.confidence)])
    if args.output:
        script_args.extend(["--output", args.output])

    run_ocr_script("src/ocr_trocr.py", script_args)

def main():
    """Commande principale: shelfreader <commande> [options]"""
    parser = argparse.ArgumentParser(
        description="ShelfReader P1 - CLI OCR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  shelfreader easyocr --gpu                    # EasyOCR avec GPU
  shelfreader tesseract --lang fra             # Tesseract français
  shelfreader trocr --gpu --confidence 0.5     # TrOCR haute précision

Ou utilisez directement:
  easyocr --gpu
  tesseract
  trocr --gpu --confidence 0.5
        """
    )
    parser.add_argument("command", choices=["easyocr", "tesseract", "trocr"],
                       help="Commande OCR à exécuter")
    parser.add_argument("args", nargs=argparse.REMAINDER,
                       help="Arguments pour la commande OCR")

    args = parser.parse_args()

    # Rediriger vers la bonne fonction
    if args.command == "easyocr":
        # Recréer les arguments pour main_easyocr
        sys.argv = ["easyocr"] + args.args
        main_easyocr()
    elif args.command == "tesseract":
        sys.argv = ["tesseract"] + args.args
        main_tesseract()
    elif args.command == "trocr":
        sys.argv = ["trocr"] + args.args
        main_trocr()

if __name__ == "__main__":
    main()