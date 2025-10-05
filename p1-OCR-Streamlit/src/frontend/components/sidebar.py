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
        # Paramètres avancés (global) — placés juste après la navigation
        st.markdown("### 🔧 Paramètres avancés (optionnel)")
        with st.expander("⚙️ Paramètres communs"):
            # Seuil de confiance global
            global_confidence = st.slider(
                "Seuil de confiance",
                min_value=0.1,
                max_value=1.0,
                value=0.3,
                step=0.1,
                help="Confiance minimale pour accepter un résultat (0.1 = plus de détections)",
                key="global_confidence"
            )

            # GPU/CPU global
            global_use_gpu = st.checkbox(
                "Utiliser GPU",
                value=True,
                help="Accélère considérablement le traitement si GPU disponible",
                key="global_gpu"
            )

            # Stocker les paramètres communs dans session_state
            if 'global_params' not in st.session_state:
                st.session_state.global_params = {}

            st.session_state.global_params.update({
                'confidence': global_confidence,
                'use_gpu': global_use_gpu
            })

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