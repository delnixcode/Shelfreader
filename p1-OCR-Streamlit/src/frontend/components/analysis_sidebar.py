"""
Composant Sidebar - Page d'Analyse - ShelfReader P1

Ce module contient les éléments spécifiques à la sidebar
pour la page d'analyse OCR.
"""

import streamlit as st


def render_analysis_sidebar():
    """
    Affiche les éléments spécifiques à la sidebar de la page d'analyse.

    Inclut :
    - Conseils d'utilisation
    - Paramètres recommandés
    - Informations sur les moteurs OCR
    """
    with st.sidebar:
        st.markdown("### 💡 Conseils d'utilisation")
        st.markdown("""
        - **Qualité d'image** : Photos bien éclairées, perpendiculaires à l'étagère
        - **Taille minimale** : 1000 pixels de largeur recommandée
        - **Formats** : JPG ou PNG
        - **Contenu** : Étageres de livres avec titres visibles
        """)

        st.markdown("### ⚙️ Paramètres recommandés")
        st.markdown("""
        - **Moteur OCR** : EasyOCR (recommandé)
        - **Confiance** : 0.3 (optimisé)
        - **GPU** : Activé si disponible
        - **Enrichissement OL** : Activé pour métadonnées
        """)

        st.markdown("### 🔧 Moteurs OCR")
        st.markdown("""
        - **EasyOCR** : Spécialisé textes complexes
        - **Tesseract** : Rapide et fiable
        - **TrOCR** : Très précis (transformers)
        """)