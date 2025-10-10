#!/bin/bash
# Script simple pour activer l'environnement virtuel env-p1

# Activer l'environnement virtuel
. env-p1/bin/activate

# Afficher confirmation
echo "✅ Environnement virtuel env-p1 activé"
echo "� Python: $(which python)"
echo "💡 Tapez 'deactivate' pour quitter"