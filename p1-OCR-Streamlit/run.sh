#!/bin/bash
# Script de lancement pour ShelfReader P1

echo "🚀 Lancement de ShelfReader P1 - OCR Adaptatif"
echo "=============================================="

# Chemin vers l'environnement virtuel (à adapter selon votre setup)
ENV_PATH="env-p1/bin/activate"

# Vérifier si l'environnement virtuel existe
if [ -f "$ENV_PATH" ]; then
    echo "🔧 Activation de l'environnement virtuel..."
    source "$ENV_PATH"
else
    echo "⚠️  Environnement virtuel non trouvé à $ENV_PATH"
    echo "   Lancement sans environnement virtuel..."
fi

# Lancement de Streamlit
echo "📚 Démarrage de l'application..."
echo "   URL locale: http://localhost:8501"
echo "   URL réseau: http://$(hostname -I | awk '{print $1}'):8501"
echo "   Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

streamlit run src/frontend/main.py --server.headless true --server.port 8501