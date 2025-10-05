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

            # Récupérer les paramètres globaux de la sidebar
            global_confidence = 0.3
            global_use_gpu = True
            if 'global_params' in st.session_state:
                global_confidence = st.session_state.global_params.get('confidence', 0.3)
                global_use_gpu = st.session_state.global_params.get('use_gpu', True)

            # Afficher les paramètres globaux (lecture seule)
            st.markdown("**Paramètres globaux (configurés dans la sidebar) :**")
            col_conf, col_gpu = st.columns(2)
            with col_conf:
                st.metric("Confiance", f"{global_confidence}")
            with col_gpu:
                st.metric("GPU", "Activé" if global_use_gpu else "Désactivé")

            # Paramètres spécifiques selon le moteur
            advanced_params = {}

            if ocr_engine == "EasyOCR":
                st.markdown("### 🎯 Paramètres EasyOCR")
                
                # Sélecteur de langue
                easyocr_lang = st.multiselect(
                    "Langues",
                    options=["en", "fr", "de", "es", "it"],
                    default=["en"],
                    help="Langues à utiliser pour la reconnaissance"
                )

                # Méthode de détection de tranches
                easyocr_spine_method = st.selectbox(
                    "Méthode de détection",
                    options=["vertical_lines", "horizontal_shelves"],
                    index=0,
                    help="Algorithme de détection des séparations entre livres"
                )

                advanced_params = {
                    'languages': easyocr_lang,
                    'spine_method': easyocr_spine_method
                }
                st.session_state.easyocr_params = advanced_params

            elif ocr_engine == "Tesseract":
                st.markdown("### 📝 Paramètres Tesseract")
                
                # Sélecteur de langue
                tesseract_lang = st.selectbox(
                    "Langue",
                    options=["eng", "fra", "deu", "spa", "ita"],
                    index=0,
                    help="Langue principale pour la reconnaissance"
                )

                # PSM (Page Segmentation Mode)
                tesseract_psm = st.selectbox(
                    "Mode de segmentation (PSM)",
                    options=[
                        ("6", "Bloc uniforme de texte (recommandé)"),
                        ("3", "Analyse automatique complète"),
                        ("8", "Ligne de texte unique"),
                        ("13", "Ligne brute")
                    ],
                    index=0,
                    format_func=lambda x: x[1],
                    help="Comment Tesseract analyse la structure de la page"
                )[0]

                advanced_params = {
                    'lang': tesseract_lang,
                    'psm': int(tesseract_psm)
                }
                st.session_state.tesseract_params = advanced_params

            elif ocr_engine == "TrOCR":
                st.markdown("### 🤖 Paramètres TrOCR")
                
                # Device
                trocr_device = st.selectbox(
                    "Device",
                    options=["auto", "cuda", "cpu"],
                    index=0,
                    help="Matériel pour exécuter le modèle (auto = détection automatique)"
                )

                advanced_params = {
                    'device': trocr_device
                }
                st.session_state.trocr_params = advanced_params

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
                    # Récupérer les paramètres avancés selon le moteur sélectionné
                    advanced_params = None
                    if ocr_engine == 'EasyOCR' and 'easyocr_params' in st.session_state:
                        advanced_params = st.session_state.easyocr_params
                    elif ocr_engine == 'Tesseract' and 'tesseract_params' in st.session_state:
                        advanced_params = st.session_state.tesseract_params
                    elif ocr_engine == 'TrOCR' and 'trocr_params' in st.session_state:
                        advanced_params = st.session_state.trocr_params
                    
                    # Construction de la commande réellement exécutée (pour debug)
                    executed_cmd_parts = ["python", "main.py", temp_path]
                    
                    # Paramètres globaux - TOUJOURS inclus
                    if global_use_gpu:
                        executed_cmd_parts.append("--gpu")
                    else:
                        executed_cmd_parts.append("--cpu")
                    
                    executed_cmd_parts.extend(["--confidence", str(global_confidence)])
                    
                    if debug_mode:
                        executed_cmd_parts.append("--debug")
                    
                    # Paramètres avancés - TOUJOURS inclus selon le moteur
                    if advanced_params:
                        if ocr_engine == 'EasyOCR':
                            executed_cmd_parts.extend(["--spine-method", advanced_params.get('spine_method', 'vertical_lines')])
                            if advanced_params.get('languages'):
                                executed_cmd_parts.extend(["--lang"] + advanced_params['languages'])
                        elif ocr_engine == 'Tesseract':
                            if advanced_params.get('lang'):
                                executed_cmd_parts.extend(["--lang", advanced_params['lang']])
                            if advanced_params.get('psm') is not None:
                                executed_cmd_parts.extend(["--psm", str(advanced_params['psm'])])
                        elif ocr_engine == 'TrOCR':
                            if advanced_params.get('device'):
                                executed_cmd_parts.extend(["--device", advanced_params['device']])
                    
                    executed_command = " ".join(executed_cmd_parts)
                    
                    # Traitement OCR avec paramètres avancés
                    results, processing_time = ocr_processor.process_image(
                        temp_path,
                        engine_name=ocr_engine,
                        confidence=global_confidence,
                        use_gpu=global_use_gpu,
                        debug=debug_mode,
                        advanced_params=advanced_params
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
                        display_results(results, processing_time, enriched_books,
                                      engine_name=ocr_engine,
                                      global_confidence=global_confidence,
                                      global_use_gpu=global_use_gpu,
                                      advanced_params=advanced_params,
                                      executed_command=executed_command)

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