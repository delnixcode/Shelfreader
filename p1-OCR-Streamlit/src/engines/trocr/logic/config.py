# DÉPENDANCES:
#   - Utilise: Aucun (fichier de constantes)
#   - Importe: Aucun
#   - Utilisé par: orchestrator.py, __init__.py

"""
ShelfReader - TrOCR Configuration
Constantes et paramètres de configuration pour TrOCR.
"""

# Paramètres de génération
MAX_LENGTH = 100
NUM_BEAMS = 6
EARLY_STOPPING = True
NO_REPEAT_NGRAM_SIZE = 2
LENGTH_PENALTY = 1.5
REPETITION_PENALTY = 1.2

# Paramètres de segmentation
NUM_STRIPS = 14  # Nombre de bandes verticales

# Modèle
MODEL_NAME = 'microsoft/trocr-base-handwritten'