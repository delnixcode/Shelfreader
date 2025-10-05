"""
Composant Sidebar - ShelfReader P1

Ce module contient la logique d'affichage de la sidebar de navigation
et des informations générales sur l'application.
"""

import streamlit as st
from typing import Literal


def render_sidebar() -> Literal["Analysis", "comparaison"]:
    """
    Affiche la sidebar de navigation et retourne la page sélectionnée.

    La sidebar contient :
    - Navigation entre les pages principales
    - Informations sur l'algorithme et les performances
    - Paramètres recommandés

    Returns:
        Literal["Analysis", "comparaison"]: Page sélectionnée par l'utilisateur
    """
    with st.sidebar:
        # Navigation principale (radio en haut, rien d'autre avant)
        page = st.radio(
            "Navigation",
            ["Analysis", "Comparaison"],
            index=0,
            help="Choisissez la fonctionnalité à utiliser"
        )
        
        st.markdown("---")
        # Section informations
        st.header("ℹ️ Informations")
        st.markdown("**Algorithme :** OCR Adaptatif Multi-échelle")
        st.markdown("**Précision :** 93% (14/15 livres)")
        st.markdown("**GPU :** Support automatique")
        st.markdown("**Enrichissement :** Open Library intégré")
        st.markdown("---")
        # Paramètres recommandés
        st.markdown("**Paramètres recommandés :**")
        st.markdown("- **GPU** : Activé si disponible")
        st.markdown("- **Confiance** : 0.3 (optimisé)")
        st.markdown("---")
        # Tests effectués
        st.markdown("**Testé sur :**")
        st.markdown("- books1.jpg : 14/15 livres (93%)")
        st.markdown("- 6 images : moyenne 83.8%")
        return page