"""
Application principale ShelfReader P1 - OCR Adaptatif

Point d'entrée de l'application Streamlit pour ShelfReader P1.
Interface web pour l'analyse OCR adaptative multi-échelle avec détection
intelligente de livres sur étagères.

Architecture modulaire:
- app_pages/ : Pages Streamlit (analyse, comparaison)
- components/ : Composants réutilisables (sidebar, display, visualization)
- utils/ : Logique métier (OCR processing, enrichment)
- engines/ : Moteurs OCR spécialisés
- services/ : APIs externes (Open Library)
"""

import streamlit as st
import os
import sys

# Configuration du path pour les imports locaux
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import des pages
from app_pages.analysis_page import show as show_analysis_page
from app_pages.comparison_page import show as show_comparison_page

# Import des composants sidebar
from components.sidebar import render_sidebar
from components.analysis_sidebar import render_analysis_sidebar
from components.comparison_sidebar import render_comparison_sidebar


def main():
    """
    Fonction principale de l'application.

    Configure l'interface Streamlit et gère la navigation
    entre les différentes pages de l'application.
    """
    # Configuration de la page Streamlit
    st.set_page_config(
        page_title="ShelfReader P1 - OCR Adaptatif",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Titre principal
    st.title("📚 ShelfReader P1 - OCR Adaptatif")
    st.markdown("**Détection automatique de livres sur étagères avec OCR intelligent**")
    st.markdown("---")

    # Rendu de la sidebar et récupération de la page sélectionnée
    selected_page = render_sidebar()

    # Navigation entre les pages
    if selected_page == "Analysis":
        render_analysis_sidebar()
        show_analysis_page()
    elif selected_page == "Comparaison":
        render_comparison_sidebar()
        show_comparison_page()


if __name__ == "__main__":
    main()