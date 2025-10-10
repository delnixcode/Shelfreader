#!/bin/bash
# Script de lancement pour EasyOCR Engine

echo "🚀 Lancement de ShelfReader - EasyOCR Engine"
echo "==========================================="

# Chemin vers l'environnement virtuel
ENV_PATH="env-p1/bin/activate"

# Vérifier si l'environnement virtuel existe
if [ -f "$ENV_PATH" ]; then
    echo "🔧 Activation de l'environnement virtuel..."
    source "$ENV_PATH"
else
    echo "⚠️  Environnement virtuel non trouvé"
fi

# Lancement d'EasyOCR avec paramètres par défaut
echo "📚 Démarrage d'EasyOCR..."
echo "   Paramètres: --gpu --confidence 0.1 --spine-method vertical_lines"
echo ""

python src/engines/easyocr/main.py "$@" --gpu --confidence 0.1 --spine-method vertical_lines