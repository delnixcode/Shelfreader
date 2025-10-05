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

    # Configuration des moteurs à comparer
    st.markdown("### 🔧 Configuration des moteurs à comparer")
    
    # Nombre de configurations à comparer
    num_configs = st.slider(
        "Nombre de configurations à comparer",
        min_value=2,
        max_value=6,
        value=3,
        help="Nombre de configurations OCR différentes à comparer (2-6)"
    )

    # Liste des moteurs disponibles
    available_engines = ["EasyOCR", "Tesseract", "TrOCR"]
    
    # Configurations des moteurs
    engine_configs = []
    
    for i in range(num_configs):
        st.markdown(f"**Configuration {i+1}**")
        cols = st.columns([2, 3])
        
        with cols[0]:
            engine = st.selectbox(
                f"Moteur OCR {i+1}",
                options=available_engines,
                key=f"engine_{i}",
                help=f"Sélectionnez le moteur OCR pour la configuration {i+1}"
            )
        
        # Générer automatiquement le nom de la configuration
        config_name = f"Configuration {i+1} ({engine})"
        
        engine_configs.append({
            'engine': engine,
            'name': config_name,
            'index': i
        })

    # Vérifier qu'on a au moins deux configurations différentes
    if len(set(config['engine'] for config in engine_configs)) < 2 and len(engine_configs) > 1:
        st.warning("⚠️ Pour une comparaison pertinente, utilisez au moins deux moteurs OCR différents.")
    
    # Extraire les moteurs sélectionnés (pour compatibilité avec le code existant)
    selected_engines = [config['engine'] for config in engine_configs]

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

        # Paramètres spécifiques pour chaque configuration
        st.markdown("### 🔧 Paramètres spécifiques par configuration")
        advanced_params = {}

        for config in engine_configs:
            engine = config['engine']
            config_name = config['name']
            config_index = config['index']
            
            with st.expander(f"⚙️ {config_name}"):
                if engine == "EasyOCR":
                    # Paramètres communs pour EasyOCR
                    easyocr_confidence = st.slider(
                        "Seuil de confiance",
                        min_value=0.1,
                        max_value=1.0,
                        value=0.3,
                        step=0.1,
                        help="Confiance minimale pour accepter un résultat (0.1 = plus de détections)",
                        key=f"comp_easyocr_confidence_{config_index}"
                    )
                    
                    easyocr_use_gpu = st.checkbox(
                        "Utiliser GPU",
                        value=True,
                        help="Accélère considérablement le traitement si GPU disponible",
                        key=f"comp_easyocr_gpu_{config_index}"
                    )
                    
                    # Sélecteur de langue
                    easyocr_lang = st.multiselect(
                        "Langues",
                        options=["en", "fr", "de", "es", "it"],
                        default=["en"],
                        help="Langues à utiliser pour la reconnaissance",
                        key=f"comp_easyocr_lang_{config_index}"
                    )

                    # Méthode de détection de tranches
                    easyocr_spine_method = st.selectbox(
                        "Méthode de détection",
                        options=["vertical_lines", "horizontal_shelves"],
                        index=0,
                        help="Algorithme de détection des séparations entre livres",
                        key=f"comp_easyocr_spine_{config_index}"
                    )

                    advanced_params[config_name] = {
                        'engine': engine,
                        'confidence': easyocr_confidence,
                        'use_gpu': easyocr_use_gpu,
                        'languages': easyocr_lang,
                        'spine_method': easyocr_spine_method
                    }

                elif engine == "Tesseract":
                    # Paramètres communs pour Tesseract
                    tesseract_confidence = st.slider(
                        "Seuil de confiance",
                        min_value=0.1,
                        max_value=1.0,
                        value=0.3,
                        step=0.1,
                        help="Confiance minimale pour accepter un résultat (0.1 = plus de détections)",
                        key=f"comp_tesseract_confidence_{config_index}"
                    )
                    
                    tesseract_use_gpu = st.checkbox(
                        "Utiliser GPU",
                        value=True,
                        help="Accélère considérablement le traitement si GPU disponible",
                        key=f"comp_tesseract_gpu_{config_index}"
                    )
                    
                    # Sélecteur de langue
                    tesseract_lang = st.selectbox(
                        "Langue",
                        options=["eng", "fra", "deu", "spa", "ita"],
                        index=0,
                        help="Langue principale pour la reconnaissance",
                        key=f"comp_tesseract_lang_{config_index}"
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
                        help="Comment Tesseract analyse la structure de la page",
                        key=f"comp_tesseract_psm_{config_index}"
                    )[0]

                    advanced_params[config_name] = {
                        'engine': engine,
                        'confidence': tesseract_confidence,
                        'use_gpu': tesseract_use_gpu,
                        'lang': tesseract_lang,
                        'psm': int(tesseract_psm)
                    }

                elif engine == "TrOCR":
                    # Paramètres communs pour TrOCR
                    trocr_confidence = st.slider(
                        "Seuil de confiance",
                        min_value=0.1,
                        max_value=1.0,
                        value=0.3,
                        step=0.1,
                        help="Confiance minimale pour accepter un résultat (0.1 = plus de détections)",
                        key=f"comp_trocr_confidence_{config_index}"
                    )
                    
                    trocr_use_gpu = st.checkbox(
                        "Utiliser GPU",
                        value=True,
                        help="Accélère considérablement le traitement si GPU disponible",
                        key=f"comp_trocr_gpu_{config_index}"
                    )
                    
                    # Device
                    trocr_device = st.selectbox(
                        "Device",
                        options=["auto", "cuda", "cpu"],
                        index=0,
                        help="Matériel pour exécuter le modèle (auto = détection automatique)",
                        key=f"comp_trocr_device_{config_index}"
                    )

                    # Validation des conflits pour TrOCR
                    conflict_warning = None
                    if trocr_use_gpu and trocr_device == "cpu":
                        conflict_warning = f"⚠️ **Conflit détecté** dans {config_name} : GPU activé mais device CPU sélectionné. Le device CPU sera prioritaire."
                        trocr_use_gpu = False  # Résoudre automatiquement le conflit
                    elif not trocr_use_gpu and trocr_device == "cuda":
                        conflict_warning = f"⚠️ **Conflit détecté** dans {config_name} : GPU désactivé mais device CUDA sélectionné. Le device CUDA sera prioritaire."
                        trocr_use_gpu = True  # Résoudre automatiquement le conflit

                    if conflict_warning:
                        st.warning(conflict_warning)

                    advanced_params[config_name] = {
                        'engine': engine,
                        'confidence': trocr_confidence,
                        'use_gpu': trocr_use_gpu,
                        'device': trocr_device
                    }

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
                # Les advanced_params sont déjà définis plus haut dans la boucle de configuration
                # Ils contiennent les paramètres spécifiques à chaque configuration

                # Construction des commandes réellement exécutées (pour debug)
                executed_commands = {}
                for config in engine_configs:
                    engine = config['engine']
                    config_name = config['name']
                    
                    cmd_parts = ["python", f"src/engines/{engine.lower()}/main.py", temp_path]
                    
                    # Paramètres spécifiques à cette configuration - TOUJOURS inclus
                    config_adv_params = advanced_params.get(config_name, {})
                    config_confidence = config_adv_params.get('confidence', 0.3)
                    config_use_gpu = config_adv_params.get('use_gpu', True)
                    
                    # Pour TrOCR, le device prend la priorité sur use_gpu
                    if engine == 'TrOCR':
                        trocr_device = config_adv_params.get('device', 'auto')
                        if trocr_device == 'cuda':
                            config_use_gpu = True
                        elif trocr_device == 'cpu':
                            config_use_gpu = False
                        # Pour 'auto', garder la valeur de use_gpu
                    
                    if config_use_gpu:
                        cmd_parts.append("--gpu")
                    else:
                        cmd_parts.append("--cpu")
                    
                    cmd_parts.extend(["--confidence", str(config_confidence)])
                    
                    if debug_mode:
                        cmd_parts.append("--debug")
                    
                    # Paramètres avancés pour cette configuration - TOUJOURS inclus
                    if engine == 'EasyOCR':
                        cmd_parts.extend(["--spine-method", config_adv_params.get('spine_method', 'vertical_lines')])
                        if config_adv_params.get('languages'):
                            cmd_parts.extend(["--lang"] + config_adv_params['languages'])
                    elif engine == 'Tesseract':
                        if config_adv_params.get('lang'):
                            cmd_parts.extend(["--lang", config_adv_params['lang']])
                        if config_adv_params.get('psm') is not None:
                            cmd_parts.extend(["--psm", str(config_adv_params['psm'])])
                    elif engine == 'TrOCR':
                        if config_adv_params.get('device'):
                            cmd_parts.extend(["--device", config_adv_params['device']])
                    
                    executed_commands[config_name] = " ".join(cmd_parts)

                # Adapter advanced_params pour ocr_processor.compare_engines
                # Le processeur s'attend à des clés par moteur, mais nous avons des configurations nommées
                processor_advanced_params = {}
                for config in engine_configs:
                    engine = config['engine']
                    config_name = config['name']
                    config_params = advanced_params.get(config_name, {}).copy()
                    config_params.pop('engine', None)  # Retirer la clé 'engine' si elle existe
                    # Pour les moteurs multiples du même type, on garde seulement la dernière configuration
                    # car ocr_processor ne gère pas plusieurs configurations du même moteur
                    processor_advanced_params[engine] = config_params

                # Traitement de chaque configuration individuellement
                with st.spinner("🔍 Comparaison en cours..."):
                    config_results = {}
                    
                    for config in engine_configs:
                        engine = config['engine']
                        config_name = config['name']
                        
                        # Paramètres pour cette configuration spécifique
                        config_adv_params = advanced_params.get(config_name, {}).copy()
                        config_confidence = config_adv_params.pop('confidence', 0.3)
                        config_use_gpu = config_adv_params.pop('use_gpu', True)
                        
                        # Traiter cette configuration individuellement
                        result, processing_time = ocr_processor.process_image(
                            temp_path,
                            engine,
                            confidence=config_confidence,
                            use_gpu=config_use_gpu,
                            debug=debug_mode,
                            advanced_params=config_adv_params
                        )
                        
                        if result:
                            result['processing_time'] = processing_time
                            config_results[config_name] = result
                        else:
                            config_results[config_name] = {
                                'books': [],
                                'text': '',
                                'confidence': 0.0,
                                'processing_time': processing_time,
                                'engine': engine
                            }

                # Progression terminée
                progress_bar.progress(100)
                st.success("Comparaison terminée !")

                # Utiliser les noms de configuration pour l'affichage
                config_names = [config['name'] for config in engine_configs]

                # Affichage des visualisations côte à côte
                display_comparison_visualizations(config_results, config_names, temp_path)

                # Affichage des résultats détaillés
                display_comparison_results(config_results, config_names,
                                        global_confidence=None,  # Plus de paramètres globaux
                                        global_use_gpu=None,     # Plus de paramètres globaux
                                        advanced_params=advanced_params,
                                        executed_commands=executed_commands)

                # Graphiques de comparaison avancés
                display_comparison_charts(config_results, config_names)

            finally:
                # Nettoyage du fichier temporaire
                os.unlink(temp_path)

    else:
        # Message informatif quand aucune image n'est uploadée
        st.info("👆 Veuillez uploader une image pour commencer la comparaison")