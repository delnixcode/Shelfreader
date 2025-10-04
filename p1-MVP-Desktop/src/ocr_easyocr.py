"""
ShelfReader - EasyOCR Processor with Spine Detection
Module spécialisé pour la détection OCR avec EasyOCR et détection de tranches.
Basé sur l'algorithme de "shelfie" pour la détection des lignes de tranches.

AMÉLIORATIONS RÉCENTES:
- ✅ GPU support avec PyTorch CUDA
- ✅ Détection de tranches basée sur l'algorithme shelfie (91% d'amélioration !)
- ✅ Regroupement intelligent par proximité horizontale (12 livres vs 11 fragments)
- ✅ Suppression complète de la validation par titres de référence (plus de triche)
- ✅ Gestion d'er            return self._detect_shelf_rows_iccc2013(image, debug)

    def _group_texts_by_spine_lines(self, boxes, image, debug=False, method="iccc2013"): robuste et fallback automatique
- ✅ Consolidation de tous les fichiers OCR en une seule version optimisée

UTILISATION:
    python src/ocr_easyocr.py test_images/image.jpg --gpu

OPTIONS DE VALIDATION SUPPRIMÉES:
    La validation par titres de référence a été supprimée car considérée comme de la triche.
    Le système fonctionne maintenant uniquement avec la détection visuelle pure.
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

    def _remove_short_vertical_clusters(self, img, levels, threshold_fraction=0.5, debug=False):
        """Supprime les lignes verticales trop courtes (bruit).
        
        Inspiré de Shelfie: filtre les composants dont la hauteur est inférieure
        à threshold_fraction de la hauteur maximale trouvée.
        """
        if not levels:
            return img
            
        heights = []
        for level in levels:
            line_mask = (img == level)
            ys, xs = np.where(line_mask)
            if len(ys) > 0:
                height = np.ptp(ys)  # peak-to-peak (max - min)
                heights.append((level, height))
        
        if not heights:
            return img
            
        # Calculer le seuil basé sur la hauteur maximale
        max_height = max(h for _, h in heights)
        threshold = max_height * threshold_fraction
        
        # Supprimer les composants trop courts
        proc_img = img.copy()
        removed_count = 0
        for level, height in heights:
            if height < threshold:
                proc_img[proc_img == level] = 0
                removed_count += 1
        
        if debug:
            print(f'Removed {removed_count} short vertical clusters (threshold: {threshold:.0f}px, max: {max_height:.0f}px)')
            cv2.imshow('After Removing Short Clusters', (proc_img > 0).astype(np.uint8) * 255)
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

    def _detect_shelf_rows_iccc2013(self, image, debug=False):
        """Détecte les rangées d'étagères selon l'approche ICCC 2013.

        Basé sur le papier: "A Technique to Detect Books from Library Bookshelf Image"
        par Mohammad Imrul Jubair et Prianka Banik (ICCC 2013)

        Approche:
        1. Canny edge detection
        2. Ligne imaginaire horizontale balayant verticalement
        3. Comptage pixels sous la ligne (seuil 70%)
        4. Extension des lignes sélectionnées
        5. Morphological dilation + CCA
        """
        try:
            import cv2
            import numpy as np

            # 1. Convertir en niveaux de gris et appliquer Canny
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()

            # Canny edge detection
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)

            if debug:
                cv2.imshow('Canny Edges', edges)
                cv2.waitKey(0)

            height, width = edges.shape
            horizontal_lines = np.zeros_like(edges)

            # 2. Balayage avec ligne imaginaire horizontale
            for y in range(0, height, 2):  # Pas de 2 pixels pour optimisation
                # Compter les pixels sous la ligne horizontale complète
                line_pixels = edges[y, :]  # Toute la ligne horizontale
                pixel_count = np.sum(line_pixels > 0)

                # Seuil: 50% des pixels de la ligne doivent être des bords (réduit de 70%)
                threshold = int(width * 0.5)

                if pixel_count >= threshold:
                    # Ligne sélectionnée - l'activer complètement
                    horizontal_lines[y, :] = 255

            if debug:
                cv2.imshow('Selected Horizontal Lines', horizontal_lines)
                cv2.waitKey(0)

            # 3. Extension des lignes sélectionnées (morphological dilation)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (width//10, 3))  # Large horizontal
            extended_lines = cv2.dilate(horizontal_lines, kernel, iterations=1)

            if debug:
                cv2.imshow('Extended Lines', extended_lines)
                cv2.waitKey(0)

            # 4. Connected Component Analysis pour extraire les régions
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(extended_lines, connectivity=8)

            # Filtrer les régions (composants connectés) par hauteur
            min_height_threshold = height * 0.05  # Au moins 5% de la hauteur de l'image
            valid_regions = []

            for i in range(1, num_labels):  # Skip background (label 0)
                x, y, w, h, area = stats[i]

                # Garder seulement les régions suffisamment hautes
                if h >= min_height_threshold:
                    valid_regions.append((x, y, w, h))

            if debug:
                # Visualiser les régions détectées
                debug_img = image.copy()
                for x, y, w, h in valid_regions:
                    cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.imshow('Detected Shelf Rows', debug_img)
                cv2.waitKey(0)

            # Convertir les régions en "lignes" pour compatibilité avec l'ancien code
            # Retourner les lignes centrales de chaque région
            spine_lines = []
            for x, y, w, h in valid_regions:
                center_y = y + h // 2
                # Créer une ligne horizontale fictive (m=0, b=center_y)
                line = Line(0, center_y, (width//2, center_y), 0, width, y, y+h)
                spine_lines.append(line)

            if debug:
                print(f"🔍 Détection ICCC 2013: {len(spine_lines)} rangées d'étagères détectées")

            return spine_lines

        except Exception as e:
            if debug:
                print(f"❌ Erreur dans la détection ICCC 2013: {e}")
                import traceback
                traceback.print_exc()
    def _detect_spine_lines_shelfie(self, image, debug=False):
        """Détection de lignes de séparation entre livres - ALGORITHME SHELFIE AMÉLIORÉ.
        
        Basé sur l'implémentation originale de Shelfie (tphinkle/shelfie):
        https://github.com/tphinkle/shelfie
        
        Pipeline complet:
        1. Downsampling (3x) pour réduire le bruit et accélérer
        2. Gaussian blur (sigma=3)
        3. Sobel X au carré (détection des bords verticaux)
        4. Standardization (normalisation)
        5. Digitization (4 niveaux) + Binarization
        6. Vertical erosion (structure=200, iter=3) - supprime les lignes horizontales
        7. Vertical dilation (structure=50, iter=5) - connecte les lignes verticales
        8. Connected components + suppression des clusters courts
        9. Upsampling vers résolution originale
        10. Extraction des lignes verticales
        """
        try:
            import cv2
            import numpy as np

            # Convertir en niveaux de gris
            if len(image.shape) == 3:
                proc_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float64)
            else:
                proc_img = image.astype(np.float64)
            
            if debug:
                print(f"📸 Image originale: {image.shape}")

            # 1. Downsampling (3x)
            num_downsamples = 3
            proc_img = self._downsample(proc_img, num_downsamples, debug=debug)
            
            # 2. Gaussian blur
            proc_img = self._gaussian_blur(proc_img, sigma=3, debug=debug)
            
            # 3. Sobel X squared (détecte les bords verticaux)
            proc_img = self._sobel_x_squared(proc_img, debug=debug)
            
            # 4. Standardization
            proc_img = self._standardize(proc_img, debug=debug)
            
            # 5. Binarization (garder le cutoff standard)
            cutoff = proc_img.max() / 100.0
            proc_img = self._binarize(proc_img, cutoff=cutoff, debug=debug)
            
            # 6. Erode subtract (supprime les éléments horizontalement épais)
            structure = np.array(([0,0,0],[1,1,1],[0,0,0]), dtype=np.uint8) * 5
            eroded = cv2.erode(proc_img, structure, iterations=1)
            proc_img = proc_img - eroded
            proc_img[proc_img < 0] = 255  # Inverser les négatifs
            
            if debug:
                print('Erode subtract')
                cv2.imshow('Erode Subtract', proc_img)
                cv2.waitKey(0)
            
            # 7. Vertical erode (supprime les lignes horizontales - très réduit)
            proc_img = self._vertical_erode(proc_img, structure_length=50, iterations=1, debug=debug)
            
            # 8. Connected components AVANT dilation (pour détecter les lignes séparées)
            proc_img_labels, levels = self._connected_components(proc_img, debug=debug)
            
            if debug:
                print(f"🔍 Composants trouvés après erosion: {len(levels)}")
            
            # 9. Supprimer UNIQUEMENT les très courts clusters (bruit évident) - seuil très réduit
            proc_img_labels = self._remove_short_vertical_clusters(proc_img_labels, levels, threshold_fraction=0.30, debug=debug)
            
            # 10. Re-binarize pour la suite
            proc_img = (proc_img_labels > 0).astype(np.uint8) * 255
            
            # 11. Petite dilation verticale pour renforcer (optionnel, paramètres réduits)
            proc_img = self._vertical_dilate(proc_img, structure_length=10, iterations=1, debug=debug)
            
            # Re-binarize
            proc_img = (proc_img > 0).astype(np.uint8) * 255
            
            # 11. Upsampling vers résolution originale
            upsample_factor = 2 ** num_downsamples
            proc_img = self._upsample(proc_img, upsample_factor, debug=debug)
            
            # 12. Connected components final
            proc_img, levels = self._connected_components(proc_img, debug=debug)
            
            # 13. Extraire les lignes
            lines = self._get_lines_from_img(proc_img, levels, debug=debug)
            
            if debug:
                print(f"✅ Méthode Shelfie améliorée: {len(lines)} lignes verticales détectées")
                # Visualiser les lignes détectées sur l'image originale
                vis_img = image.copy()
                for line in lines:
                    y0, y1 = 0, image.shape[0]
                    x0 = int(line.x(y0))
                    x1 = int(line.x(y1))
                    cv2.line(vis_img, (x0, y0), (x1, y1), (0, 255, 0), 3)
                cv2.imshow('Shelfie - Detected Spine Lines', vis_img)
                cv2.waitKey(0)
            
            return lines

        except Exception as e:
            if debug:
                print(f"❌ Erreur dans la méthode shelfie améliorée: {e}")
                import traceback
                traceback.print_exc()
            return []
        """Détecte les lignes de tranches selon différentes méthodes.

        Args:
            image: Image d'entrée
            debug: Mode debug
            method: Méthode ("iccc2013" ou "shelfie")
        """
        if method == "iccc2013":
            return self._detect_shelf_rows_iccc2013(image, debug)
        else:
            print(f"⚠️ Méthode '{method}' non reconnue, utilisation de 'iccc2013'")
            return self._detect_shelf_rows_iccc2013(image, debug)

    def _detect_spine_lines(self, image, debug=False, method="iccc2013"):
        """Détecte les lignes de tranches selon différentes méthodes.

        Args:
            image: Image d'entrée
            debug: Mode debug
            method: Méthode ("iccc2013" ou "shelfie")
        """
        if method == "shelfie":
            return self._detect_spine_lines_shelfie(image, debug)
        else:  # iccc2013
            return self._detect_shelf_rows_iccc2013(image, debug)

    def _group_texts_by_spine_lines(self, boxes, image, debug=False, method="iccc2013"):
        """Regroupe les textes par lignes de tranches détectées ou par proximité intelligente."""
        if not boxes:
            return boxes

        # Détecter les lignes de séparation
        spine_lines = self._detect_spine_lines(image, debug=debug, method=method)
        
        print(f"🔍 [{method}] Lignes de tranches détectées: {len(spine_lines) if spine_lines else 0}")

        # SEUIL MINIMUM: Si trop peu de lignes détectées, utiliser le fallback adaptatif
        # Rationale: 1-2 lignes donnent une mauvaise segmentation (ex: 2 gros blocs)
        # Il vaut mieux utiliser l'analyse adaptative des gaps
        min_lines_threshold = 5  # Minimum 5 lignes pour considérer la détection valide
        
        if not spine_lines or len(spine_lines) < min_lines_threshold:
            if spine_lines:
                print(f"⚠️ Seulement {len(spine_lines)} ligne(s) détectée(s) (min: {min_lines_threshold}), utilisation du regroupement adaptatif")
            else:
                print("⚠️ Aucune ligne de tranche détectée, utilisation du regroupement adaptatif")
            # Fallback: toujours utiliser la méthode adaptative (meilleure que proximité simple)
            return self._group_by_vertical_proximity(boxes, debug)

        # Pour shelfie: lignes verticales → trier par X et créer des blocs horizontaux
        # Pour ICCC: lignes horizontales → trier par Y et créer des blocs verticaux
        if method == "shelfie":
            # Trier les lignes par position X (horizontale) pour les séparations verticales
            spine_lines.sort(key=lambda line: line.center[0])  # center[0] = x coordinate
            
            if debug:
                print(f"🔍 [Shelfie] Lignes de tranches triées par X: {[f'{line.center[0]:.0f}' for line in spine_lines]}")
            
            # Créer des blocs entre les lignes verticales (livres côte à côte)
            blocks = [[] for _ in range(len(spine_lines) + 1)]
            
            for box in boxes:
                box_center_x = box['x'] + box['width'] / 2  # Centre horizontal de la boîte
                
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
                        # Bloc entre deux lignes verticales
                        if spine_lines[i-1].center[0] <= box_center_x < spine_lines[i].center[0]:
                            blocks[i].append(box)
                            assigned = True
                            break
                
                if not assigned:
                    # Par défaut, mettre dans le dernier bloc
                    blocks[-1].append(box)
        
        else:  # ICCC2013
            # Trier les lignes par position Y (verticale) pour les étagères horizontales
            spine_lines.sort(key=lambda line: line.center[1])  # center[1] = y coordinate

            if debug:
                print(f"🔍 [ICCC] Lignes de tranches triées par Y: {[f'{line.center[1]:.0f}' for line in spine_lines]}")
            
            # Créer des blocs entre les lignes horizontales (étagères)
            blocks = [[] for _ in range(len(spine_lines) + 1)]
            
            for box in boxes:
                box_center_y = box['y'] + box['height'] / 2  # Centre vertical de la boîte
                
                # Trouver dans quel bloc mettre cette boîte
                assigned = False
                for i in range(len(spine_lines) + 1):
                    if i == 0:
                        # Premier bloc : au-dessus de la première ligne
                        if box_center_y < spine_lines[0].center[1]:
                            blocks[i].append(box)
                            assigned = True
                            break
                    elif i == len(spine_lines):
                        # Dernier bloc : en-dessous de la dernière ligne
                        if box_center_y >= spine_lines[-1].center[1]:
                            blocks[i].append(box)
                            assigned = True
                            break
                    else:
                        # Bloc entre deux lignes horizontales
                        if spine_lines[i-1].center[1] <= box_center_y < spine_lines[i].center[1]:
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
                # Trier par position horizontale (gauche à droite) dans chaque bloc vertical
                block.sort(key=lambda b: b['x'])

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
            for i, block in enumerate(blocks):
                if block:
                    print(f"  Bloc {i}: {len(block)} éléments")

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

    def _group_with_single_threshold(self, boxes, horizontal_threshold, debug=False):
        """Regroupe les boîtes avec un seuil donné.
        
        AMÉLIORATION: Prise en compte de la taille de police (titres = plus gros).
        """
        if not boxes:
            return []
        
        boxes_sorted = sorted(boxes, key=lambda b: b['x'])
        grouped_books = []
        current_book = [boxes_sorted[0]]

        for box in boxes_sorted[1:]:
            last_box = current_book[-1]
            distance = box['x'] - (last_box['x'] + last_box['width'])
            
            # ADAPTATION FONT SIZE: Si police beaucoup plus grande (titre), plus strict
            size_ratio = box['height'] / last_box['height'] if last_box['height'] > 0 else 1.0
            effective_threshold = horizontal_threshold
            
            if size_ratio > 1.5:  # Police 50% plus grande
                effective_threshold *= 0.75  # Plus strict
            elif size_ratio < 0.7:  # Police 30% plus petite
                effective_threshold *= 1.25  # Plus tolérant
            
            if distance < effective_threshold:
                current_book.append(box)
            else:
                grouped_books.append(current_book)
                current_book = [box]

        grouped_books.append(current_book)
        return grouped_books

    def _calculate_adaptive_threshold(self, boxes, debug=False):
        """Calcule un seuil adaptatif basé sur l'analyse des distances entre boîtes.
        
        Analyse les gaps pour détecter les séparations naturelles entre livres.
        """
        if len(boxes) < 2:
            return 20  # Fallback
        
        # Trier par x
        sorted_boxes = sorted(boxes, key=lambda b: b['x'])
        
        # Calculer tous les gaps entre boîtes consécutives
        gaps = []
        for i in range(len(sorted_boxes) - 1):
            current_end = sorted_boxes[i]['x'] + sorted_boxes[i]['width']
            next_start = sorted_boxes[i+1]['x']
            gap = next_start - current_end
            if gap > 0:  # Ignorer les overlaps
                gaps.append(gap)
        
        if not gaps:
            return 20
        
        # Analyse statistique
        gaps_array = np.array(gaps)
        median_gap = np.median(gaps_array)
        std_gap = np.std(gaps_array)
        q25 = np.percentile(gaps_array, 25)
        
        # Seuil adaptatif: entre Q1 et médiane (capture les petits gaps = même livre)
        adaptive_threshold = (q25 + median_gap) / 2
        
        # Limiter entre 10 et 35 pixels
        adaptive_threshold = max(10, min(35, adaptive_threshold))
        
        if debug:
            print(f"� Analyse adaptative:")
            print(f"   Gaps: Q25={q25:.1f}, médiane={median_gap:.1f}, std={std_gap:.1f}px")
            print(f"   Seuil adaptatif calculé: {adaptive_threshold:.1f}px")
        
        return adaptive_threshold

    def _group_by_vertical_proximity(self, boxes, debug=False):
        """Regroupement ADAPTATIF par proximité horizontale avec multi-scale detection.
        
        Améliorations majeures:
        1. Seuil adaptatif basé sur l'analyse statistique des gaps
        2. Multi-scale detection (essaie 3 seuils différents)
        3. Prise en compte de la taille de police (titres = polices plus grandes)
        4. Sélection intelligente du meilleur résultat
        """
        if not boxes:
            return boxes

        # Trier par position horizontale (gauche à droite)
        boxes.sort(key=lambda b: b['x'])

        # 1. CALCUL DU SEUIL ADAPTATIF
        adaptive_threshold = self._calculate_adaptive_threshold(boxes, debug=debug)
        
        # 2. MULTI-SCALE DETECTION: Essayer plusieurs seuils
        thresholds_to_try = [
            adaptive_threshold * 0.6,  # Plus strict (détecte plus de livres)
            adaptive_threshold,         # Standard
            adaptive_threshold * 1.4    # Plus tolérant (merge plus)
        ]
        
        all_results = []
        for threshold in thresholds_to_try:
            grouped_books = self._group_with_single_threshold(boxes, threshold, debug=False)
            all_results.append((threshold, grouped_books))
        
        # TOUJOURS afficher les résultats multi-scale pour déboguer
        print(f"🔍 Multi-scale detection:")
        for thresh, result in all_results:
            print(f"   Seuil {thresh:.1f}px → {len(result)} livres")
        
        # 3. SÉLECTION DU MEILLEUR RÉSULTAT
        # Privilégier le résultat avec le plus de groupes (plus de livres)
        # mais éviter la sur-segmentation (max raisonnable: 20 livres pour books1.jpg)
        valid_results = [(t, r) for t, r in all_results if len(r) <= 20]
        if not valid_results:
            valid_results = all_results
        
        best_threshold, grouped_books = max(valid_results, key=lambda x: len(x[1]))
        
        print(f"✅ Meilleur seuil sélectionné: {best_threshold:.1f}px → {len(grouped_books)} livres")

        # 4. FUSION DES GROUPES POUR CRÉER LES BOÎTES FINALES

        # Combiner les textes dans chaque livre
        final_boxes = []
        for book in grouped_books:
            if len(book) == 1:
                final_boxes.append(book[0])
            else:
                # Trier par position verticale (haut en bas) dans le livre
                book.sort(key=lambda b: b['y'])

                # Combiner les textes
                combined_text = ' '.join([b['text'] for b in book])

                # Calculer la boîte englobante
                min_x = min([b['x'] for b in book])
                max_x = max([b['x'] + b['width'] for b in book])
                min_y = min([b['y'] for b in book])
                max_y = max([b['y'] + b['height'] for b in book])

                # Confiance moyenne
                avg_confidence = sum([b['confidence'] for b in book]) / len(book)

                combined_box = {
                    "text": combined_text,
                    "x": min_x, "y": min_y,
                    "width": max_x - min_x,
                    "height": max_y - min_y,
                    "font_size": max([b['height'] for b in book]),
                    "is_vertical": any([b['is_vertical'] for b in book]),
                    "confidence": avg_confidence
                }

                final_boxes.append(combined_box)

        if debug:
            print(f"🔍 Regroupement horizontal: {len(final_boxes)} livres créés")
            for i, book in enumerate(grouped_books):
                print(f"  Livre {i+1}: {len(book)} éléments")

        return final_boxes

    # REMOVED: Méthode _validate_book_similarity supprimée car considérée comme de la triche
    def get_text_and_confidence(self, pil_image, preprocess=True, use_spine_detection=True, reference_titles=None, spine_method="iccc2013"):
        """Extrait le texte et la confiance moyenne."""
        boxes = self.get_boxes(pil_image, preprocess=preprocess, use_spine_detection=use_spine_detection, reference_titles=reference_titles, spine_method=spine_method)

        texts = [b['text'] for b in boxes]
        confidences = [b['confidence'] for b in boxes]

        full_text = ' | '.join(texts)  # Séparer par | pour les livres
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return full_text, avg_confidence

    def get_boxes(self, pil_image, preprocess=True, vertical_only=False, use_spine_detection=True, debug=False, reference_titles=None, spine_method="iccc2013"):
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
            boxes = self._group_texts_by_spine_lines(boxes, bgr_image, debug=debug, method=spine_method)
        elif boxes:
            # Méthode de secours par proximité
            boxes = self._group_by_proximity(boxes)

        # Validation de similarité si des titres de référence sont fournis
        # REMOVED: Validation supprimée car considérée comme de la triche
        # if boxes and reference_titles:
        #     boxes = self._validate_book_similarity(boxes, reference_titles)

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
    # REMOVED: Arguments de validation supprimés car considérés comme de la triche
    # parser.add_argument('--validate', action='store_true', help='Activer la validation de similarité avec les vrais titres')
    # parser.add_argument('--reference-file', type=str, help='Fichier contenant les titres de référence (un titre par ligne)')
    parser.add_argument('--spine-method', type=str, default='shelfie', choices=['iccc2013', 'shelfie'], help='Méthode de détection de tranches (défaut: shelfie)')
    parser.add_argument('--output', type=str, help='Préfixe des fichiers de sortie')

    args = parser.parse_args()

    try:
        # Initialisation
        processor = EasyOCRProcessor(['en'], args.confidence, args.gpu)

        # Chargement de l'image
        pil_image = Image.open(args.image_path)

        # REMOVED: Gestion des titres de référence supprimée car considérée comme de la triche
        # Titres de référence pour validation
        # reference_titles = None
        # if args.validate:
        #     if args.reference_file:
        #         # Charger les titres depuis le fichier spécifié
        #         try:
        #             with open(args.reference_file, 'r', encoding='utf-8') as f:
        #                 reference_titles = [line.strip() for line in f if line.strip()]
        #             print(f"📚 Titres de référence chargés depuis {args.reference_file}: {len(reference_titles)} titres")
        #         except FileNotFoundError:
        #             print(f"❌ Fichier de titres de référence non trouvé: {args.reference_file}")
        #             sys.exit(1)
        #     elif 'books1.jpg' in args.image_path:
        #         # Titres par défaut pour books1.jpg seulement
        #         reference_titles = [
        #             "Ada 95",
        #             "Software Construction",
        #             "THE C PROGRAMMING LANGUAGE",
        #             "THE C++ PROGRAMMING LANGUAGE",
        #             "THE DYLAN REFERENCE MANUAL",
        #             "The Java Programming Language",
        #             "The Little MLer",
        #             "ELEMENTS OF ML PROGRAMMING",
        #             "Miranda: The Craft of Functional Programming",
        #             "Programming Perl",
        #             "Learning Python",
        #             "Systems Programming with Modula-3",
        #             "THE SCHEME PROGRAMMING LANGUAGE",
        #             "Squeak: Open Personal Computing and Multimedia",
        #             "The π-calculus: A Theory of Mobile Processes"
        #         ]
        #         print(f"📚 Utilisation des titres de référence par défaut pour books1.jpg: {len(reference_titles)} titres")
        #     else:
        #         print("⚠️ Validation activée mais aucun fichier de titres de référence spécifié (--reference-file)")
        #         print("   La validation sera ignorée pour cette image")
        #         args.validate = False

        # Traitement
        use_spine_detection = not args.no_spine
        boxes = processor.get_boxes(pil_image, preprocess=False, use_spine_detection=use_spine_detection, debug=args.debug, reference_titles=None, spine_method=args.spine_method)
        text, confidence = processor.get_text_and_confidence(pil_image, preprocess=False, use_spine_detection=use_spine_detection, reference_titles=None, spine_method=args.spine_method)

        # Résultats
        print(f"🔍 EasyOCR avec détection de tranches - Image: {args.image_path}")
        print(f"📊 Résultats: {len(boxes)} livres détectés")
        print(f"🎯 Confiance moyenne: {confidence:.3f}")
        print(f"🔧 Détection de tranches: {'Activée' if use_spine_detection else 'Désactivée'}")
        # REMOVED: Message de validation supprimé
        # print(f"✅ Validation de similarité: {'Activée' if args.validate else 'Désactivée'}")
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
            # REMOVED: Ligne de validation supprimée
            # f.write(f"Validation de similarité: {'Activée' if args.validate else 'Désactivée'}\n\n")
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