"""
Composant Sidebar - Page de Comparaison - ShelfReader P1

Ce module contient les éléments spécifiques à la sidebar
pour la page de comparaison OCR.
"""

import streamlit as st


def render_comparison_sidebar():
    """
    Affiche les éléments spécifiques à la sidebar de la page de comparaison.

    Inclut :
    - Objectif de la comparaison
    - Conseils pour la comparaison
    - Informations sur les moteurs
    """
    with st.sidebar:
        st.markdown("### 🎯 Objectif de la comparaison")
        st.markdown("""
        Cette fonctionnalité vous permet de:

        - **Comparer les performances** de différents moteurs OCR
        - **Évaluer la précision** de détection des livres
        - **Analyser les différences** de reconnaissance de texte
        - **Choisir le moteur optimal** selon vos besoins
        """)

        st.markdown("### 💡 Conseils pour la comparaison")
        st.markdown("""
        - **Sélectionnez 2-3 moteurs** pour un comparatif équilibré
        - **Utilisez des images variées** (différentes qualités, angles)
        - **Comparez les temps de traitement** et la précision
        - **Analysez les différences** de détection de zones
        """)

        st.markdown("### 🔧 Moteurs disponibles")
        st.markdown("""
        - **EasyOCR** : Spécialisé pour les textes complexes, excellent pour les livres
        - **Tesseract** : Moteur classique, rapide et fiable
        - **TrOCR** : Basé sur transformers, très précis pour l'impression
        """)