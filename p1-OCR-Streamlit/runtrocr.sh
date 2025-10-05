#!/bin/bash
# Script de lancement pour TrOCR Engine

echo "🚀 Lancement de ShelfReader - TrOCR Engine"
echo "========================================="

# Chemin vers l'environnement virtuel
ENV_PATH="env-p1/bin/activate"

# Vérifier si l'environnement virtuel existe
if [ -f "$ENV_PATH" ]; then
    echo "🔧 Activation de l'environnement virtuel..."
    source "$ENV_PATH"
else
    echo "⚠️  Environnement virtuel non trouvé"
fi

# Lancement de TrOCR avec paramètres par défaut
echo "📚 Démarrage de TrOCR..."
echo "   Paramètres: --gpu --device auto"
echo ""

python src/engines/trocr/main.py "$@" --gpu --device auto