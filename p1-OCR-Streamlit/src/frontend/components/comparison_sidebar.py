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
    - Paramètres avancés des engines OCR
    - Informations sur les moteurs
    """
    with st.sidebar:

            # Note: informations globales et paramètres avancés sont affichés
            # dans la sidebar principale (components.sidebar) juste après la navigation.

            # Conseils d'utilisation
            st.markdown("### 💡 Conseils d'utilisation")
            st.markdown("""
            - **Qualité d'image** : Photos bien éclairées, perpendiculaires à l'étagère
            - **Taille minimale** : 1000 pixels de largeur recommandée
            - **Formats** : JPG ou PNG
            - **Contenu** : Étageres de livres avec titres visibles
            """)

            # Paramètres recommandés (détail)
            st.markdown("### ⚙️ Paramètres recommandés")
            st.markdown("""
            - **Moteur OCR** : EasyOCR (recommandé)
            - **Confiance** : 0.3 (optimisé)
            - **GPU** : Activé si disponible
            - **Enrichissement OL** : Activé pour métadonnées
            """)

            # Moteurs OCR
            st.markdown("### 🔧 Moteurs OCR")
            st.markdown("""
            - **EasyOCR** : Spécialisé textes complexes
            - **Tesseract** : Rapide et fiable
            - **TrOCR** : Très précis (transformers)
            """)