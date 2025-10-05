# DÉPENDANCES:
#   - Utilise: Aucun (fichier de constantes)
#   - Importe: Aucun
#   - Utilisé par: orchestrator.py, __init__.py

"""
ShelfReader - Tesseract Configuration
Constantes et paramètres de configuration pour Tesseract.
"""

# Paramètres de prétraitement
CLAHE_CLIP_LIMIT = 2.0
CLAHE_TILE_GRID_SIZE = (8, 8)
BILATERAL_D = 5
BILATERAL_SIGMA_COLOR = 50
BILATERAL_SIGMA_SPACE = 50

# Configurations PSM (Page Segmentation Mode)
PSM_CONFIGS = [
    '--psm 6',  # Texte uniforme - le plus rapide et efficace
]

# Paramètres de filtrage
MAX_RESULTS = 15
MIN_TEXT_LENGTH = 2