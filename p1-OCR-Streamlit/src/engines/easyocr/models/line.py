# DÉPENDANCES:
#   - Utilise: Aucun (structure de données simple)
#   - Importe: Aucun
#   - Utilisé par: detection/spine_detection.py, __init__.py

"""
ShelfReader - EasyOCR Line Model
Classe représentant une ligne détectée dans l'image.
"""

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