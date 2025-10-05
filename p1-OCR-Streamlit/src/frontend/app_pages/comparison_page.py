"""
Page de comparaison OCR - ShelfReader P1

Cette page permet de comparer les performances de plusieurs moteurs OCR
sur la même image, avec visualisations et graphiques comparatifs.
"""

import streamlit as st
import tempfile
import os
from PIL import Image

from components.results_display import display_comparison_results, display_comparison_charts
from components.visualization import display_comparison_visualizations
from utils.ocr_processing import ocr_processor


def show():
    """
    Affiche la page de comparaison des moteurs OCR.

    Cette fonction permet de:
    - Sélectionner plusieurs moteurs OCR à comparer
    - Traiter la même image avec tous les moteurs
    - Afficher les résultats côte à côte
    - Présenter des graphiques comparatifs
    - Visualiser les différences de détection
    """
    st.header("📊 Comparaison des moteurs OCR")
    st.markdown("Comparez plusieurs moteurs OCR sur la même image.")

    # Sélection des moteurs à comparer
    engines = ["EasyOCR", "Tesseract", "TrOCR"]
    selected_engines = st.multiselect(
        "Sélectionnez les moteurs OCR à comparer",
        options=engines,
        default=["EasyOCR", "Tesseract", "TrOCR"],
        help="Choisissez au moins deux moteurs pour la comparaison."
    )

    # Vérification du nombre minimum de moteurs
    if len(selected_engines) < 2:
        st.warning("Veuillez sélectionner au moins deux moteurs OCR.")
        return

    # Upload d'image
    uploaded_file = st.file_uploader(
        "Téléchargez une image pour la comparaison",
        type=['jpg', 'jpeg', 'png'],
        help="Formats supportés : JPG, PNG. Taille recommandée : 1000px minimum"
    )

    if uploaded_file is not None:
        # Charger et afficher l'image originale
        image = Image.open(uploaded_file)
        st.image(image, caption="Image à comparer", use_container_width=True)

        # Paramètres communs à tous les moteurs
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

        # Bouton de comparaison
        if st.button("🚀 Comparer les moteurs OCR", type="primary", use_container_width=True):
            # Barre de progression
            progress_bar = st.progress(0)

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
                # Traitement avec tous les moteurs sélectionnés
                results_dict = {}

                for idx, engine in enumerate(selected_engines):
                    # Mise à jour de la progression
                    progress_bar.progress(int((idx / len(selected_engines)) * 100))

                    with st.spinner(f"🔍 Traitement avec {engine}..."):
                        result, processing_time = ocr_processor.process_image(
                            temp_path,
                            engine_name=engine,
                            confidence=confidence,
                            use_gpu=use_gpu,
                            debug=debug_mode
                        )

                        if result:
                            result['processing_time'] = processing_time
                            results_dict[engine] = result
                        else:
                            st.error(f"Échec du traitement avec {engine}")
                            results_dict[engine] = {
                                'books': [],
                                'text': '',
                                'confidence': 0.0,
                                'processing_time': 0.0
                            }

                # Progression terminée
                progress_bar.progress(100)
                st.success("Comparaison terminée !")

                # Affichage des visualisations côte à côte
                display_comparison_visualizations(results_dict, selected_engines, temp_path)

                # Affichage des résultats détaillés
                display_comparison_results(results_dict, selected_engines)

                # Graphiques de comparaison avancés
                display_comparison_charts(results_dict, selected_engines)

            finally:
                # Nettoyage du fichier temporaire
                os.unlink(temp_path)

    else:
        # Message informatif quand aucune image n'est uploadée
        st.info("👆 Veuillez uploader une image pour commencer la comparaison")