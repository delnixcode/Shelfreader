"""
ShelfReader - EasyOCR Spine Detection
Module de détection des lignes de séparation entre livres (tranches).
"""

import cv2
import numpy as np
import scipy.ndimage
import scipy.stats
from ..models.line import Line
from ..config import (
    DOWNSAMPLE_FACTOR, GAUSSIAN_BLUR_SIGMA, BINARIZE_CUTOFF_FACTOR,
    VERTICAL_ERODE_LENGTH, VERTICAL_ERODE_ITERATIONS,
    VERTICAL_DILATE_LENGTH, VERTICAL_DILATE_ITERATIONS,
    SHORT_CLUSTER_THRESHOLD_FRACTION, CANNY_MIN, CANNY_MAX,
    ICCC_PIXEL_THRESHOLD_RATIO, ICCC_DILATE_WIDTH, ICCC_DILATE_HEIGHT,
    ICCC_MIN_HEIGHT_RATIO
)


class EasyOCRSpineDetection:
    """Algorithmes de détection des lignes de tranches de livres."""

    @staticmethod
    def gaussian_blur(img, sigma, debug=False):
        """Applique un flou gaussien."""
        proc_img = scipy.ndimage.gaussian_filter(img, sigma)
        if debug:
            print('Gaussian blur')
            cv2.imshow('Gaussian Blur', proc_img.astype(np.uint8))
            cv2.waitKey(0)
        return proc_img

    @staticmethod
    def downsample(img, num_downsamples, debug=False):
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

    @staticmethod
    def sobel_x_squared(img, debug=False):
        """Applique le filtre Sobel horizontal au carré."""
        sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        proc_img = sobel_x ** 2
        if debug:
            print('Sobel X squared')
            cv2.imshow('Sobel X Squared', (proc_img / proc_img.max() * 255).astype(np.uint8))
            cv2.waitKey(0)
        return proc_img

    @staticmethod
    def standardize(img, debug=False):
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

    @staticmethod
    def binarize(img, cutoff=None, debug=False):
        """Binarise l'image."""
        if cutoff is None:
            cutoff = img.max() / BINARIZE_CUTOFF_FACTOR
        proc_img = (img > cutoff).astype(np.uint8) * 255
        if debug:
            print(f'Binarized with cutoff {cutoff}')
            cv2.imshow('Binarized', proc_img)
            cv2.waitKey(0)
        return proc_img

    @staticmethod
    def vertical_erode(img, structure_length=VERTICAL_ERODE_LENGTH,
                      iterations=VERTICAL_ERODE_ITERATIONS, debug=False):
        """Applique une érosion verticale."""
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, structure_length))
        proc_img = cv2.erode(img, kernel, iterations=iterations)
        if debug:
            print(f'Vertical erode: length={structure_length}, iterations={iterations}')
            cv2.imshow('Vertical Erode', proc_img)
            cv2.waitKey(0)
        return proc_img

    @staticmethod
    def vertical_dilate(img, structure_length=VERTICAL_DILATE_LENGTH,
                       iterations=VERTICAL_DILATE_ITERATIONS, debug=False):
        """Applique une dilatation verticale."""
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, structure_length))
        proc_img = cv2.dilate(img, kernel, iterations=iterations)
        if debug:
            print(f'Vertical dilate: length={structure_length}, iterations={iterations}')
            cv2.imshow('Vertical Dilate', proc_img)
            cv2.waitKey(0)
        return proc_img

    @staticmethod
    def remove_short_vertical_clusters(img, levels, threshold_fraction=SHORT_CLUSTER_THRESHOLD_FRACTION, debug=False):
        """Supprime les lignes verticales trop courtes (bruit)."""
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

    @staticmethod
    def connected_components(img, debug=False):
        """Trouve les composants connectés."""
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)
        if debug:
            print(f'Connected components: {num_labels} found')
            # Créer une image colorée pour visualiser les composants
            colored = cv2.applyColorMap((labels * 255 / num_labels).astype(np.uint8), cv2.COLORMAP_JET)
            cv2.imshow('Connected Components', colored)
            cv2.waitKey(0)
        return labels, list(range(1, num_labels))  # levels exclut le fond (0)

    @staticmethod
    def upsample(img, factor, debug=False):
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

    @staticmethod
    def get_lines_from_img(img, levels, debug=False):
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

    @classmethod
    def detect_shelf_rows_iccc2013(cls, image, debug=False):
        """Détecte les rangées d'étagères selon l'approche ICCC 2013."""
        try:
            # Convertir en niveaux de gris et appliquer Canny
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()

            # Canny edge detection
            edges = cv2.Canny(gray, CANNY_MIN, CANNY_MAX, apertureSize=3)

            if debug:
                cv2.imshow('Canny Edges', edges)
                cv2.waitKey(0)

            height, width = edges.shape
            horizontal_lines = np.zeros_like(edges)

            # Balayage avec ligne imaginaire horizontale
            for y in range(0, height, 2):  # Pas de 2 pixels pour optimisation
                # Compter les pixels sous la ligne horizontale complète
                line_pixels = edges[y, :]  # Toute la ligne horizontale
                pixel_count = np.sum(line_pixels > 0)

                # Seuil: 50% des pixels de la ligne doivent être des bords
                threshold = int(width * ICCC_PIXEL_THRESHOLD_RATIO)

                if pixel_count >= threshold:
                    # Ligne sélectionnée - l'activer complètement
                    horizontal_lines[y, :] = 255

            if debug:
                cv2.imshow('Selected Horizontal Lines', horizontal_lines)
                cv2.waitKey(0)

            # Extension des lignes sélectionnées (morphological dilation)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (width//10, ICCC_DILATE_HEIGHT))
            extended_lines = cv2.dilate(horizontal_lines, kernel, iterations=1)

            if debug:
                cv2.imshow('Extended Lines', extended_lines)
                cv2.waitKey(0)

            # Connected Component Analysis pour extraire les régions
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(extended_lines, connectivity=8)

            # Filtrer les régions par hauteur
            min_height_threshold = height * ICCC_MIN_HEIGHT_RATIO
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

            # Convertir les régions en "lignes" pour compatibilité
            spine_lines = []
            for x, y, w, h in valid_regions:
                center_y = y + h // 2
                # Créer une ligne horizontale fictive
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
            return []

    @classmethod
    def detect_spine_lines_shelfie(cls, image, debug=False):
        """Détection de lignes de séparation - ALGORITHME SHELFIE AMÉLIORÉ."""
        try:
            # Convertir en niveaux de gris
            if len(image.shape) == 3:
                proc_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float64)
            else:
                proc_img = image.astype(np.float64)

            if debug:
                print(f"📸 Image originale: {image.shape}")

            # 1. Downsampling
            proc_img = cls.downsample(proc_img, DOWNSAMPLE_FACTOR, debug=debug)

            # 2. Gaussian blur
            proc_img = cls.gaussian_blur(proc_img, GAUSSIAN_BLUR_SIGMA, debug=debug)

            # 3. Sobel X squared
            proc_img = cls.sobel_x_squared(proc_img, debug=debug)

            # 4. Standardization
            proc_img = cls.standardize(proc_img, debug=debug)

            # 5. Binarization
            cutoff = proc_img.max() / BINARIZE_CUTOFF_FACTOR
            proc_img = cls.binarize(proc_img, cutoff=cutoff, debug=debug)

            # 6. Erode subtract
            structure = np.array(([0,0,0],[1,1,1],[0,0,0]), dtype=np.uint8) * 5
            eroded = cv2.erode(proc_img, structure, iterations=1)
            proc_img = proc_img - eroded
            proc_img[proc_img < 0] = 255  # Inverser les négatifs

            if debug:
                print('Erode subtract')
                cv2.imshow('Erode Subtract', proc_img)
                cv2.waitKey(0)

            # 7. Vertical erode
            proc_img = cls.vertical_erode(proc_img, debug=debug)

            # 8. Connected components
            proc_img_labels, levels = cls.connected_components(proc_img, debug=debug)

            if debug:
                print(f"🔍 Composants trouvés après erosion: {len(levels)}")

            # 9. Supprimer les très courts clusters
            proc_img_labels = cls.remove_short_vertical_clusters(proc_img_labels, levels, debug=debug)

            # 10. Re-binarize
            proc_img = (proc_img_labels > 0).astype(np.uint8) * 255

            # 11. Petite dilation verticale
            proc_img = cls.vertical_dilate(proc_img, debug=debug)

            # 12. Re-binarize
            proc_img = (proc_img > 0).astype(np.uint8) * 255

            # 13. Upsampling
            upsample_factor = 2 ** DOWNSAMPLE_FACTOR
            proc_img = cls.upsample(proc_img, upsample_factor, debug=debug)

            # 14. Connected components final
            proc_img, levels = cls.connected_components(proc_img, debug=debug)

            # 15. Extraire les lignes
            lines = cls.get_lines_from_img(proc_img, levels, debug=debug)

            if debug:
                print(f"✅ Méthode Shelfie améliorée: {len(lines)} lignes verticales détectées")
                # Visualiser les lignes détectées
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

    @classmethod
    def detect_spine_lines(cls, image, debug=False, method="shelfie"):
        """Détecte les lignes de tranches selon différentes méthodes."""
        if method == "shelfie":
            return cls.detect_spine_lines_shelfie(image, debug)
        else:  # iccc2013
            return cls.detect_shelf_rows_iccc2013(image, debug)