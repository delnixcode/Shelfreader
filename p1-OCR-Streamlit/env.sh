#!/bin/bash
# Script pour activer l'environnement virtuel env-p1 de ShelfReader P1

echo "🐍 Activation de l'environnement virtuel Python 3.12 pour ShelfReader P1"
echo "=================================================================="

# Chemin vers l'environnement virtuel
ENV_PATH="env-p1/bin/activate"

# Vérifier si l'environnement virtuel existe
if [ -f "$ENV_PATH" ]; then
    echo "✅ Environnement virtuel trouvé : $ENV_PATH"
    echo "🔧 Activation en cours..."

    # Activer l'environnement virtuel
    source "$ENV_PATH"

    # Vérifier que l'activation a fonctionné
    if [ "$VIRTUAL_ENV" != "" ]; then
        echo "✅ Environnement virtuel activé avec succès !"
        echo "📍 Python path : $(which python)"
        echo "📍 Python version : $(python --version)"
        echo "📍 Environnement : $VIRTUAL_ENV"
        echo ""
        echo "💡 Commandes disponibles :"
        echo "   • streamlit run src/frontend/main.py    # Lancer l'interface web"
        echo "   • python src/engines/easyocr/main.py    # Test EasyOCR"
        echo "   • python src/engines/tesseract/main.py  # Test Tesseract"
        echo "   • python src/engines/trocr/main.py      # Test TrOCR"
        echo "   • deactivate                            # Désactiver l'environnement"
        echo ""
        echo "🚀 Prêt à travailler sur ShelfReader P1 !"
        echo ""

        # Si des arguments sont passés, les exécuter
        if [ $# -gt 0 ]; then
            echo "▶️  Exécution de la commande : $@"
            exec "$@"
        else
            # Sinon, lancer un shell interactif
            echo "💻 Lancement d'un shell interactif dans l'environnement virtuel..."
            echo "   Tapez 'exit' ou Ctrl+D pour quitter"
            exec bash --rcfile <(echo "PS1='\[\e[32m\](env-p1) \[\e[34m\]\w\[\e[0m\] $ '")
        fi
    else
        echo "❌ Échec de l'activation de l'environnement virtuel"
        exit 1
    fi
else
    echo "❌ Environnement virtuel non trouvé à : $ENV_PATH"
    echo ""
    echo "💡 Pour créer l'environnement virtuel :"
    echo "   python3.12 -m venv env-p1"
    echo ""
    echo "💡 Pour installer les dépendances :"
    echo "   source env-p1/bin/activate && pip install -r requirements.txt"
    exit 1
fi