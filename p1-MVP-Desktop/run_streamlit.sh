#!/bin/bash
# Script de lancement de l'application Streamlit ShelfReader P1

echo "📚 ShelfReader P1 - Application Web"
echo "=================================="

# Vérifier si on est dans le bon répertoire
if [ ! -f "src/app.py" ]; then
    echo "❌ Erreur: Ce script doit être exécuté depuis la racine du projet P1"
    echo "   Utilisation: cd p1-MVP-Desktop && ./run_streamlit.sh"
    exit 1
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source env-p1/bin/activate

# Vérifier que streamlit est installé
if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit n'est pas installé. Installation en cours..."
    pip install streamlit pandas numpy
fi

echo "🚀 Démarrage de l'application Streamlit..."
echo "   URL: http://localhost:8501"
echo "   Pour arrêter: Ctrl+C"
echo ""

# Lancer l'application
streamlit run src/app.py --server.headless true --server.port 8501