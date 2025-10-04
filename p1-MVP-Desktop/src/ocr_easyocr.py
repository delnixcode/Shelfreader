"""
ShelfReader - EasyOCR Processor with Spine Detection
Module spécialisé pour la détection OCR avec EasyOCR et détection de tranches.
Basé sur l'algorithme de "shelfie" pour la détection des lignes de tranches.

AMÉLIORATIONS RÉCENTES:
- ✅ GPU support avec PyTorch CUDA
- ✅ Détection de tranches basée sur l'algorithme shelfie
- ✅ Regroupement intelligent par proximité et lignes de tranches
- ✅ Validation de similarité avec titres de référence
- ✅ Gestion d'erreurs robuste et fallback automatique
- ✅ Consolidation de tous les fichiers OCR en une seule version optimisée

UTILISATION:
    python src/ocr_easyocr.py test_images/books1.jpg --gpu --validate
"""

# === IMPORTS ===
import cv2
import numpy as np
import scipy.ndimage
import scipy.stats

class Line(object):
    """Classe représentant une ligne détectée (bord de tranche de livre)."""

    def __init__(self, slope, intercept, center, min_x, max_x, min_y, max_y):
        self.m = slope  # pente
        self.b = intercept  # ordonnée à l'origine
        self.center = center  # centre de la ligne
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.vertical_threshold = 1000  # seuil pour considérer une ligne comme verticale

    def x(self, y):
        """Retourne la coordonnée x de la ligne à la position y."""
        # Ligne verticale
        if self.m > self.vertical_threshold:
            return self.center[0]
        # Ligne normale
        else:
            return (y - self.b) / self.m

class EasyOCRProcessor:
    """Processeur OCR spécialisé pour EasyOCR avec détection de tranches."""

    def __init__(self, languages, confidence_threshold, use_gpu=False):
        """Initialise EasyOCR."""
        try:
            import easyocr
            import cv2
            import numpy as np
            from PIL import Image
        except ImportError as e:
            raise ImportError(f"EasyOCR nécessite des dépendances manquantes: {e}")

        self.confidence_threshold = confidence_threshold
        self.reader = easyocr.Reader(languages, gpu=use_gpu)
        device = "GPU" if use_gpu else "CPU"
        print(f"🔍 EasyOCR initialisé - Langues: {languages}, Seuil: {confidence_threshold}, Device: {device}")

    # === PRÉTRAITEMENT ===
    def _preprocess_image(self, image):
        """Prétraitement agressivement optimisé pour EasyOCR."""
        import cv2

        # Convertir en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Améliorer drastiquement le contraste avec CLAHE
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(6,6))
        enhanced = clahe.apply(gray)

        # Réduction du bruit avec filtre bilatéral (préserve les bords)
        denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)

        # Améliorer la netteté avec unsharp masking
        gaussian = cv2.GaussianBlur(denoised, (0, 0), 1.0)
        sharpened = cv2.addWeighted(denoised, 1.5, gaussian, -0.5, 0)

        # Binarisation adaptative plus agressive
        binary = cv2.adaptiveThreshold(
            sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 3
        )

        # Dilatation légère pour connecter les caractères
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        dilated = cv2.dilate(binary, kernel, iterations=1)

        # Reconvertir en BGR pour EasyOCR
        processed = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)

        return processed

    # === DÉTECTION OCR ===
    def detect_text(self, pil_image, preprocess=True):
        """Détecte le texte avec EasyOCR."""
        import numpy as np
        import cv2

        image_array = np.array(pil_image)
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Prétraitement si demandé
        if preprocess:
            bgr_image = self._preprocess_image(bgr_image)

        # Détection OCR avec paramètres optimisés pour texte vertical
        results = self.reader.readtext(
            bgr_image,
            rotation_info=[0, 90, 180, 270],
            width_ths=0.3,      # Tolérance largeur
            height_ths=0.3,     # Tolérance hauteur
            contrast_ths=0.05,  # Seuil contraste très bas
            adjust_contrast=0.7, # Ajustement contraste
            text_threshold=0.5, # Seuil texte
            link_threshold=0.3  # Seuil liaison
        )

        # Filtrage par confiance et longueur
        filtered_results = [
            r for r in results
            if r[2] >= self.confidence_threshold and len(r[1].strip()) >= 2
        ]

        return filtered_results

    # === DÉTECTION DES TRANCHES (ALGORITHME SHELFIE) ===
    def _gaussian_blur(self, img, sigma, debug=False):
        """Applique un flou gaussien."""
        proc_img = scipy.ndimage.gaussian_filter(img, sigma)
        if debug:
            print('Gaussian blur')
            cv2.imshow('Gaussian Blur', proc_img.astype(np.uint8))
            cv2.waitKey(0)
        return proc_img

    def _downsample(self, img, num_downsamples, debug=False):
        """Réduit la résolution de l'image."""
        proc_img = img.copy()
        for i in range(num_downsamples):
            height, width = proc_img.shape[:2]
            if height < 4 or width < 4:
                break  # Ne pas descendre en dessous d'une taille minimale
            new_width = max(1, width // 2)
            new_height = max(1, height // 2)
            proc_img = cv2.resize(proc_img, (new_width, new_height))
        if debug:
            print(f'Downsampled {min(num_downsamples, i+1)} times (final size: {proc_img.shape})')
            cv2.imshow('Downsampled', proc_img.astype(np.uint8))
            cv2.waitKey(0)
        return proc_img

    def _sobel_x_squared(self, img, debug=False):
        """Applique le filtre Sobel horizontal au carré."""
        sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        proc_img = sobel_x ** 2
        if debug:
            print('Sobel X squared')
            cv2.imshow('Sobel X Squared', (proc_img / proc_img.max() * 255).astype(np.uint8))
            cv2.waitKey(0)
        return proc_img

    def _standardize(self, img, debug=False):
        """Standardise l'image (moyenne 0, écart-type 1)."""
        if img.std() > 0:
            proc_img = (img - img.mean()) / img.std()
        else:
            proc_img = img - img.mean()
        if debug:
            print('Standardized')
            cv2.imshow('Standardized', ((proc_img - proc_img.min()) / (proc_img.max() - proc_img.min()) * 255).astype(np.uint8))
            cv2.waitKey(0)
        return proc_img

    def _binarize(self, img, cutoff=None, debug=False):
        """Binarise l'image."""
        if cutoff is None:
            cutoff = img.max() / 100.0
        proc_img = (img > cutoff).astype(np.uint8) * 255
        if debug:
            print(f'Binarized with cutoff {cutoff}')
            cv2.imshow('Binarized', proc_img)
            cv2.waitKey(0)
        return proc_img

    def _vertical_erode(self, img, structure_length, iterations, debug=False):
        """Applique une érosion verticale."""
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, structure_length))
        proc_img = cv2.erode(img, kernel, iterations=iterations)
        if debug:
            print(f'Vertical erode: length={structure_length}, iterations={iterations}')
            cv2.imshow('Vertical Erode', proc_img)
            cv2.waitKey(0)
        return proc_img

    def _vertical_dilate(self, img, structure_length, iterations, debug=False):
        """Applique une dilatation verticale."""
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, structure_length))
        proc_img = cv2.dilate(img, kernel, iterations=iterations)
        if debug:
            print(f'Vertical dilate: length={structure_length}, iterations={iterations}')
            cv2.imshow('Vertical Dilate', proc_img)
            cv2.waitKey(0)
        return proc_img

    def _connected_components(self, img, debug=False):
        """Trouve les composants connectés."""
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)
        if debug:
            print(f'Connected components: {num_labels} found')
            # Créer une image colorée pour visualiser les composants
            colored = cv2.applyColorMap((labels * 255 / num_labels).astype(np.uint8), cv2.COLORMAP_JET)
            cv2.imshow('Connected Components', colored)
            cv2.waitKey(0)
        return labels, list(range(1, num_labels))  # levels exclut le fond (0)

    def _upsample(self, img, factor, debug=False):
        """Remonte la résolution de l'image."""
        height, width = img.shape[:2]
        new_width = int(width * factor)
        new_height = int(height * factor)

        if debug:
            print(f"Upsampling: {width}x{height} -> {new_width}x{new_height} (factor: {factor})")

        # Vérifier que les dimensions sont valides
        if new_width <= 0 or new_height <= 0:
            print(f"❌ Dimensions invalides pour upsampling: {new_width}x{new_height}")
            return img

        try:
            # Convertir en float32 pour le resize si nécessaire
            if img.dtype != np.uint8 and img.dtype != np.float32:
                img = img.astype(np.float32)
            proc_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
        except cv2.error as e:
            print(f"❌ Erreur OpenCV lors de l'upsampling: {e}")
            print(f"   Dimensions originales: {img.shape}, dtype: {img.dtype}")
            print(f"   Dimensions cibles: {new_width}x{new_height}")
            return img

        if debug:
            print(f'Upsampled by factor {factor}')
            cv2.imshow('Upsampled', proc_img.astype(np.uint8))
            cv2.waitKey(0)
        return proc_img

    def _get_lines_from_img(self, img, levels, debug=False):
        """Extrait les lignes des composants connectés."""
        lines = []
        for level in levels:
            line_mask = (img == level)
            ys, xs = np.where(line_mask)

            if len(xs) == 0 or len(ys) == 0:
                continue

            center = [np.mean(xs), np.mean(ys)]
            min_x, max_x = np.min(xs), np.max(xs)
            min_y, max_y = np.min(ys), np.max(ys)

            # Calculer le spread pour déterminer si c'est une ligne verticale
            spread = (max_y - min_y) / (max_x - min_x) if (max_x - min_x) > 0 else 1000

            # Ligne verticale
            if spread > 10:
                line = Line(1000, 0, center, min_x, max_x, min_y, max_y)
            else:
                # Ligne normale - régression linéaire
                slope, intercept, r, p, std = scipy.stats.linregress(xs, ys)
                line = Line(slope, intercept, center, min_x, max_x, min_y, max_y)

            lines.append(line)

        # Trier par position x centrale
        lines.sort(key=lambda line: line.center[0])

        if debug:
            print(f'Extracted {len(lines)} lines')
            # Visualiser les lignes - convertir en uint8 pour OpenCV
            if len(img.shape) == 2:
                vis_img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_GRAY2BGR)
            else:
                vis_img = img.astype(np.uint8).copy()
            for line in lines:
                y0, y1 = 0, img.shape[0]
                x0 = int(line.x(y0))
                x1 = int(line.x(y1))
                cv2.line(vis_img, (x0, y0), (x1, y1), (0, 255, 0), 2)
            cv2.imshow('Extracted Lines', vis_img)
            cv2.waitKey(0)

        return lines

    def _detect_spine_lines(self, image, debug=False):
        """Détecte les lignes de tranches de livres dans l'image (algorithme shelfie)."""
        try:
            # Convertir en niveaux de gris
            proc_img = np.mean(image, axis=2).astype(np.uint8)

            # Downsampling pour réduire le bruit (moins agressif)
            num_downsamples = 2  # Réduit de 2 au lieu de 3
            proc_img = self._downsample(proc_img, num_downsamples, debug=debug)

            # Flou gaussien
            sigma = 3
            proc_img = self._gaussian_blur(proc_img, sigma, debug=debug)

            # Détection de bords horizontaux (Sobel X)
            proc_img = self._sobel_x_squared(proc_img, debug=debug)

            # Standardisation
            proc_img = self._standardize(proc_img, debug=debug)

            # Binarisation
            cutoff = proc_img.max() / 100.0
            proc_img = self._binarize(proc_img, cutoff, debug=debug)

            # Érosion verticale pour connecter les lignes (plus précise)
            structure_length = 50  # Réduit de 100 à 50
            iterations = 1  # Réduit de 2 à 1
            proc_img = self._vertical_erode(proc_img, structure_length, iterations, debug=debug)

            # Dilatation verticale pour renforcer (plus précise)
            structure_length = 100  # Réduit de 200 à 100
            iterations = 50  # Réduit de 100 à 50
            proc_img = self._vertical_dilate(proc_img, structure_length, iterations, debug=debug)

            # Composants connectés
            proc_img, levels = self._connected_components(proc_img, debug=debug)

            # Remonter à la résolution originale
            upsample_factor = 2 ** num_downsamples
            proc_img = self._upsample(proc_img, upsample_factor, debug=debug)

            # Extraire les lignes
            lines = self._get_lines_from_img(proc_img, levels, debug=debug)

            return lines

        except Exception as e:
            if debug:
                print(f"❌ Erreur dans la détection de tranches: {e}")
                import traceback
                traceback.print_exc()
            return []

    def _group_texts_by_spine_lines(self, boxes, image, debug=False):
        """Regroupe les textes par lignes de tranches détectées (approche shelfie)."""
        if not boxes:
            return boxes

        # Détecter les lignes de tranches
        spine_lines = self._detect_spine_lines(image, debug=debug)

        if not spine_lines:
            print("⚠️ Aucune ligne de tranche détectée, utilisation du regroupement par proximité")
            return self._group_by_proximity(boxes)

        # Trier les lignes par position x
        spine_lines.sort(key=lambda line: line.center[0])

        # Créer des blocs entre les lignes
        blocks = [[] for _ in range(len(spine_lines) + 1)]

        for box in boxes:
            box_center_x = box['x'] + box['width'] / 2

            # Trouver dans quel bloc mettre cette boîte
            assigned = False
            for i in range(len(spine_lines) + 1):
                if i == 0:
                    # Premier bloc : à gauche de la première ligne
                    if box_center_x < spine_lines[0].center[0]:
                        blocks[i].append(box)
                        assigned = True
                        break
                elif i == len(spine_lines):
                    # Dernier bloc : à droite de la dernière ligne
                    if box_center_x >= spine_lines[-1].center[0]:
                        blocks[i].append(box)
                        assigned = True
                        break
                else:
                    # Bloc entre deux lignes
                    if spine_lines[i-1].center[0] <= box_center_x < spine_lines[i].center[0]:
                        blocks[i].append(box)
                        assigned = True
                        break

            if not assigned:
                # Par défaut, mettre dans le dernier bloc
                blocks[-1].append(box)

        # Combiner les textes dans chaque bloc
        grouped_boxes = []
        for block in blocks:
            if not block:
                continue

            if len(block) == 1:
                grouped_boxes.append(block[0])
            else:
                # Trier par position verticale (haut en bas)
                block.sort(key=lambda b: b['y'])

                # Combiner les textes
                combined_text = ' '.join([b['text'] for b in block])

                # Calculer la boîte englobante
                min_x = min([b['x'] for b in block])
                max_x = max([b['x'] + b['width'] for b in block])
                min_y = min([b['y'] for b in block])
                max_y = max([b['y'] + b['height'] for b in block])

                # Confiance moyenne
                avg_confidence = sum([b['confidence'] for b in block]) / len(block)

                combined_box = {
                    "text": combined_text,
                    "x": min_x, "y": min_y,
                    "width": max_x - min_x,
                    "height": max_y - min_y,
                    "font_size": max([b['height'] for b in block]),
                    "is_vertical": any([b['is_vertical'] for b in block]),
                    "confidence": avg_confidence
                }

                grouped_boxes.append(combined_box)

        if debug:
            print(f"🔍 Regroupement par lignes: {len(spine_lines)} lignes détectées, {len(grouped_boxes)} groupes créés")

        return grouped_boxes

    def _group_by_proximity(self, boxes):
        """Regroupement par proximité horizontale (méthode de secours)."""
        if not boxes:
            return boxes

        # Trier par x croissant
        boxes.sort(key=lambda b: b['x'])

        grouped_boxes = []
        current_group = [boxes[0]]
        group_x_threshold = 50  # pixels de tolérance horizontale

        for box in boxes[1:]:
            # Si la différence x est petite, ajouter au groupe
            if abs(box['x'] - current_group[-1]['x']) < group_x_threshold:
                current_group.append(box)
            else:
                # Nouveau groupe
                grouped_boxes.append(current_group)
                current_group = [box]

        # Ajouter le dernier groupe
        grouped_boxes.append(current_group)

        # Combiner les textes dans chaque groupe
        final_boxes = []
        for group in grouped_boxes:
            if len(group) == 1:
                final_boxes.append(group[0])
            else:
                # Trier par y et combiner
                group.sort(key=lambda b: b['y'])
                combined_text = ' '.join([b['text'] for b in group])
                combined_box = group[0].copy()
                combined_box['text'] = combined_text
                combined_box['width'] = max([b['x'] + b['width'] for b in group]) - min([b['x'] for b in group])
                combined_box['height'] = max([b['y'] + b['height'] for b in group]) - min([b['y'] for b in group])
                combined_box['confidence'] = sum([b['confidence'] for b in group]) / len(group)
                final_boxes.append(combined_box)

        return final_boxes

    def _validate_book_similarity(self, book_texts, reference_titles=None):
        """Valide la similarité des textes de livres avec des titres de référence (approche shelfie)."""
        if not book_texts or not reference_titles:
            return book_texts

        validated_books = []

        for book_text in book_texts:
            best_match = None
            best_score = 0.0

            # Nettoyer le texte détecté
            detected_text = book_text['text'].strip().upper()

            for ref_title in reference_titles:
                ref_clean = ref_title.strip().upper()

                # Calculer similarité simple (Jaccard-like)
                detected_words = set(detected_text.split())
                ref_words = set(ref_clean.split())

                if not detected_words or not ref_words:
                    continue

                intersection = detected_words.intersection(ref_words)
                union = detected_words.union(ref_words)

                similarity = len(intersection) / len(union) if union else 0.0

                if similarity > best_score:
                    best_score = similarity
                    best_match = ref_title

            # Si similarité suffisante (> 0.3), utiliser le titre de référence
            if best_score > 0.3 and best_match:
                book_text = book_text.copy()
                book_text['original_text'] = book_text['text']
                book_text['text'] = best_match
                book_text['similarity_score'] = best_score

            validated_books.append(book_text)

        return validated_books
    def get_text_and_confidence(self, pil_image, preprocess=True, use_spine_detection=True, reference_titles=None):
        """Extrait le texte et la confiance moyenne."""
        boxes = self.get_boxes(pil_image, preprocess=preprocess, use_spine_detection=use_spine_detection, reference_titles=reference_titles)

        texts = [b['text'] for b in boxes]
        confidences = [b['confidence'] for b in boxes]

        full_text = ' | '.join(texts)  # Séparer par | pour les livres
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return full_text, avg_confidence

    def get_boxes(self, pil_image, preprocess=True, vertical_only=False, use_spine_detection=True, debug=False, reference_titles=None):
        """Extrait les boîtes de texte avec coordonnées, groupées par livre."""
        import numpy as np
        import cv2

        results = self.detect_text(pil_image, preprocess=preprocess)

        boxes = []
        for bbox, text, confidence in results:
            # Calcul des dimensions
            x = min([p[0] for p in bbox])
            y = min([p[1] for p in bbox])
            width = max([p[0] for p in bbox]) - x
            height = max([p[1] for p in bbox]) - y
            font_size = height

            # Détection verticale
            is_vertical = height > width * 1.5

            if vertical_only and not is_vertical:
                continue

            boxes.append({
                "text": text,
                "x": x, "y": y,
                "width": width, "height": height,
                "font_size": font_size,
                "is_vertical": is_vertical,
                "confidence": confidence
            })

        # Regrouper les boîtes par livre
        if boxes and use_spine_detection:
            # Convertir l'image PIL en numpy array pour la détection de lignes
            image_array = np.array(pil_image)
            bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

            # Utiliser le regroupement par lignes de tranches
            boxes = self._group_texts_by_spine_lines(boxes, bgr_image, debug=debug)
        elif boxes:
            # Méthode de secours par proximité
            boxes = self._group_by_proximity(boxes)

        # Validation de similarité si des titres de référence sont fournis
        if boxes and reference_titles:
            boxes = self._validate_book_similarity(boxes, reference_titles)

        return boxes

# === SCRIPT PRINCIPAL ===
if __name__ == "__main__":
    """
    Point d'entrée pour tester EasyOCR avec détection de tranches.
    Usage: python ocr_easyocr_new.py <image_path> [--gpu] [--debug]
    """
    import sys
    import argparse
    from PIL import Image

    parser = argparse.ArgumentParser(description='Test EasyOCR avec détection de tranches')
    parser.add_argument('image_path', help='Chemin vers l\'image à analyser')
    parser.add_argument('--gpu', action='store_true', help='Utiliser le GPU')
    parser.add_argument('--confidence', type=float, default=0.1, help='Seuil de confiance (défaut: 0.1)')
    parser.add_argument('--debug', action='store_true', help='Mode debug pour visualiser les étapes')
    parser.add_argument('--no-spine', action='store_true', help='Désactiver la détection de tranches')
    parser.add_argument('--validate', action='store_true', help='Activer la validation de similarité avec les vrais titres')
    parser.add_argument('--output', type=str, help='Préfixe des fichiers de sortie')

    args = parser.parse_args()

    try:
        # Initialisation
        processor = EasyOCRProcessor(['en'], args.confidence, args.gpu)

        # Chargement de l'image
        pil_image = Image.open(args.image_path)

        # Titres de référence pour validation (liste des vrais titres de l'image books1.jpg)
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
        ] if args.validate else None

        # Traitement
        use_spine_detection = not args.no_spine
        boxes = processor.get_boxes(pil_image, preprocess=False, use_spine_detection=use_spine_detection, debug=args.debug, reference_titles=reference_titles)
        text, confidence = processor.get_text_and_confidence(pil_image, preprocess=False, use_spine_detection=use_spine_detection, reference_titles=reference_titles)

        # Résultats
        print(f"🔍 EasyOCR avec détection de tranches - Image: {args.image_path}")
        print(f"📊 Résultats: {len(boxes)} livres détectés")
        print(f"🎯 Confiance moyenne: {confidence:.3f}")
        print(f"🔧 Détection de tranches: {'Activée' if use_spine_detection else 'Désactivée'}")
        print(f"✅ Validation de similarité: {'Activée' if args.validate else 'Désactivée'}")
        print(f"📝 Texte complet: {text}")

        # Sauvegarder dans un fichier unique qui se remplace
        output_file = args.output if args.output else 'result-ocr/easyocr_spine_results.txt'
        if not output_file.startswith('result-ocr/'):
            output_file = f'result-ocr/{output_file}'

        # Créer le dossier s'il n'existe pas
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"=== RÉSULTATS OCR AVEC DÉTECTION DE TRANCHES - {args.image_path} ===\n")
            f.write(f"Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Nombre de livres détectés: {len(boxes)}\n")
            f.write(f"Confiance moyenne: {confidence:.3f}\n")
            f.write(f"Détection de tranches: {'Activée' if use_spine_detection else 'Désactivée'}\n")
            f.write(f"Validation de similarité: {'Activée' if args.validate else 'Désactivée'}\n\n")
            f.write(f"TEXTE COMPLET:\n{text}\n\n")

            if boxes:
                f.write("DÉTAIL PAR LIVRE:\n")
                for i, box in enumerate(boxes, 1):
                    f.write(f"\n--- Livre {i} ---\n")
                    f.write(f"Confiance: {box['confidence']:.3f}\n")
                    f.write(f"Texte: {box['text']}\n")
                    f.write(f"Position: ({box['x']:.1f}, {box['y']:.1f})\n")
                    f.write(f"Dimensions: {box['width']:.1f} x {box['height']:.1f}\n")

        print(f"💾 Résultats sauvegardés dans {output_file}")

        if boxes:
            print("\n📚 Livres détectés:")
            for i, box in enumerate(boxes, 1):
                print(f"  {i:2d}. {box['text']}")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)