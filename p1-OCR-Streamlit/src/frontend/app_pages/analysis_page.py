"""
Page d'analyse OCR - ShelfReader P1

Cette page permet l'analyse OCR d'une image d'étagère de livres
avec enrichissement optionnel via Open Library.
"""

import streamlit as st
import tempfile
import os
from PIL import Image

from components.results_display import display_results
from components.visualization import display_visualization, display_book_details
from utils.ocr_processing import ocr_processor
from utils.openlibrary_enrichment import openlibrary_enricher


def show():
    """
    Affiche la page principale d'analyse OCR.

    Cette fonction gère:
    - L'upload d'image
    - La configuration des paramètres OCR
    - Le traitement OCR avec le moteur sélectionné
    - L'enrichissement optionnel avec Open Library
    - L'affichage des résultats et visualisations
    """
    st.header("🖼️ Upload et traitement d'image")

    # Upload d'image
    uploaded_file = st.file_uploader(
        "Choisissez une image d'étagère de livres",
        type=['jpg', 'jpeg', 'png'],
        help="Formats supportés : JPG, PNG. Taille recommandée : 1000px minimum"
    )

    if uploaded_file is not None:
        # Charger et afficher l'image
        image = Image.open(uploaded_file)

        # Layout: image originale + paramètres
        col_img, col_params = st.columns([1, 1])

        with col_img:
            st.subheader("📷 Image originale")
            st.image(image, use_container_width=True)

        with col_params:
            st.subheader("⚙️ Paramètres de traitement")

            # Sélection du moteur OCR
            ocr_engine = st.selectbox(
                "Moteur OCR",
                ["EasyOCR", "Tesseract", "TrOCR"],
                index=0,
                help="Choisissez le moteur OCR à utiliser"
            )

            # Paramètres de traitement
            confidence = st.slider(
                "Seuil de confiance OCR",
                min_value=0.1,
                max_value=1.0,
                value=0.3,
                step=0.1,
                help="0.1 = tolérant, 0.5 = strict. Recommandé : 0.3"
            )

            use_gpu = st.checkbox(
                "Utiliser le GPU (recommandé)",
                value=True,
                help="Accélère le traitement si GPU disponible"
            )

            debug_mode = st.checkbox(
                "Mode debug",
                value=False,
                help="Affiche les analyses détaillées (plus lent)"
            )

            # Option d'enrichissement
            enrich_with_ol = st.checkbox(
                "Enrichir avec Open Library",
                value=True,
                help="Recherche les métadonnées des livres sur Open Library (nécessite connexion internet)"
            )

        st.markdown("---")

        # Bouton de traitement
        if st.button("🚀 Lancer l'analyse OCR", type="primary", use_container_width=True):
            with st.spinner("🔍 Analyse en cours avec algorithme adaptatif..."):
                # Sauvegarde temporaire de l'image
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                    # Conversion en RGB si nécessaire
                    if image.mode == 'RGBA':
                        background = Image.new('RGB', image.size, (255, 255, 255))
                        background.paste(image, mask=image.split()[-1])
                        background.save(tmp_file.name, 'JPEG')
                    else:
                        rgb_image = image.convert('RGB')
                        rgb_image.save(tmp_file.name, 'JPEG')
                    temp_path = tmp_file.name

                try:
                    # Traitement OCR
                    results, processing_time = ocr_processor.process_image(
                        temp_path,
                        engine_name=ocr_engine,
                        confidence=confidence,
                        use_gpu=use_gpu,
                        debug=debug_mode
                    )

                    if results:
                        # Enrichissement optionnel
                        enriched_books = None
                        if enrich_with_ol and results.get('books'):
                            with st.spinner("🔍 Enrichissement avec Open Library..."):
                                enriched_books = openlibrary_enricher.enrich_books(results['books'])

                        # Message de succès
                        success_msg = "✅ Analyse terminée !"
                        if enrich_with_ol:
                            success_msg += " + Enrichissement OL"
                        st.success(success_msg)

                        st.markdown("---")

                        # Affichage des résultats
                        display_results(results, processing_time, enriched_books)

                        # Section visualisation et détails
                        st.markdown("---")

                        # Visualisation des zones détectées
                        books = enriched_books if enriched_books else results.get('books', [])
                        display_visualization(temp_path, books)

                        # Détails par livre
                        if books:
                            col_det, col_viz = st.columns([1, 1])
                            with col_det:
                                display_book_details(books, temp_path)

                        # Section informations techniques (expandable)
                        with st.expander("🔧 Informations techniques"):
                            st.json(results)

                    else:
                        st.error("❌ Échec de l'analyse OCR")

                finally:
                    # Nettoyage du fichier temporaire
                    os.unlink(temp_path)

    else:
        # Message d'accueil quand aucune image n'est uploadée
        st.info("👆 Veuillez uploader une image d'étagère de livres pour commencer l'analyse")