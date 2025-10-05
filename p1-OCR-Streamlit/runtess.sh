#!/bin/bash
# Script de lancement pour Tesseract Engine

echo "🚀 Lancement de ShelfReader - Tesseract Engine"
echo "============================================="

# Chemin vers l'environnement virtuel
ENV_PATH="env-p1/bin/activate"

# Vérifier si l'environnement virtuel existe
if [ -f "$ENV_PATH" ]; then
    echo "🔧 Activation de l'environnement virtuel..."
    source "$ENV_PATH"
else
    echo "⚠️  Environnement virtuel non trouvé"
fi

# Lancement de Tesseract avec paramètres par défaut
echo "📚 Démarrage de Tesseract..."
echo "   Paramètres: --confidence 0.5 --psm 6"
echo ""

python src/engines/tesseract/main.py "$@" --confidence 0.5 --psm 6